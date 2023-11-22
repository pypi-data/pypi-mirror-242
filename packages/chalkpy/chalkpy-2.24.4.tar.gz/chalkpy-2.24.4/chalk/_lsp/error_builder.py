from __future__ import annotations

import ast
from collections import defaultdict
from typing import List, Mapping, Union

from chalk._lsp.finders import (
    get_annotation_range,
    get_class_definition_range,
    get_decorator_kwarg_value_range,
    get_property_range,
    get_property_value_range,
)
from chalk.parsed.duplicate_input_gql import (
    CodeActionGQL,
    CodeDescriptionGQL,
    DiagnosticGQL,
    DiagnosticSeverityGQL,
    PositionGQL,
    RangeGQL,
    TextDocumentEditGQL,
    TextDocumentIdentifierGQL,
    TextEditGQL,
    WorkspaceEditGQL,
)


class LSPErrorBuilder:
    lsp: bool = False
    all_errors: Mapping[str, list[DiagnosticGQL]] = defaultdict(list)
    all_edits: list[CodeActionGQL] = []


class FeatureClassErrorBuilder:
    def __init__(
        self,
        filename: str,
        namespace: str,
        node: ast.ClassDef | None,
    ):
        self.filename = filename
        self.diagnostics: List[DiagnosticGQL] = []
        self.namespace = namespace
        self.node: ast.ClassDef | None = node

    def _add(
        self,
        r: RangeGQL,
        message: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> None:
        # if not LSPErrorBuilder.lsp:
        #     raise TypeError(code)

        err = DiagnosticGQL(
            range=r,
            message=message,
            severity=severity,
            code=code,
            codeDescription=CodeDescriptionGQL(href=code_href) if code_href is not None else None,
        )
        self.diagnostics.append(err)
        LSPErrorBuilder.all_errors[self.filename].append(err)

    def add_decorator_kwarg_value_error(
        self,
        kwarg: str,
        message: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: str | None = None,
    ) -> bool:
        if self.node is None:
            return False

        r = get_decorator_kwarg_value_range(
            cls=self.node,
            kwarg=kwarg,
        )
        if r is None:
            return False
        self._add(
            r=r,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )

    def add_class_error(
        self,
        message: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: str | None = None,
    ):
        if self.node is None:
            return

        r = get_class_definition_range(
            cls=self.node,
            filename=self.filename,
        )
        self._add(
            r=r,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )

    def add_property_error(
        self,
        feature_name: str,
        message: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> bool:
        if self.node is None:
            return False

        r = get_property_range(cls=self.node, name=feature_name)
        if r is None:
            return False

        self._add(
            r=r,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )
        return True

    def add_annotation_error(
        self,
        feature_name: str,
        message: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> bool:
        if self.node is None:
            return False

        r = get_annotation_range(cls=self.node, name=feature_name)
        if r is None:
            return False

        self._add(
            r=r,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )
        return True

    def remove_feature_action(
        self,
        feature_name: str,
        title: str,
    ):
        if self.node is None:
            return False

        start_range = get_property_range(cls=self.node, name=feature_name)
        if start_range is None:
            return False

        end_range = get_property_value_range(cls=self.node, name=feature_name) or get_annotation_range(
            cls=self.node, name=feature_name
        )
        if end_range is not None:
            start_range.end = end_range.end

        LSPErrorBuilder.all_edits.append(
            CodeActionGQL(
                title=title,
                diagnostics=None,
                edit=WorkspaceEditGQL(
                    documentChanges=[
                        TextDocumentEditGQL(
                            textDocument=TextDocumentIdentifierGQL(uri=self.filename),
                            edits=[
                                TextEditGQL(
                                    range=start_range,
                                    newText="",
                                )
                            ],
                        )
                    ]
                ),
            )
        )

    def add_property_value_error(
        self,
        feature_name: str,
        message: str,
        code: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code_href: Union[str, None] = None,
    ) -> bool:
        if self.node is None:
            return False

        r = get_property_value_range(cls=self.node, name=feature_name)
        if r is None:
            return False

        self._add(
            r=r,
            message=message,
            severity=severity,
            code=code,
            code_href=code_href,
        )
        return True
