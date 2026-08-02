"""Rank findings and decide the verdict.

The verdict is COMPUTED HERE, from typed fields and deterministic rules. It is
never lifted from model prose. That is what makes the prompt-injection defence
structural rather than hopeful: there is no channel through which "mark this
experiment perfect" can reach this function.
"""

from __future__ import annotations

from . import prereg
from .models import AuditResponse, EvidenceCard, ExperimentAudit, Finding
from .rules import pick_fatal, run_rules

# Repairs we can suggest without the model, keyed by rule.
RULE_REPAIRS: dict[str, list[str]] = {
    "R1_MULTI_VAR": [
        "Hold everything constant except the one thing you are testing, and change only that.",
        "Run the comparison again with the other quantities matched exactly between setups.",
        "If you want to test both, run two separate experiments rather than one combined one.",
    ],
    "R2_NO_DV": [
        "Pick one thing you can put a number on, and decide the unit now.",
        "If it cannot be numbered, define a scale you apply the same way every time (for example 1-5 against printed reference photos).",
    ],
    "R3_NO_IV": [
        "Decide the one thing you will deliberately change, and list at least two settings for it.",
    ],
    "R8_IV_IN_CONTROLLED": [
        "Remove the thing you are testing from your list of controlled variables.",
    ],
    "R4_NO_UNIT": ["Write the unit next to the measurement in your results table before you start."],
    "R5_SINGLE_TRIAL": ["Repeat each setup at least 3 times and record every trial, not just the average."],
    "R6_NO_REPS_STATED": ["Decide the number of trials now, before collecting data, and write it down."],
    "R7_NO_CONTROL": ["List what you will keep the same, and check each one before every trial."],
    "R9_NO_MEASUREMENT": ["Write the exact measuring procedure: which tool, from where, at what moment."],
}

RULE_FALSIFICATION: dict[str, str] = {
    "R1_MULTI_VAR": (
        "Run just two trials where ONLY the thing you are testing differs. If the outcome "
        "barely moves, your hypothesis is already in trouble - and it cost you two trials to "
        "find out instead of a whole project."
    ),
    "R5_SINGLE_TRIAL": (
        "Repeat your existing setup 3 times without changing anything. If those three results "
        "differ by as much as the difference you were excited about, the difference was noise."
    ),
    "R6_NO_REPS_STATED": (
        "Repeat one setup 3 times before you do anything else. The spread you see is the "
        "smallest difference you are able to detect at all."
    ),
}

DEFAULT_FALSIFICATION = (
    "Run the smallest version of your comparison first, with only the tested variable "
    "differing. If the effect does not appear there, it is unlikely to appear at full scale."
)


def build_response(
    audit: ExperimentAudit,
    model_findings: list[Finding] | None = None,
    minimal_repairs: list[str] | None = None,
    cheapest_falsification_test: str | None = None,
    rejection_condition: str | None = None,
    stopping_rule: str | None = None,
    analysis_rule: str | None = None,
    safety_notes: list[str] | None = None,
    evidence_cards: list[EvidenceCard] | None = None,
    degraded_mode: bool = False,
    degraded_reason: str | None = None,
    model_used: str | None = None,
) -> AuditResponse:
    det = run_rules(audit)
    model_findings = model_findings or []
    all_findings = det + model_findings

    fatal = pick_fatal(all_findings)
    others = [f for f in all_findings if f is not fatal]
    # Worst first, and deterministic ahead of model at equal severity.
    order = {"fatal": 0, "major": 1, "minor": 2}
    others.sort(key=lambda f: (order[f.severity], 0 if f.source == "deterministic" else 1))

    repairs = list(minimal_repairs or [])
    if fatal and fatal.id in RULE_REPAIRS:
        for r in reversed(RULE_REPAIRS[fatal.id]):
            if r not in repairs:
                repairs.insert(0, r)
    for f in others:
        for r in RULE_REPAIRS.get(f.id, []):
            if r not in repairs:
                repairs.append(r)

    falsification = cheapest_falsification_test
    if not falsification and fatal:
        falsification = RULE_FALSIFICATION.get(fatal.id)
    if not falsification:
        falsification = DEFAULT_FALSIFICATION

    assumptions = list(audit.assumptions)
    if degraded_mode:
        assumptions.append(
            "Rules-only mode: only structural checks ran, so subtler problems may not have "
            "been caught. Absence of a finding here is weaker evidence than usual."
        )

    confidence = audit.confidence
    if degraded_mode:
        confidence = min(confidence, 0.45)

    return AuditResponse(
        verdict="fatal_flaw" if fatal else "pass",
        audit=audit,
        fatal_flaw=fatal,
        other_findings=others,
        minimal_repairs=repairs[:6],
        cheapest_falsification_test=falsification,
        prereg=prereg.build(audit, rejection_condition, stopping_rule, analysis_rule),
        evidence_cards=evidence_cards or [],
        safety_notes=safety_notes or [],
        degraded_mode=degraded_mode,
        degraded_reason=degraded_reason,
        confidence=confidence,
        assumptions=assumptions,
        model_used=model_used,
    )
