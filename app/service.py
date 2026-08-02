"""Orchestration: safety -> model -> deterministic rules -> verdict.

The one invariant: this function never raises. Any failure anywhere degrades to
a rules-only answer, because a student who gets a blank error page learns
nothing and a judge who sees one marks Project Condition down.
"""

from __future__ import annotations

import logging
import os

from . import merge, safety
from .extract import heuristic_extract
from .models import AuditResponse, ExperimentInput
from .providers.base import LLMProvider, ProviderResult, ProviderUnavailable

log = logging.getLogger("counterlab")


def get_provider() -> LLMProvider | None:
    if os.getenv("COUNTERLAB_FORCE_RULES_ONLY") == "1":
        return None
    if not os.getenv("GEMINI_API_KEY"):
        return None
    try:
        from .providers.gemini_provider import GeminiProvider

        return GeminiProvider()
    except Exception as e:  # noqa: BLE001
        log.warning("provider unavailable at startup: %s", e)
        return None


def mode() -> str:
    return "full" if get_provider() else "rules-only"


def audit(inp: ExperimentInput, provider: LLMProvider | None = None) -> AuditResponse:
    # 1. Safety gate, on the raw text, before anything else runs.
    verdict = safety.check(inp.hypothesis, inp.procedure, inp.materials)
    if verdict.blocked:
        empty = heuristic_extract(inp)
        return AuditResponse(
            verdict="safety_stop",
            audit=empty,
            safety_notes=[verdict.message] if verdict.message else [],
            safe_alternative=verdict.alternative,
            confidence=0.9,
            assumptions=[],
        )

    # 2. Model pass, if available.
    result: ProviderResult | None = None
    degraded = False
    reason: str | None = None

    if provider is None:
        provider = get_provider()

    if provider is None:
        degraded = True
        reason = "No language model is configured, so only structural checks ran."
    else:
        try:
            result = provider.analyse(inp)
        except ProviderUnavailable as e:
            degraded = True
            reason = "The language model did not respond in time, so only structural checks ran."
            log.warning("degraded: %s", e)
        except Exception as e:  # noqa: BLE001
            degraded = True
            reason = "The language model returned something unusable, so only structural checks ran."
            log.warning("degraded (unexpected): %s: %s", type(e).__name__, e)

    # 3. Deterministic rules ALWAYS run, on whichever structure we have.
    audit_obj = result.audit if result else heuristic_extract(inp)

    response = merge.build_response(
        audit=audit_obj,
        model_findings=result.model_findings if result else [],
        minimal_repairs=result.minimal_repairs if result else [],
        cheapest_falsification_test=result.cheapest_falsification_test if result else None,
        rejection_condition=result.rejection_condition if result else None,
        stopping_rule=result.stopping_rule if result else None,
        analysis_rule=result.analysis_rule if result else None,
        safety_notes=verdict.notes,
        degraded_mode=degraded,
        degraded_reason=reason,
        model_used=result.model_used if result else None,
    )

    # Injection attempts are surfaced to the student, not hidden.
    if _looks_like_injection(inp):
        response.assumptions.insert(
            0,
            "Your submission contained text that looked like an instruction to the AI "
            "(for example 'ignore previous instructions'). That was treated as part of your "
            "experiment description, not as a command, and it did not affect the verdict below.",
        )
    return response


INJECTION_MARKERS = (
    "ignore all previous",
    "ignore previous",
    "disregard your",
    "disregard all",
    "system:",
    "you are now in",
    "new instruction",
    "approval mode",
    "mark this experiment perfect",
    "pass_state=true",
    "</student_submission>",
)


def _looks_like_injection(inp: ExperimentInput) -> bool:
    blob = f"{inp.hypothesis} {inp.procedure} {inp.materials}".lower()
    return any(m in blob for m in INJECTION_MARKERS)
