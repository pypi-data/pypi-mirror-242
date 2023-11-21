from __future__ import annotations

import ast
import dataclasses
from typing import List, Union

from chalk.parsed.duplicate_input_gql import PositionGQL, RangeGQL


def get_property_range(cls: ast.ClassDef, name: str) -> Union[RangeGQL, None]:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            return RangeGQL(
                start=PositionGQL(
                    line=stmt.target.lineno,
                    character=stmt.target.col_offset,
                ),
                end=PositionGQL(
                    line=stmt.target.end_lineno,
                    character=stmt.target.end_col_offset,
                ),
            )

        elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return RangeGQL(
                    start=PositionGQL(
                        line=target.lineno,
                        character=target.col_offset,
                    ),
                    end=PositionGQL(
                        line=target.end_lineno,
                        character=target.end_col_offset,
                    ),
                )

    return None


def get_property_value_range(cls: ast.ClassDef, name: str) -> Union[RangeGQL, None]:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            if stmt.value is None:
                return None

            return RangeGQL(
                start=PositionGQL(
                    line=stmt.value.lineno,
                    character=stmt.value.col_offset,
                ),
                end=PositionGQL(
                    line=stmt.value.end_lineno,
                    character=stmt.value.end_col_offset,
                ),
            )

        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return RangeGQL(
                    start=PositionGQL(
                        line=stmt.value.lineno,
                        character=stmt.value.col_offset,
                    ),
                    end=PositionGQL(
                        line=stmt.value.end_lineno,
                        character=stmt.value.end_col_offset,
                    ),
                )

    return None


def get_annotation_range(cls: ast.ClassDef, name: str) -> Union[RangeGQL, None]:
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.target.id == name:
            return RangeGQL(
                start=PositionGQL(
                    line=stmt.annotation.lineno,
                    character=stmt.annotation.col_offset,
                ),
                end=PositionGQL(
                    line=stmt.annotation.end_lineno,
                    character=stmt.annotation.end_col_offset,
                ),
            )

    return None


@dataclasses.dataclass
class ResolverRanges:
    decorator: Union[RangeGQL, None]
    arg_values: List[Union[RangeGQL, None]]
    arg_annotations: List[Union[RangeGQL, None]]
    return_annotation: Union[RangeGQL, None]
    return_statement: Union[RangeGQL, None]


_RESOLVER_DECORATORS = {"online", "offline", "realtime", "batch", "stream", "sink"}


def get_resolver_ranges(node: ast.FunctionDef) -> ResolverRanges:
    decorator = None
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id in _RESOLVER_DECORATORS:
            decorator = RangeGQL(
                start=PositionGQL(
                    line=decorator.lineno,
                    character=decorator.col_offset,
                ),
                end=PositionGQL(
                    line=decorator.end_lineno,
                    character=decorator.end_col_offset,
                ),
            )
            break
    arg_values = []
    arg_annotations = []
    for stmt in node.args.args:
        if isinstance(stmt, ast.arg):
            arg_value = RangeGQL(
                start=PositionGQL(
                    line=stmt.lineno,
                    character=stmt.col_offset,
                ),
                end=PositionGQL(
                    line=stmt.end_lineno,
                    character=stmt.end_col_offset,
                ),
            )
            if stmt.annotation is not None:
                arg_annotation = RangeGQL(
                    start=PositionGQL(
                        line=stmt.annotation.lineno,
                        character=stmt.annotation.col_offset,
                    ),
                    end=PositionGQL(
                        line=stmt.annotation.end_lineno,
                        character=stmt.annotation.end_col_offset,
                    ),
                )
            else:
                arg_annotation = None
            arg_values.append(arg_value)
            arg_annotations.append(arg_annotation)
    return_statement = None
    for stmt in node.body:
        if isinstance(stmt, ast.Return):
            return_statement = RangeGQL(
                start=PositionGQL(
                    line=stmt.lineno,
                    character=stmt.col_offset,
                ),
                end=PositionGQL(
                    line=stmt.end_lineno,
                    character=stmt.end_col_offset,
                ),
            )
    return_annotation = None
    if node.returns is not None:
        return_annotation = RangeGQL(
            start=PositionGQL(
                line=node.returns.lineno,
                character=node.returns.col_offset,
            ),
            end=PositionGQL(
                line=node.returns.end_lineno,
                character=node.returns.end_col_offset,
            ),
        )
    return ResolverRanges(
        decorator=decorator,
        arg_values=arg_values if len(arg_values) > 0 else None,
        arg_annotations=arg_annotations if len(arg_annotations) > 0 else None,
        return_statement=return_statement,
        return_annotation=return_annotation,
    )
