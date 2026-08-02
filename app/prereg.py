"""Pre-registration card.

Written BEFORE data exists. The point is the rejection condition: committing in
advance to what result would count as being wrong is the single cheapest defence
against talking yourself into a conclusion afterwards.
"""

from __future__ import annotations

from .models import ExperimentAudit, PreRegCard
from .rules import MIN_TRIALS


def build(
    audit: ExperimentAudit,
    rejection_condition: str | None = None,
    stopping_rule: str | None = None,
    analysis_rule: str | None = None,
) -> PreRegCard:
    dv = (audit.dependent_variable or "your outcome").strip()
    iv = (audit.independent_variable or "the thing you change").strip()
    unit = (audit.measurement_unit or "").strip()

    if unit:
        measurement = f"Measure {dv} in {unit}"
    else:
        measurement = f"Measure {dv} (decide the unit before you start)"
    if audit.measurement_method:
        measurement += f", by: {audit.measurement_method.strip()}"
    measurement += "."

    reps = audit.planned_repetitions if (audit.planned_repetitions or 0) > 0 else None
    planned = reps if reps and reps >= MIN_TRIALS else MIN_TRIALS

    return PreRegCard(
        measurement_plan=measurement,
        planned_repetitions=planned,
        stopping_rule=(
            stopping_rule
            or f"Run exactly {planned} trials per setting of {iv}, then stop. "
            f"Do not add trials because the result looks unconvincing, and do not stop early "
            f"because it already looks convincing."
        ),
        analysis_rule=(
            analysis_rule
            or f"Compare the average {dv} across settings of {iv}, and also write down the "
            f"highest and lowest value in each group. If the groups overlap, the difference "
            f"is not clear enough to claim."
        ),
        rejection_condition=(
            rejection_condition
            or f"I will reject my hypothesis if the average {dv} does not change in the "
            f"direction I predicted when I change {iv}, or if the spread within each group "
            f"is larger than the difference between groups."
        ),
    )


def as_text(card: PreRegCard) -> str:
    return (
        "COUNTERLAB PRE-REGISTRATION CARD\n"
        "Written before any data was collected.\n"
        f"{'-' * 52}\n"
        f"MEASUREMENT:  {card.measurement_plan}\n\n"
        f"REPETITIONS:  {card.planned_repetitions} trials per condition\n\n"
        f"STOPPING RULE:  {card.stopping_rule}\n\n"
        f"ANALYSIS RULE:  {card.analysis_rule}\n\n"
        f"I WILL REJECT MY HYPOTHESIS IF:\n  {card.rejection_condition}\n"
        f"{'-' * 52}\n"
        "Signed: ______________________   Date: ____________\n"
    )
