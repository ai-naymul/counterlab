"""Deterministic fake provider.

Used by the test suite and by local development without a key. Because it never
touches the network, the whole suite runs green with GEMINI_API_KEY unset - which
is the acceptance gate for "the deterministic layer is real".
"""

from __future__ import annotations

from ..extract import heuristic_extract
from ..models import ExperimentInput, Finding
from .base import LLMProvider, ProviderResult, ProviderUnavailable


class FixtureProvider(LLMProvider):
    name = "fixture"

    def __init__(self, fail_with: Exception | None = None, findings: list[Finding] | None = None) -> None:
        self.fail_with = fail_with
        self.findings = findings or []

    def analyse(self, inp: ExperimentInput) -> ProviderResult:
        if self.fail_with:
            raise self.fail_with
        audit = heuristic_extract(inp)
        audit.confidence = 0.8
        return ProviderResult(
            audit=audit,
            model_findings=self.findings,
            minimal_repairs=[],
            model_used="fixture",
        )


class BrokenProvider(LLMProvider):
    """Always unavailable - drives the degraded-mode tests."""

    name = "broken"

    def analyse(self, inp: ExperimentInput) -> ProviderResult:
        raise ProviderUnavailable("simulated provider failure")
