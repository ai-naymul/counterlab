"""Provider boundary.

Everything above this line is provider-agnostic. Swapping Gemini for another
model is a new class implementing this protocol, not a rewrite.
"""

from __future__ import annotations

from typing import Protocol

from ..models import ExperimentAudit, ExperimentInput, Finding


class ProviderResult:
    def __init__(
        self,
        audit: ExperimentAudit,
        model_findings: list[Finding] | None = None,
        minimal_repairs: list[str] | None = None,
        cheapest_falsification_test: str | None = None,
        rejection_condition: str | None = None,
        stopping_rule: str | None = None,
        analysis_rule: str | None = None,
        model_used: str | None = None,
    ) -> None:
        self.audit = audit
        self.model_findings = model_findings or []
        self.minimal_repairs = minimal_repairs or []
        self.cheapest_falsification_test = cheapest_falsification_test
        self.rejection_condition = rejection_condition
        self.stopping_rule = stopping_rule
        self.analysis_rule = analysis_rule
        self.model_used = model_used


class ProviderUnavailable(Exception):
    """Raised when the provider cannot produce a validated result.

    Callers must treat this as 'degrade', never as 'fail the request'.
    """


class LLMProvider(Protocol):
    name: str

    def analyse(self, inp: ExperimentInput) -> ProviderResult: ...
