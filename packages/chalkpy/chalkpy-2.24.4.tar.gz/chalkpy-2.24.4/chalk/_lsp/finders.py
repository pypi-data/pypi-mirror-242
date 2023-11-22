from __future__ import annotations

import ast
from typing import Callable, List, Union

from chalk._lsp._class_finder import get_function_ast
from chalk.parsed.duplicate_input_gql import PositionGQL, RangeGQL


def get_class_definition_range(cls: ast.ClassDef, filename: str) -> RangeGQL:
    with open(filename) as f:
        lines = f.readlines()

    line_length = len(lines[cls.lineno - 1]) if cls.lineno < len(lines) else len("class ") + len(cls.name)
    return RangeGQL(
        start=PositionGQL(
            line=cls.lineno,
            character=0,
        ),
        end=PositionGQL(
            line=cls.lineno,
            character=max(line_length - 1, 1),
        ),
    )


def get_decorator_kwarg_value_range(cls: ast.ClassDef, kwarg: str) -> Union[RangeGQL, None]:
    for stmt in cls.decorator_list:
        if isinstance(stmt, ast.Call):
            for keyword in stmt.keywords:
                if keyword.arg == kwarg:
                    return RangeGQL(
                        start=PositionGQL(
                            line=keyword.value.lineno,
                            character=keyword.value.col_offset,
                        ),
                        end=PositionGQL(
                            line=keyword.value.end_lineno,
                            character=keyword.value.end_col_offset,
                        ),
                    )
    return None


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


_RESOLVER_DECORATORS = {"online", "offline", "realtime", "batch", "stream", "sink"}


def get_function_decorator_range(node: ast.FunctionDef) -> Union[RangeGQL, None]:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id in _RESOLVER_DECORATORS:
            return RangeGQL(
                start=PositionGQL(
                    line=decorator.lineno,
                    character=decorator.col_offset,
                ),
                end=PositionGQL(
                    line=decorator.end_lineno,
                    character=decorator.end_col_offset,
                ),
            )
    return None


def get_function_arg_values(node: ast.FunctionDef) -> List[Union[RangeGQL, None]]:
    arg_values = []
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
        else:
            arg_value = None
        arg_values.append(arg_value)
    return arg_values


def get_function_arg_annotations(node: ast.FunctionDef) -> List[Union[RangeGQL, None]]:
    arg_annotations = []
    for stmt in node.args.args:
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
        arg_annotations.append(arg_annotation)
    return arg_annotations


def get_function_return_annotation(node: ast.FunctionDef) -> Union[RangeGQL, None]:
    if node.returns is not None:
        return RangeGQL(
            start=PositionGQL(
                line=node.returns.lineno,
                character=node.returns.col_offset,
            ),
            end=PositionGQL(
                line=node.returns.end_lineno,
                character=node.returns.end_col_offset,
            ),
        )
    return None


def get_function_return_statement(node: ast.FunctionDef) -> RangeGQL | None:
    for stmt in node.body:
        if isinstance(stmt, ast.Return):
            return RangeGQL(
                start=PositionGQL(
                    line=stmt.lineno,
                    character=stmt.col_offset,
                ),
                end=PositionGQL(
                    line=stmt.end_lineno,
                    character=stmt.end_col_offset,
                ),
            )
    return None
