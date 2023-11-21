from __future__ import annotations

import ast
from typing import List, Union

from chalk._lsp.finders import get_annotation_range, get_property_range, get_property_value_range
from chalk.parsed.duplicate_input_gql import (
    CodeDescriptionGQL,
    DiagnosticGQL,
    DiagnosticSeverityGQL,
    PositionGQL,
    RangeGQL,
)


class LSPErrorBuilder:
    lsp: bool = False


class FeatureClassErrorBuilder:
    def __init__(self, namespace: str, node: Union[ast.ClassDef, None]):
        self.diagnostics: List[DiagnosticGQL] = []  # DiagnosticGQL not hashable
        self.namespace = namespace
        self.node = node

    def _add(
        self,
        r: RangeGQL,
        message: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code: Union[str, None] = None,
        code_href: Union[str, None] = None,
    ) -> None:
        self.diagnostics.append(
            DiagnosticGQL(
                range=r,
                message=message,
                severity=severity,
                code=code,
                codeDescription=CodeDescriptionGQL(href=code_href) if code_href is not None else None,
            )
        )

    def add_property_error(
        self,
        feature_name: str,
        message: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code: Union[str, None] = None,
        code_href: Union[str, None] = None,
    ) -> bool:
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
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code: Union[str, None] = None,
        code_href: Union[str, None] = None,
    ) -> bool:
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

    def add_property_value_error(
        self,
        feature_name: str,
        message: str,
        severity: DiagnosticSeverityGQL = DiagnosticSeverityGQL.Error,
        code: Union[str, None] = None,
        code_href: Union[str, None] = None,
    ) -> bool:
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
