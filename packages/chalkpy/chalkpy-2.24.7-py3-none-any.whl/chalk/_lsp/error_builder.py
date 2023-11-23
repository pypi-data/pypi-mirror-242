from __future__ import annotations

import ast
from collections import defaultdict
from typing import List, Mapping, Type, Union

from chalk._lsp.finders import (
    get_annotation_range,
    get_class_definition_range,
    get_decorator_kwarg_value_range,
    get_function_return_annotation,
    get_property_range,
    get_property_value_call_range,
    get_property_value_range,
    node_to_range,
)
from chalk.parsed.duplicate_input_gql import (
    CodeActionGQL,
    CodeDescriptionGQL,
    DiagnosticGQL,
    DiagnosticRelatedInformationGQL,
    DiagnosticSeverityGQL,
    LocationGQL,
    RangeGQL,
    TextDocumentEditGQL,
    TextDocumentIdentifierGQL,
    TextEditGQL,
    WorkspaceEditGQL,
)


class DiagnosticBuilder:
    def __init__(
        self,
        severity: DiagnosticSeverityGQL,
        message: str,
        uri: str,
        range: RangeGQL,
        label: str,
        code: str,
        code_href: str | None,
    ):
        self.uri = uri
        self.diagnostic = DiagnosticGQL(
            range=range,
            message=message,
            severity=severity,
            code=code,
            codeDescription=CodeDescriptionGQL(href=code_href) if code_href is not None else None,
            relatedInformation=[
                DiagnosticRelatedInformationGQL(
                    location=LocationGQL(uri=uri, range=range),
                    message=label,
                )
            ],
        )

    def with_range(
        self,
        range: RangeGQL,
        label: str,
    ) -> DiagnosticBuilder:
        self.diagnostic.relatedInformation.append(
            DiagnosticRelatedInformationGQL(
                location=LocationGQL(
                    uri=self.uri,
                    range=range,
                ),
                message=label,
            )
        )
        return self


class LSPErrorBuilder:
    lsp: bool = False
    all_errors: Mapping[str, list[DiagnosticGQL]] = defaultdict(list)
    all_edits: list[CodeActionGQL] = []


class FeatureClassErrorBuilder:
    def __init__(
        self,
        uri: str,
        namespace: str,
        node: ast.ClassDef | None,
    ):
        self.uri = uri
        self.diagnostics: List[DiagnosticGQL] = []
        self.namespace = namespace
        self.node: ast.ClassDef | None = node

    def property_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_range(cls=self.node, name=feature_name)

    def annotation_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_annotation_range(cls=self.node, name=feature_name)

    def property_value_range(self, feature_name: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_value_range(cls=self.node, name=feature_name)

    def property_value_kwarg_range(self, feature_name: str, kwarg: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_property_value_call_range(cls=self.node, name=feature_name, kwarg=kwarg)

    def decorator_kwarg_value_range(self, kwarg: str) -> ast.AST | None:
        if self.node is None:
            return None

        return get_decorator_kwarg_value_range(cls=self.node, kwarg=kwarg)

    def class_definition_range(self) -> RangeGQL | None:
        if self.node is None:
            return None

        return get_class_definition_range(cls=self.node, filename=self.uri)

    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
    ) -> DiagnosticBuilder:
        if isinstance(range, ast.AST):
            range = node_to_range(range)

        builder = DiagnosticBuilder(
            severity=severity,
            message=message,
            uri=self.uri,
            range=range,
            label=label,
            code=code,
            code_href=code_href,
        )
        if range is not None:
            # TODO: Raise in here if we don't have the range.
            self.diagnostics.append(builder.diagnostic)
            LSPErrorBuilder.all_errors[self.uri].append(builder.diagnostic)
        if raise_error is not None:
            raise raise_error(message)
        return builder


class ResolverErrorBuilder:
    def __init__(
        self,
        uri: str,
        node: ast.FunctionDef | None,
    ):
        self.uri = uri
        self.diagnostics: List[DiagnosticGQL] = []
        self.node: ast.FunctionDef | None = node

    def add_diagnostic(
        self,
        message: str,
        label: str,
        code: str,
        range: RangeGQL | ast.AST | None,
        code_href: str | None = None,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        raise_error: Type[Exception] | None = None,
    ) -> DiagnosticBuilder:
        if isinstance(range, ast.AST):
            range = node_to_range(range)
        builder = DiagnosticBuilder(
            severity=severity,
            message=message,
            uri=self.uri,
            range=range,
            label=label,
            code=code,
            code_href=code_href,
        )
        if range is not None:
            # TODO: Raise in here if we don't have the range.
            self.diagnostics.append(builder.diagnostic)
            LSPErrorBuilder.all_errors[self.uri].append(builder.diagnostic)
        if raise_error is not None:
            raise raise_error(message)
        return builder

    def return_annotation(self) -> ast.AST | None:
        if self.node is None:
            return None

        return get_function_return_annotation(self.node)
