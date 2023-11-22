from typing import List, Dict, Set, Optional, Any, Union

import warp as wp

import re
import ast

from warp.sparse import BsrMatrix, bsr_zeros, bsr_set_from_triplets, bsr_copy, bsr_assign
from warp.types import type_length
from warp.utils import array_cast
from warp.codegen import get_annotations

from warp.fem.domain import GeometryDomain
from warp.fem.field import (
    TestField,
    TrialField,
    FieldLike,
    DiscreteField,
    FieldRestriction,
    make_restriction,
)
from warp.fem.quadrature import Quadrature, RegularQuadrature
from warp.fem.operator import Operator, Integrand
from warp.fem import cache
from warp.fem.types import Domain, Field, Sample, DofIndex, NULL_DOF_INDEX, OUTSIDE, make_free_sample


def _resolve_path(func, node):
    """
    Resolves variable and path from ast node/attribute (adapted from warp.codegen)
    """

    modules = []

    while isinstance(node, ast.Attribute):
        modules.append(node.attr)
        node = node.value

    if isinstance(node, ast.Name):
        modules.append(node.id)

    # reverse list since ast presents it backward order
    path = [*reversed(modules)]

    if len(path) == 0:
        return None, path

    # try and evaluate object path
    try:
        # Look up the closure info and append it to adj.func.__globals__
        # in case you want to define a kernel inside a function and refer
        # to varibles you've declared inside that function:
        capturedvars = dict(
            zip(
                func.__code__.co_freevars,
                [c.cell_contents for c in (func.__closure__ or [])],
            )
        )

        vars_dict = {**func.__globals__, **capturedvars}
        func = eval(".".join(path), vars_dict)
        return func, path
    except (NameError, AttributeError):
        pass

    return None, path


def _path_to_ast_attribute(name: str) -> ast.Attribute:
    path = name.split(".")
    path.reverse()

    node = ast.Name(id=path.pop(), ctx=ast.Load())
    while len(path):
        node = ast.Attribute(
            value=node,
            attr=path.pop(),
            ctx=ast.Load(),
        )
    return node


class IntegrandTransformer(ast.NodeTransformer):
    def __init__(self, integrand: Integrand, field_args: Dict[str, FieldLike]):
        self._integrand = integrand
        self._field_args = field_args

    def visit_Call(self, call: ast.Call):
        call = self.generic_visit(call)

        callee = getattr(call.func, "id", None)
        if callee in self._field_args:
            # Shortcut for evaluating fields as f(x...)
            field = self._field_args[callee]

            arg_type = self._integrand.argspec.annotations[callee]
            operator = arg_type.call_operator

            call.func = ast.Attribute(
                value=_path_to_ast_attribute(f"{arg_type.__module__}.{arg_type.__qualname__}"),
                attr="call_operator",
                ctx=ast.Load(),
            )
            call.args = [ast.Name(id=callee, ctx=ast.Load())] + call.args

            self._replace_call_func(call, operator, field)

            return call

        func, _ = _resolve_path(self._integrand.func, call.func)

        if isinstance(func, Operator) and len(call.args) > 0:
            # Evaluating operators as op(field, x, ...)
            callee = getattr(call.args[0], "id", None)
            if callee in self._field_args:
                field = self._field_args[callee]
                self._replace_call_func(call, func, field)

        if isinstance(func, Integrand):
            key = self._translate_callee(func, call.args)
            call.func = ast.Attribute(
                value=call.func,
                attr=key,
                ctx=ast.Load(),
            )

        # print(ast.dump(call, indent=4))

        return call

    def _replace_call_func(self, call: ast.Call, operator: Operator, field: FieldLike):
        try:
            pointer = operator.resolver(field)
            setattr(operator, pointer.key, pointer)
        except AttributeError:
            raise ValueError(f"Operator {operator.func.__name__} is not defined for field {field.name}")
        call.func = ast.Attribute(value=call.func, attr=pointer.key, ctx=ast.Load())

    def _translate_callee(self, callee: Integrand, args: List[ast.AST]):
        # Get field types for call site arguments
        call_site_field_args = []
        for arg in args:
            name = getattr(arg, "id", None)
            if name in self._field_args:
                call_site_field_args.append(self._field_args[name])

        call_site_field_args.reverse()

        # Pass to callee in same order
        callee_field_args = {}
        for arg in callee.argspec.args:
            arg_type = callee.argspec.annotations[arg]
            if arg_type in (Field, Domain):
                callee_field_args[arg] = call_site_field_args.pop()

        return _translate_integrand(callee, callee_field_args).key


def _translate_integrand(integrand: Integrand, field_args: Dict[str, FieldLike]) -> wp.Function:
    # Specialize field argument types
    argspec = integrand.argspec
    annotations = {}
    for arg in argspec.args:
        arg_type = argspec.annotations[arg]
        if arg_type == Field:
            annotations[arg] = field_args[arg].ElementEvalArg
        elif arg_type == Domain:
            annotations[arg] = field_args[arg].ElementArg
        else:
            annotations[arg] = arg_type

    # Transform field evaluation calls
    transformer = IntegrandTransformer(integrand, field_args)

    def is_field_like(f):
        return isinstance(f, FieldLike)

    suffix = "_".join([f.name for f in field_args.values() if is_field_like(f)])

    func = cache.get_integrand_function(
        integrand=integrand,
        suffix=suffix,
        annotations=annotations,
        code_transformers=[transformer],
    )

    key = func.key
    setattr(integrand, key, integrand.module.functions[key])

    return getattr(integrand, key)


def _get_integrand_field_arguments(
    integrand: Integrand,
    fields: Dict[str, FieldLike],
    domain: GeometryDomain = None,
):
    # parse argument types
    field_args = {}
    value_args = {}

    domain_name = None
    sample_name = None

    argspec = integrand.argspec
    for arg in argspec.args:
        arg_type = argspec.annotations[arg]
        if arg_type == Field:
            if arg not in fields:
                raise ValueError(f"Missing field for argument '{arg}'")
            field_args[arg] = fields[arg]
        elif arg_type == Domain:
            domain_name = arg
            field_args[arg] = domain
        elif arg_type == Sample:
            sample_name = arg
        else:
            value_args[arg] = arg_type

    return field_args, value_args, domain_name, sample_name


def _get_test_and_trial_fields(
    fields: Dict[str, FieldLike],
):
    test = None
    trial = None
    test_name = None
    trial_name = None

    for name, field in fields.items():
        if isinstance(field, TestField):
            if test is not None:
                raise ValueError("Duplicate test field argument")
            test = field
            test_name = name
        elif isinstance(field, TrialField):
            if trial is not None:
                raise ValueError("Duplicate test field argument")
            trial = field
            trial_name = name

    if trial is not None:
        if test is None:
            raise ValueError("A trial field cannot be provided without a test field")

        if test.domain != trial.domain:
            raise ValueError("Incompatible test and trial domains")

    return test, test_name, trial, trial_name


def _gen_field_struct(field_args: Dict[str, FieldLike]):
    class Fields:
        pass

    annotations = get_annotations(Fields)

    for name, arg in field_args.items():
        if isinstance(arg, GeometryDomain):
            continue
        setattr(Fields, name, arg.EvalArg())
        annotations[name] = arg.EvalArg

    try:
        Fields.__annotations__ = annotations
    except AttributeError:
        setattr(Fields.__dict__, "__annotations__", annotations)

    suffix = "_".join([f"{name}_{arg_struct.cls.__qualname__}" for name, arg_struct in annotations.items()])

    return cache.get_struct(Fields, suffix=suffix)


def _gen_value_struct(value_args: Dict[str, type]):
    class Values:
        pass

    annotations = get_annotations(Values)

    for name, arg_type in value_args.items():
        setattr(Values, name, None)
        annotations[name] = arg_type

    def arg_type_name(arg_type):
        if isinstance(arg_type, wp.codegen.Struct):
            return arg_type_name(arg_type.cls)
        return getattr(arg_type, "__name__", str(arg_type))

    def arg_type_name(arg_type):
        if isinstance(arg_type, wp.codegen.Struct):
            return arg_type_name(arg_type.cls)
        return getattr(arg_type, "__name__", str(arg_type))

    try:
        Values.__annotations__ = annotations
    except AttributeError:
        setattr(Values.__dict__, "__annotations__", annotations)

    suffix = "_".join([f"{name}_{arg_type_name(arg_type)}" for name, arg_type in annotations.items()])

    return cache.get_struct(Values, suffix=suffix)


def _get_trial_arg():
    pass


def _get_test_arg():
    pass


class _FieldWrappers:
    pass


def _register_integrand_field_wrappers(integrand_func: wp.Function, fields: Dict[str, FieldLike]):
    integrand_func._field_wrappers = _FieldWrappers()
    for name, field in fields.items():
        setattr(integrand_func._field_wrappers, name, field.ElementEvalArg)


class PassFieldArgsToIntegrand(ast.NodeTransformer):
    def __init__(
        self,
        arg_names: List[str],
        field_args: Set[str],
        value_args: Set[str],
        sample_name: str,
        domain_name: str,
        test_name: str = None,
        trial_name: str = None,
        func_name: str = "integrand_func",
        fields_var_name: str = "fields",
        values_var_name: str = "values",
        domain_var_name: str = "domain_arg",
        sample_var_name: str = "sample",
        field_wrappers_attr: str = "_field_wrappers",
    ):
        self._arg_names = arg_names
        self._field_args = field_args
        self._value_args = value_args
        self._domain_name = domain_name
        self._sample_name = sample_name
        self._func_name = func_name
        self._test_name = test_name
        self._trial_name = trial_name
        self._fields_var_name = fields_var_name
        self._values_var_name = values_var_name
        self._domain_var_name = domain_var_name
        self._sample_var_name = sample_var_name
        self._field_wrappers_attr = field_wrappers_attr

    def visit_Call(self, call: ast.Call):
        call = self.generic_visit(call)

        callee = getattr(call.func, "id", None)

        if callee == self._func_name:
            # Replace function arguments with ours generated structs
            call.args.clear()
            for arg in self._arg_names:
                if arg == self._domain_name:
                    call.args.append(
                        ast.Name(id=self._domain_var_name, ctx=ast.Load()),
                    )
                elif arg == self._sample_name:
                    call.args.append(
                        ast.Name(id=self._sample_var_name, ctx=ast.Load()),
                    )
                elif arg in self._field_args:
                    call.args.append(
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Attribute(
                                    value=ast.Name(id=self._func_name, ctx=ast.Load()),
                                    attr=self._field_wrappers_attr,
                                    ctx=ast.Load(),
                                ),
                                attr=arg,
                                ctx=ast.Load(),
                            ),
                            args=[
                                ast.Name(id=self._domain_var_name, ctx=ast.Load()),
                                ast.Attribute(
                                    value=ast.Name(id=self._fields_var_name, ctx=ast.Load()),
                                    attr=arg,
                                    ctx=ast.Load(),
                                ),
                            ],
                            keywords=[],
                        )
                    )
                elif arg in self._value_args:
                    call.args.append(
                        ast.Attribute(
                            value=ast.Name(id=self._values_var_name, ctx=ast.Load()),
                            attr=arg,
                            ctx=ast.Load(),
                        )
                    )
                else:
                    raise RuntimeError(f"Unhandled argument {arg}")
            # print(ast.dump(call, indent=4))
        elif callee == _get_test_arg.__name__:
            # print(ast.dump(call, indent=4))
            call = ast.Attribute(
                value=ast.Name(id=self._fields_var_name, ctx=ast.Load()),
                attr=self._test_name,
                ctx=ast.Load(),
            )
        elif callee == _get_trial_arg.__name__:
            # print(ast.dump(call, indent=4))
            call = ast.Attribute(
                value=ast.Name(id=self._fields_var_name, ctx=ast.Load()),
                attr=self._trial_name,
                ctx=ast.Load(),
            )

        return call


def get_integrate_null_kernel(
    integrand_func: wp.Function,
    domain: GeometryDomain,
    quadrature: Quadrature,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
):
    def integrate_kernel_fn(
        qp_arg: quadrature.Arg,
        domain_arg: domain.ElementArg,
        domain_index_arg: domain.ElementIndexArg,
        fields: FieldStruct,
        values: ValueStruct,
    ):
        element_index = domain.element_index(domain_index_arg, wp.tid())

        test_dof_index = NULL_DOF_INDEX
        trial_dof_index = NULL_DOF_INDEX

        qp_point_count = quadrature.point_count(domain_arg, qp_arg, element_index)
        for k in range(qp_point_count):
            qp_index = quadrature.point_index(domain_arg, qp_arg, element_index, k)
            qp_coords = quadrature.point_coords(domain_arg, qp_arg, element_index, k)
            qp_weight = quadrature.point_weight(domain_arg, qp_arg, element_index, k)
            sample = Sample(element_index, qp_coords, qp_index, qp_weight, test_dof_index, trial_dof_index)
            integrand_func(sample, fields, values)

    return integrate_kernel_fn


def get_integrate_constant_kernel(
    integrand_func: wp.Function,
    domain: GeometryDomain,
    quadrature: Quadrature,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
    accumulate_dtype,
):
    def integrate_kernel_fn(
        qp_arg: quadrature.Arg,
        domain_arg: domain.ElementArg,
        domain_index_arg: domain.ElementIndexArg,
        fields: FieldStruct,
        values: ValueStruct,
        result: wp.array(dtype=accumulate_dtype),
    ):
        element_index = domain.element_index(domain_index_arg, wp.tid())
        elem_sum = accumulate_dtype(0.0)

        test_dof_index = NULL_DOF_INDEX
        trial_dof_index = NULL_DOF_INDEX

        qp_point_count = quadrature.point_count(domain_arg, qp_arg, element_index)
        for k in range(qp_point_count):
            qp_index = quadrature.point_index(domain_arg, qp_arg, element_index, k)
            coords = quadrature.point_coords(domain_arg, qp_arg, element_index, k)
            qp_weight = quadrature.point_weight(domain_arg, qp_arg, element_index, k)
            
            sample = Sample(element_index, coords, qp_index, qp_weight, test_dof_index, trial_dof_index)
            vol = domain.element_measure(domain_arg, sample)

            val = integrand_func(sample, fields, values)

            elem_sum += accumulate_dtype(qp_weight * vol * val)

        wp.atomic_add(result, 0, elem_sum)

    return integrate_kernel_fn


def get_integrate_linear_kernel(
    integrand_func: wp.Function,
    domain: GeometryDomain,
    quadrature: Quadrature,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
    test: TestField,
    accumulate_dtype,
):
    def integrate_kernel_fn(
        qp_arg: quadrature.Arg,
        domain_arg: domain.ElementArg,
        domain_index_arg: domain.ElementIndexArg,
        test_arg: test.space_restriction.NodeArg,
        fields: FieldStruct,
        values: ValueStruct,
        result: wp.array2d(dtype=accumulate_dtype),
    ):
        local_node_index = wp.tid()
        node_index = test.space_restriction.node_partition_index(test_arg, local_node_index)
        element_count = test.space_restriction.node_element_count(test_arg, local_node_index)

        trial_dof_index = NULL_DOF_INDEX

        for n in range(element_count):
            node_element_index = test.space_restriction.node_element_index(test_arg, local_node_index, n)
            element_index = domain.element_index(domain_index_arg, node_element_index.domain_element_index)

            qp_point_count = quadrature.point_count(domain_arg, qp_arg, element_index)
            for k in range(qp_point_count):
                qp_index = quadrature.point_index(domain_arg, qp_arg, element_index, k)
                coords = quadrature.point_coords(domain_arg, qp_arg, element_index, k)

                qp_weight = quadrature.point_weight(domain_arg, qp_arg, element_index, k)
                vol = domain.element_measure(domain_arg, make_free_sample(element_index, coords))

                for i in range(test.space.VALUE_DOF_COUNT):
                    test_dof_index = DofIndex(node_element_index.node_index_in_element, i)
                    sample = Sample(element_index, coords, qp_index, qp_weight, test_dof_index, trial_dof_index)
                    val = integrand_func(sample, fields, values)

                    result[node_index, i] = result[node_index, i] + accumulate_dtype(qp_weight * vol * val)

    return integrate_kernel_fn


def get_integrate_linear_nodal_kernel(
    integrand_func: wp.Function,
    domain: GeometryDomain,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
    test: TestField,
    accumulate_dtype,
):
    def integrate_kernel_fn(
        domain_arg: domain.ElementArg,
        domain_index_arg: domain.ElementIndexArg,
        test_restriction_arg: test.space_restriction.NodeArg,
        fields: FieldStruct,
        values: ValueStruct,
        result: wp.array2d(dtype=accumulate_dtype),
    ):
        local_node_index, dof = wp.tid()

        node_index = test.space_restriction.node_partition_index(test_restriction_arg, local_node_index)
        element_count = test.space_restriction.node_element_count(test_restriction_arg, local_node_index)

        trial_dof_index = NULL_DOF_INDEX

        val_sum = accumulate_dtype(0.0)

        for n in range(element_count):
            node_element_index = test.space_restriction.node_element_index(test_restriction_arg, local_node_index, n)
            element_index = domain.element_index(domain_index_arg, node_element_index.domain_element_index)

            coords = test.space.node_coords_in_element(
                domain_arg,
                _get_test_arg(),
                element_index,
                node_element_index.node_index_in_element,
            )

            if coords[0] != OUTSIDE:
                node_weight = test.space.node_quadrature_weight(
                    domain_arg,
                    _get_test_arg(),
                    element_index,
                    node_element_index.node_index_in_element,
                )

                test_dof_index = DofIndex(node_element_index.node_index_in_element, dof)

                sample = Sample(
                    element_index,
                    coords,
                    node_index,
                    node_weight,
                    test_dof_index,
                    trial_dof_index,
                )
                vol = domain.element_measure(domain_arg, sample)
                val = integrand_func(sample, fields, values)

                val_sum += accumulate_dtype(node_weight * vol * val)

        result[node_index, dof] = val_sum

    return integrate_kernel_fn


def get_integrate_bilinear_kernel(
    integrand_func: wp.Function,
    domain: GeometryDomain,
    quadrature: Quadrature,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
    test: TestField,
    trial: TrialField,
    accumulate_dtype,
):
    NODES_PER_ELEMENT = trial.space.topology.NODES_PER_ELEMENT

    def integrate_kernel_fn(
        qp_arg: quadrature.Arg,
        domain_arg: domain.ElementArg,
        domain_index_arg: domain.ElementIndexArg,
        test_arg: test.space_restriction.NodeArg,
        trial_partition_arg: trial.space_partition.PartitionArg,
        trial_topology_arg: trial.space_partition.space_topology.TopologyArg,
        fields: FieldStruct,
        values: ValueStruct,
        row_offsets: wp.array(dtype=int),
        triplet_rows: wp.array(dtype=int),
        triplet_cols: wp.array(dtype=int),
        triplet_values: wp.array3d(dtype=accumulate_dtype),
    ):
        test_local_node_index = wp.tid()

        element_count = test.space_restriction.node_element_count(test_arg, test_local_node_index)
        test_node_index = test.space_restriction.node_partition_index(test_arg, test_local_node_index)

        for element in range(element_count):
            test_element_index = test.space_restriction.node_element_index(test_arg, test_local_node_index, element)
            element_index = domain.element_index(domain_index_arg, test_element_index.domain_element_index)
            qp_point_count = quadrature.point_count(domain_arg, qp_arg, element_index)

            start_offset = (row_offsets[test_node_index] + element) * NODES_PER_ELEMENT

            for k in range(qp_point_count):
                qp_index = quadrature.point_index(domain_arg, qp_arg, element_index, k)
                coords = quadrature.point_coords(domain_arg, qp_arg, element_index, k)

                qp_weight = quadrature.point_weight(domain_arg, qp_arg, element_index, k)
                vol = domain.element_measure(domain_arg, make_free_sample(element_index, coords))

                offset_cur = start_offset

                for trial_n in range(NODES_PER_ELEMENT):
                    for i in range(test.space.VALUE_DOF_COUNT):
                        for j in range(trial.space.VALUE_DOF_COUNT):
                            test_dof_index = DofIndex(
                                test_element_index.node_index_in_element,
                                i,
                            )
                            trial_dof_index = DofIndex(trial_n, j)
                            sample = Sample(
                                element_index,
                                coords,
                                qp_index,
                                qp_weight,
                                test_dof_index,
                                trial_dof_index,
                            )
                            val = integrand_func(sample, fields, values)
                            triplet_values[offset_cur, i, j] = triplet_values[offset_cur, i, j] + accumulate_dtype(
                                qp_weight * vol * val
                            )

                    offset_cur += 1

            # Set column indices
            offset_cur = start_offset
            for trial_n in range(NODES_PER_ELEMENT):
                trial_node_index = trial.space_partition.partition_node_index(
                    trial_partition_arg,
                    trial.space.topology.element_node_index(domain_arg, trial_topology_arg, element_index, trial_n),
                )

                triplet_rows[offset_cur] = test_node_index
                triplet_cols[offset_cur] = trial_node_index
                offset_cur += 1

    return integrate_kernel_fn


def get_integrate_bilinear_nodal_kernel(
    integrand_func: wp.Function,
    domain: GeometryDomain,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
    test: TestField,
    accumulate_dtype,
):
    def integrate_kernel_fn(
        domain_arg: domain.ElementArg,
        domain_index_arg: domain.ElementIndexArg,
        test_restriction_arg: test.space_restriction.NodeArg,
        fields: FieldStruct,
        values: ValueStruct,
        triplet_rows: wp.array(dtype=int),
        triplet_cols: wp.array(dtype=int),
        triplet_values: wp.array3d(dtype=accumulate_dtype),
    ):
        local_node_index, test_dof, trial_dof = wp.tid()

        element_count = test.space_restriction.node_element_count(test_restriction_arg, local_node_index)
        node_index = test.space_restriction.node_partition_index(test_restriction_arg, local_node_index)

        val_sum = accumulate_dtype(0.0)

        for n in range(element_count):
            node_element_index = test.space_restriction.node_element_index(test_restriction_arg, local_node_index, n)
            element_index = domain.element_index(domain_index_arg, node_element_index.domain_element_index)

            coords = test.space.node_coords_in_element(
                domain_arg,
                _get_test_arg(),
                element_index,
                node_element_index.node_index_in_element,
            )

            if coords[0] != OUTSIDE:
                node_weight = test.space.node_quadrature_weight(
                    domain_arg,
                    _get_test_arg(),
                    element_index,
                    node_element_index.node_index_in_element,
                )


                test_dof_index = DofIndex(node_element_index.node_index_in_element, test_dof)
                trial_dof_index = DofIndex(node_element_index.node_index_in_element, trial_dof)

                sample = Sample(
                    element_index,
                    coords,
                    node_index,
                    node_weight,
                    test_dof_index,
                    trial_dof_index,
                )
                vol = domain.element_measure(domain_arg, sample)
                val = integrand_func(sample, fields, values)

                val_sum += accumulate_dtype(node_weight * vol * val)

        triplet_values[local_node_index, test_dof, trial_dof] = val_sum
        triplet_rows[local_node_index] = node_index
        triplet_cols[local_node_index] = node_index

    return integrate_kernel_fn


def _generate_integrate_kernel(
    integrand: Integrand,
    domain: GeometryDomain,
    nodal: bool,
    quadrature: Quadrature,
    test: Optional[TestField],
    test_name: str,
    trial: Optional[TrialField],
    trial_name: str,
    fields: Dict[str, FieldLike],
    accumulate_dtype: type,
    kernel_options: Dict[str, Any] = {},
) -> wp.Kernel:
    # Extract field arguments from integrand
    field_args, value_args, domain_name, sample_name = _get_integrand_field_arguments(
        integrand, fields=fields, domain=domain
    )

    FieldStruct = _gen_field_struct(field_args)
    ValueStruct = _gen_value_struct(value_args)

    # Check if kernel exist in cache
    kernel_suffix = f"_itg_{wp.types.type_typestr(accumulate_dtype)}_{domain.name}_{FieldStruct.key}"
    if nodal:
        kernel_suffix += "_nodal"
    else:
        kernel_suffix += quadrature.name

    if test:
        kernel_suffix += f"_test_{test.space_partition.name}_{test.space.name}"
    if trial:
        kernel_suffix += f"_trial_{trial.space_partition.name}_{trial.space.name}"

    kernel = cache.get_integrand_kernel(
        integrand=integrand,
        suffix=kernel_suffix,
    )
    if kernel is not None:
        return kernel, FieldStruct, ValueStruct

    # Not found in cache, trasnform integrand and generate  kernel

    integrand_func = _translate_integrand(
        integrand,
        field_args,
    )

    _register_integrand_field_wrappers(integrand_func, fields)

    if test is None and trial is None:
        integrate_kernel_fn = get_integrate_constant_kernel(
            integrand_func,
            domain,
            quadrature,
            FieldStruct,
            ValueStruct,
            accumulate_dtype=accumulate_dtype,
        )
    elif trial is None:
        if nodal:
            integrate_kernel_fn = get_integrate_linear_nodal_kernel(
                integrand_func,
                domain,
                FieldStruct,
                ValueStruct,
                test=test,
                accumulate_dtype=accumulate_dtype,
            )
        else:
            integrate_kernel_fn = get_integrate_linear_kernel(
                integrand_func,
                domain,
                quadrature,
                FieldStruct,
                ValueStruct,
                test=test,
                accumulate_dtype=accumulate_dtype,
            )
    else:
        if nodal:
            integrate_kernel_fn = get_integrate_bilinear_nodal_kernel(
                integrand_func,
                domain,
                FieldStruct,
                ValueStruct,
                test=test,
                accumulate_dtype=accumulate_dtype,
            )
        else:
            integrate_kernel_fn = get_integrate_bilinear_kernel(
                integrand_func,
                domain,
                quadrature,
                FieldStruct,
                ValueStruct,
                test=test,
                trial=trial,
                accumulate_dtype=accumulate_dtype,
            )

    kernel = cache.get_integrand_kernel(
        integrand=integrand,
        kernel_fn=integrate_kernel_fn,
        suffix=kernel_suffix,
        kernel_options=kernel_options,
        code_transformers=[
            PassFieldArgsToIntegrand(
                arg_names=integrand.argspec.args,
                field_args=field_args.keys(),
                value_args=value_args.keys(),
                sample_name=sample_name,
                domain_name=domain_name,
                test_name=test_name,
                trial_name=trial_name,
            )
        ],
    )

    return kernel, FieldStruct, ValueStruct


def _launch_integrate_kernel(
    kernel: wp.Kernel,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
    domain: GeometryDomain,
    nodal: bool,
    quadrature: Quadrature,
    test: Optional[TestField],
    trial: Optional[TrialField],
    fields: Dict[str, FieldLike],
    values: Dict[str, Any],
    accumulate_dtype: type,
    temporary_store: Optional[cache.TemporaryStore],
    output_dtype: type,
    output: Optional[Union[wp.array, BsrMatrix]],
    device,
):
    # Set-up launch arguments
    domain_elt_arg = domain.element_arg_value(device=device)
    domain_elt_index_arg = domain.element_index_arg_value(device=device)

    if quadrature is not None:
        qp_arg = quadrature.arg_value(device=device)

    field_arg_values = FieldStruct()
    for k, v in fields.items():
        setattr(field_arg_values, k, v.eval_arg_value(device=device))

    value_struct_values = ValueStruct()
    for k, v in values.items():
        setattr(value_struct_values, k, v)

    # Constant form
    if test is None and trial is None:
        if output is not None and output.dtype == accumulate_dtype:
            if output.size < 1:
                raise RuntimeError("Output array must be of size at least 1")
            accumulate_array = output
        else:
            accumulate_temporary = cache.borrow_temporary(
                shape=(1),
                device=device,
                dtype=accumulate_dtype,
                temporary_store=temporary_store,
                requires_grad=output is not None and output.requires_grad,
            )
            accumulate_array = accumulate_temporary.array

        accumulate_array.zero_()
        wp.launch(
            kernel=kernel,
            dim=domain.element_count(),
            inputs=[
                qp_arg,
                domain_elt_arg,
                domain_elt_index_arg,
                field_arg_values,
                value_struct_values,
                accumulate_array,
            ],
            device=device,
        )

        if output == accumulate_array:
            return output
        elif output is None:
            return accumulate_array.numpy()[0]
        else:
            array_cast(in_array=accumulate_array, out_array=output)
            return output

    test_arg = test.space_restriction.node_arg(device=device)

    # Linear form
    if trial is None:
        if test.space.VALUE_DOF_COUNT == 1:
            accumulate_array_dtype = accumulate_dtype
        else:
            accumulate_array_dtype = cache.cached_vec_type(length=test.space.VALUE_DOF_COUNT, dtype=accumulate_dtype)

        if output is not None and output.size < test.space_partition.node_count():
            raise RuntimeError(f"Output array must be of size at least {test.space_partition.node_count()}")

        accumulate_in_place = wp.types.types_equal(accumulate_array_dtype, output_dtype)

        # If an output array is provided with the correct type, accumulate directly into it
        # Otherwise, grab a temporary array
        if output is not None and accumulate_in_place:
            accumulate_array = output
        else:
            accumulate_temporary = cache.borrow_temporary(
                temporary_store=temporary_store,
                shape=test.space_partition.node_count(),
                dtype=accumulate_array_dtype,
                device=device,
                requires_grad=output is not None and output.requires_grad,
            )
            accumulate_array = accumulate_temporary.array

        # Launch the integration on the kernel on a 2d scalar view of the actual array
        accumulate_array.zero_()

        def as_2d_array(array):
            return wp.array(
                data=None,
                ptr=array.ptr,
                capacity=array.capacity,
                owner=False,
                device=array.device,
                shape=(test.space_partition.node_count(), test.space.VALUE_DOF_COUNT),
                dtype=accumulate_dtype,
                grad=None if array.grad is None else as_2d_array(array.grad),
            )

        accumulate_2d_view = as_2d_array(accumulate_array)

        if nodal:
            wp.launch(
                kernel=kernel,
                dim=(test.space_restriction.node_count(), test.space.VALUE_DOF_COUNT),
                inputs=[
                    domain_elt_arg,
                    domain_elt_index_arg,
                    test_arg,
                    field_arg_values,
                    value_struct_values,
                    accumulate_2d_view,
                ],
                device=device,
            )
        else:
            wp.launch(
                kernel=kernel,
                dim=test.space_restriction.node_count(),
                inputs=[
                    qp_arg,
                    domain_elt_arg,
                    domain_elt_index_arg,
                    test_arg,
                    field_arg_values,
                    value_struct_values,
                    accumulate_2d_view,
                ],
                device=device,
            )

        # Accumulate and output dtypes are simular -- return accumulation array directly
        if output == accumulate_array:
            return output

        if accumulate_in_place:
            return accumulate_temporary.detach()

        # Different types -- need to cast result
        if output is not None:
            cast_result = output
        elif type_length(output_dtype) == test.space.VALUE_DOF_COUNT:
            cast_result = wp.empty(
                dtype=output_dtype,
                shape=accumulate_array.shape,
                device=device,
                requires_grad=accumulate_array.requires_grad,
            )
        else:
            cast_result = wp.empty(
                dtype=output_dtype,
                shape=accumulate_2d_view.shape,
                device=device,
                requires_grad=accumulate_array.requires_grad,
            )

        array_cast(in_array=accumulate_array, out_array=cast_result)
        accumulate_temporary.release()  # Do not wait for garbage collection
        return cast_result

    # Bilinear form

    if test.space.VALUE_DOF_COUNT == 1 and trial.space.VALUE_DOF_COUNT == 1:
        block_type = accumulate_dtype
    else:
        block_type = cache.cached_mat_type(
            shape=(test.space.VALUE_DOF_COUNT, trial.space.VALUE_DOF_COUNT), dtype=accumulate_dtype
        )

    if nodal:
        nnz = test.space_restriction.node_count()
    else:
        nnz = test.space_restriction.total_node_element_count() * trial.space.topology.NODES_PER_ELEMENT

    triplet_rows_temp = cache.borrow_temporary(temporary_store, shape=(nnz,), dtype=int, device=device)
    triplet_cols_temp = cache.borrow_temporary(temporary_store, shape=(nnz,), dtype=int, device=device)
    triplet_values_temp = cache.borrow_temporary(
        temporary_store,
        shape=(
            nnz,
            test.space.VALUE_DOF_COUNT,
            trial.space.VALUE_DOF_COUNT,
        ),
        dtype=accumulate_dtype,
        device=device,
    )
    triplet_cols = triplet_cols_temp.array
    triplet_rows = triplet_rows_temp.array
    triplet_values = triplet_values_temp.array

    triplet_values.zero_()

    if nodal:
        wp.launch(
            kernel=kernel,
            dim=triplet_values.shape,
            inputs=[
                domain_elt_arg,
                domain_elt_index_arg,
                test_arg,
                field_arg_values,
                value_struct_values,
                triplet_rows,
                triplet_cols,
                triplet_values,
            ],
            device=device,
        )

    else:
        offsets = test.space_restriction.partition_element_offsets()

        trial_partition_arg = trial.space_partition.partition_arg_value(device)
        trial_topology_arg = trial.space_partition.space_topology.topo_arg_value(device)
        wp.launch(
            kernel=kernel,
            dim=test.space_restriction.node_count(),
            inputs=[
                qp_arg,
                domain_elt_arg,
                domain_elt_index_arg,
                test_arg,
                trial_partition_arg,
                trial_topology_arg,
                field_arg_values,
                value_struct_values,
                offsets,
                triplet_rows,
                triplet_cols,
                triplet_values,
            ],
            device=device,
        )

    compress_in_place = accumulate_dtype == output_dtype

    if output is not None:
        if output.nrow != test.space_partition.node_count() or output.ncol != trial.space_partition.node_count():
            raise RuntimeError(
                f"Output matrix must have {test.space_partition.node_count()} rows and {trial.space_partition.node_count()} columns of blocks"
            )

    if output is not None and compress_in_place:
        bsr_matrix = output
    else:
        bsr_matrix = bsr_zeros(
            rows_of_blocks=test.space_partition.node_count(),
            cols_of_blocks=trial.space_partition.node_count(),
            block_type=block_type,
            device=device,
        )

    bsr_set_from_triplets(bsr_matrix, triplet_rows, triplet_cols, triplet_values)

    # Do not wait for garbage collection
    triplet_values_temp.release()
    triplet_rows_temp.release()
    triplet_cols_temp.release()

    if compress_in_place:
        return bsr_matrix

    if output is None:
        return bsr_copy(bsr_matrix, scalar_type=output_dtype)

    bsr_assign(src=bsr_matrix, dest=output)
    return output


def integrate(
    integrand: Integrand,
    domain: Optional[GeometryDomain] = None,
    quadrature: Optional[Quadrature] = None,
    nodal: bool = False,
    fields: Dict[str, FieldLike] = {},
    values: Dict[str, Any] = {},
    accumulate_dtype: type = wp.float64,
    output_dtype: Optional[type] = None,
    output: Optional[Union[BsrMatrix, wp.array]] = None,
    device=None,
    temporary_store: Optional[cache.TemporaryStore] = None,
    kernel_options: Dict[str, Any] = {},
):
    """
    Integrates a constant, linear or bilinear form, and returns a scalar, array, or sparse matrix, respectively.

    Args:
        integrand: Form to be integrated, must have :func:`integrand` decorator
        domain: Integration domain. If None, deduced from fields
        quadrature: Quadrature formula. If None, deduced from domain and fields degree.
        nodal: For linear or bilinear form only, use the test function nodes as the quadrature points. Assumes Lagrange interpolation functions are used, and no differential or DG operator is evaluated on the test or trial functions.
        fields: Discrete, test, and trial fields to be passed to the integrand. Keys in the dictionary must match integrand parameter names.
        values: Additional variable values to be passed to the integrand, can by of any type accepted by warp kernel launchs. Keys in the dictionary must match integrand parameter names.
        temporary_store: shared pool from which to allocate temporary arrays
        accumulate_dtype: Scalar type to be used for accumulating integration samples
        output: Sparse matrix or warp array into which to store the result of the integration
        output_dtype: Scalar type for returned results in `output` is notr provided. If None, defaults to `accumulate_dtype`
        device: Device on which to perform the integration
        kernel_options: Overloaded options to be passed to the kernel builder (e.g, ``{"enable_backward": True}``)
    """
    if not isinstance(integrand, Integrand):
        raise ValueError("integrand must be tagged with @warp.fem.integrand decorator")

    test, test_name, trial, trial_name = _get_test_and_trial_fields(fields)

    if domain is None:
        if quadrature is not None:
            domain = quadrature.domain
        elif test is not None:
            domain = test.domain

    if domain is None:
        raise ValueError("Must provide at least one of domain, quadrature, or test field")
    if test is not None and domain != test.domain:
        raise NotImplementedError("Mixing integration and test domain is not supported yet")

    if nodal:
        if quadrature is not None:
            raise ValueError("Cannot specify quadrature for nodal integration")

        if test is None:
            raise ValueError("Nodal integration requires specifying a test function")

        if trial is not None and test.space_partition != trial.space_partition:
            raise ValueError(
                "Bilinear nodal integration requires test and trial to be defined on the same function space"
            )
    else:
        if quadrature is None:
            order = sum(field.degree for field in fields.values())
            quadrature = RegularQuadrature(domain=domain, order=order)
        elif domain != quadrature.domain:
            raise ValueError("Incompatible integration and quadrature domain")

    # Canonicalize types
    accumulate_dtype = wp.types.type_to_warp(accumulate_dtype)
    if output is not None:
        if isinstance(output, BsrMatrix):
            output_dtype = output.scalar_type
        else:
            output_dtype = output.dtype
    elif output_dtype is None:
        output_dtype = accumulate_dtype
    else:
        output_dtype = wp.types.type_to_warp(output_dtype)

    kernel, FieldStruct, ValueStruct = _generate_integrate_kernel(
        integrand=integrand,
        domain=domain,
        nodal=nodal,
        quadrature=quadrature,
        test=test,
        test_name=test_name,
        trial=trial,
        trial_name=trial_name,
        fields=fields,
        accumulate_dtype=accumulate_dtype,
        kernel_options=kernel_options,
    )

    return _launch_integrate_kernel(
        kernel=kernel,
        FieldStruct=FieldStruct,
        ValueStruct=ValueStruct,
        domain=domain,
        nodal=nodal,
        quadrature=quadrature,
        test=test,
        trial=trial,
        fields=fields,
        values=values,
        accumulate_dtype=accumulate_dtype,
        temporary_store=temporary_store,
        output_dtype=output_dtype,
        output=output,
        device=device,
    )


def get_interpolate_kernel(
    integrand_func: wp.Function,
    domain: GeometryDomain,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
    dest: FieldRestriction,
):
    value_type = dest.space.dtype

    def interpolate_kernel_fn(
        domain_arg: domain.ElementArg,
        domain_index_arg: domain.ElementIndexArg,
        dest_node_arg: dest.space_restriction.NodeArg,
        dest_eval_arg: dest.field.EvalArg,
        fields: FieldStruct,
        values: ValueStruct,
    ):
        local_node_index = wp.tid()
        node_index = dest.space_restriction.node_partition_index(dest_node_arg, local_node_index)

        element_count = dest.space_restriction.node_element_count(dest_node_arg, local_node_index)
        if element_count == 0:
            return

        test_dof_index = NULL_DOF_INDEX
        trial_dof_index = NULL_DOF_INDEX
        node_weight = 1.0

        # Volume-weighted average accross elements
        # Superfluous if the function is continuous, but we might as well

        val_sum = value_type(0.0)
        vol_sum = float(0.0)

        for n in range(element_count):
            node_element_index = dest.space_restriction.node_element_index(dest_node_arg, local_node_index, n)
            element_index = domain.element_index(domain_index_arg, node_element_index.domain_element_index)

            coords = dest.space.node_coords_in_element(
                domain_arg,
                dest_eval_arg.space_arg,
                element_index,
                node_element_index.node_index_in_element,
            )

            if coords[0] != OUTSIDE:
                sample = Sample(
                    element_index,
                    coords,
                    node_index,
                    node_weight,
                    test_dof_index,
                    trial_dof_index,
                )
                vol = domain.element_measure(domain_arg, sample)
                val = integrand_func(sample, fields, values)

                vol_sum += vol
                val_sum += vol * val

        if vol_sum > 0.0:
            dest.field.set_node_value(dest_eval_arg, node_index, val_sum / vol_sum)

    return interpolate_kernel_fn


def _generate_interpolate_kernel(integrand: Integrand, dest: FieldLike, fields: Dict[str, FieldLike]) -> wp.Kernel:
    domain = dest.domain

    # Extract field arguments from integrand
    field_args, value_args, domain_name, sample_name = _get_integrand_field_arguments(
        integrand, fields=fields, domain=domain
    )

    # Generate field struct
    integrand_func = _translate_integrand(
        integrand,
        field_args,
    )

    _register_integrand_field_wrappers(integrand_func, fields)

    FieldStruct = _gen_field_struct(field_args)
    ValueStruct = _gen_value_struct(value_args)

    # Check if kernel exist in cache
    kernel_suffix = (
        f"_itp_{FieldStruct.key}_{dest.domain.name}_{dest.space_restriction.space_partition.name}_{dest.space.name}"
    )

    kernel = cache.get_integrand_kernel(
        integrand=integrand,
        suffix=kernel_suffix,
    )
    if kernel is not None:
        return kernel, FieldStruct, ValueStruct

    # Generate interpolation kernel
    interpolate_kernel_fn = get_interpolate_kernel(
        integrand_func,
        domain,
        dest=dest,
        FieldStruct=FieldStruct,
        ValueStruct=ValueStruct,
    )

    kernel = cache.get_integrand_kernel(
        integrand=integrand,
        kernel_fn=interpolate_kernel_fn,
        suffix=kernel_suffix,
        code_transformers=[
            PassFieldArgsToIntegrand(
                arg_names=integrand.argspec.args,
                field_args=field_args.keys(),
                value_args=value_args.keys(),
                sample_name=sample_name,
                domain_name=domain_name,
            )
        ],
    )

    return kernel, FieldStruct, ValueStruct


def _launch_interpolate_kernel(
    kernel: wp.kernel,
    FieldStruct: wp.codegen.Struct,
    ValueStruct: wp.codegen.Struct,
    dest: FieldLike,
    fields: Dict[str, FieldLike],
    values: Dict[str, Any],
    device,
) -> wp.Kernel:
    # Set-up launch arguments
    elt_arg = dest.domain.element_arg_value(device=device)
    elt_index_arg = dest.domain.element_index_arg_value(device=device)
    dest_node_arg = dest.space_restriction.node_arg(device=device)
    dest_eval_arg = dest.field.eval_arg_value(device=device)

    field_arg_values = FieldStruct()
    for k, v in fields.items():
        setattr(field_arg_values, k, v.eval_arg_value(device=device))

    value_struct_values = ValueStruct()
    for k, v in values.items():
        setattr(value_struct_values, k, v)

    wp.launch(
        kernel=kernel,
        dim=dest.space_restriction.node_count(),
        inputs=[
            elt_arg,
            elt_index_arg,
            dest_node_arg,
            dest_eval_arg,
            field_arg_values,
            value_struct_values,
        ],
        device=device,
    )


def interpolate(
    integrand: Integrand,
    dest: Union[DiscreteField, FieldRestriction],
    fields: Dict[str, FieldLike] = {},
    values: Dict[str, Any] = {},
    device=None,
):
    """
    Interpolates a function and assigns the result to a discrete field.

    Args:
        integrand: Function to be interpolated, must have :func:`integrand` decorator
        dest: Discrete field, or restriction of a discrete field to a domain, to which the interpolation result will be assigned
        fields: Discrete fields to be passed to the integrand. Keys in the dictionary must match integrand parameters names.
        values: Additional variable values to be passed to the integrand, can by of any type accepted by warp kernel launchs. Keys in the dictionary must match integrand parameter names.
        device: Device on which to perform the interpolation
    """
    if not isinstance(integrand, Integrand):
        raise ValueError("integrand must be tagged with @integrand decorator")

    test, _, trial, __ = _get_test_and_trial_fields(fields)
    if test is not None or trial is not None:
        raise ValueError("Test or Trial fields should not be used for interpolation")

    if not isinstance(dest, FieldRestriction):
        dest = make_restriction(dest)

    kernel, FieldStruct, ValueStruct = _generate_interpolate_kernel(
        integrand=integrand,
        dest=dest,
        fields=fields,
    )

    return _launch_interpolate_kernel(
        kernel=kernel,
        FieldStruct=FieldStruct,
        ValueStruct=ValueStruct,
        dest=dest,
        fields=fields,
        values=values,
        device=device,
    )
