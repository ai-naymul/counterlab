"""Pre-registration card.

Written BEFORE data exists. The point is the rejection condition: committing in
advance to what result would count as being wrong is the single cheapest defence
against talking yourself into a conclusion afterwards.
"""

from __future__ import annotations

import re

from .models import ExperimentAudit, PreRegCard
from .rules import MIN_TRIALS

# The model tends to answer the prompt "complete this sentence" by repeating the
# stem. Strip it so the card doesn't read "I will reject my hypothesis if I will
# reject my hypothesis if ...".
_STEM = re.compile(r"^\s*i\s+will\s+reject\s+my\s+hypothesis\s+if\s*,?\s*", re.IGNORECASE)

_TRIALS_IN_TEXT = re.compile(r"\b(\d{1,2})\s*(?:trials?|repetitions?|repeats?|runs?|times)\b", re.IGNORECASE)


def _strip_stem(text: str) -> str:
    out = _STEM.sub("", text).strip()
    return (out[0].lower() + out[1:]) if out else out


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

    # If the model recommended a trial count in its stopping rule, adopt it - a card
    # that says "3 trials" above a rule that says "stop after 5" is worse than either.
    if stopping_rule:
        m = _TRIALS_IN_TEXT.search(stopping_rule)
        if m and MIN_TRIALS <= int(m.group(1)) <= 50:
            planned = int(m.group(1))

    if rejection_condition:
        rejection_condition = _strip_stem(rejection_condition)

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
