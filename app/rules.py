"""Deterministic experimental-design checks.

These run on the TYPED FIELDS of an ExperimentAudit - never on raw prose, and
never by keyword matching on content words. Each rule is a structural predicate
over extracted data, which is why it can be trusted and unit-tested.

This module makes NO network calls. It is the reason CounterLab still works when
the language model is unavailable.
"""

from __future__ import annotations

from .models import ExperimentAudit, Finding

# Fatal rules in priority order. The first one that fires becomes THE fatal flaw.
FATAL_PRIORITY = ["R1_MULTI_VAR", "R8_IV_IN_CONTROLLED", "R2_NO_DV", "R3_NO_IV"]

MIN_TRIALS = 3


def _blank(value: str | None) -> bool:
    return value is None or not value.strip()


def _norm(value: str) -> str:
    return value.strip().lower()


def run_rules(audit: ExperimentAudit) -> list[Finding]:
    """Return every structural finding, unranked."""
    found: list[Finding] = []

    # R1 - more than one thing differs between the conditions being compared.
    # The single most common design error in the literature.
    if len(audit.variables_changed) > 1:
        changed = ", ".join(audit.variables_changed)
        found.append(
            Finding(
                id="R1_MULTI_VAR",
                title=f"You changed more than one thing at once: {changed}.",
                severity="fatal",
                reason=(
                    "When two things differ between your setups, any difference you measure "
                    "could have been caused by either one. There is no way to tell them apart "
                    "afterwards, so the result cannot answer your question no matter how "
                    "carefully you measure."
                ),
                source="deterministic",
                evidence_field="variables_changed",
            )
        )

    # R2 - nothing measurable to record.
    if _blank(audit.dependent_variable):
        found.append(
            Finding(
                id="R2_NO_DV",
                title="There is no measurable outcome in this plan.",
                severity="fatal",
                reason=(
                    "You have not said what you will actually measure and write down. Without a "
                    "number or an observation you can record the same way every time, there is "
                    "nothing to compare between your setups."
                ),
                source="deterministic",
                evidence_field="dependent_variable",
            )
        )

    # R3 - nothing deliberately varied.
    if _blank(audit.independent_variable):
        found.append(
            Finding(
                id="R3_NO_IV",
                title="There is nothing you deliberately change in this plan.",
                severity="fatal",
                reason=(
                    "An experiment needs one thing you change on purpose. Without it you are "
                    "observing, not experimenting, and you cannot say what caused what."
                ),
                source="deterministic",
                evidence_field="independent_variable",
            )
        )

    # R8 - the thing being varied is also listed as held constant.
    if not _blank(audit.independent_variable):
        iv = _norm(audit.independent_variable)
        if any(_norm(c) == iv for c in audit.controlled_variables):
            found.append(
                Finding(
                    id="R8_IV_IN_CONTROLLED",
                    title=f"'{audit.independent_variable}' is listed as both changed and held constant.",
                    severity="fatal",
                    reason=(
                        "The plan contradicts itself. If this is held constant it cannot be the "
                        "thing you are testing, and if it is the thing you are testing it cannot "
                        "be held constant. One of the two has to go."
                    ),
                    source="deterministic",
                    evidence_field="controlled_variables",
                )
            )

    # R4 - a quantitative measurement with no unit.
    if not _blank(audit.dependent_variable) and _blank(audit.measurement_unit):
        found.append(
            Finding(
                id="R4_NO_UNIT",
                title="Your measurement has no unit.",
                severity="major",
                reason=(
                    "A number without a unit cannot be compared or checked by anyone else. "
                    "Decide now whether you are recording seconds, centimetres, grams, or counts."
                ),
                source="deterministic",
                evidence_field="measurement_unit",
            )
        )

    # R5 / R6 - repetition.
    if audit.planned_repetitions is not None and audit.planned_repetitions > 0:
        if audit.planned_repetitions < MIN_TRIALS:
            found.append(
                Finding(
                    id="R5_SINGLE_TRIAL",
                    title=f"You only planned {audit.planned_repetitions} trial(s) per setup.",
                    severity="major",
                    reason=(
                        "Every measurement wobbles a little. With fewer than three trials you "
                        "cannot tell whether a difference you see is real or just the wobble, "
                        "so you cannot honestly claim the change caused it."
                    ),
                    source="deterministic",
                    evidence_field="planned_repetitions",
                )
            )
    else:
        found.append(
            Finding(
                id="R6_NO_REPS_STATED",
                title="You have not said how many times you will repeat each setup.",
                severity="major",
                reason=(
                    "Decide the number of trials before you start. Choosing afterwards - stopping "
                    "once the numbers look good - is how people accidentally fool themselves."
                ),
                source="deterministic",
                evidence_field="planned_repetitions",
            )
        )

    # R7 - something varies but nothing is being held constant.
    if audit.variables_changed and not audit.controlled_variables:
        found.append(
            Finding(
                id="R7_NO_CONTROL",
                title="Nothing is being deliberately held constant.",
                severity="major",
                reason=(
                    "If you have not decided what to keep the same, differences can creep in "
                    "without you noticing and quietly become the real cause of your result."
                ),
                source="deterministic",
                evidence_field="controlled_variables",
            )
        )

    # R9 - no stated method of measuring.
    if _blank(audit.measurement_method):
        found.append(
            Finding(
                id="R9_NO_MEASUREMENT",
                title="You have not said how you will take the measurement.",
                severity="major",
                reason=(
                    "Two people following this plan would measure differently, so the results "
                    "would not be comparable. Write down the exact procedure - what tool, from "
                    "where, at what moment."
                ),
                source="deterministic",
                evidence_field="measurement_method",
            )
        )

    return found


def pick_fatal(findings: list[Finding]) -> Finding | None:
    """Choose exactly ONE fatal flaw, by fixed priority. Deterministic rules win."""
    by_id = {f.id: f for f in findings if f.severity == "fatal"}
    for rule_id in FATAL_PRIORITY:
        if rule_id in by_id:
            return by_id[rule_id]
    for f in findings:
        if f.severity == "fatal":
            return f
    return None
