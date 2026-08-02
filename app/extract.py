"""Structural pre-parse - the fallback extractor used when no model is available.

This is what makes rules-only mode more than an apology. It does NOT try to
understand the text. It pulls out stated quantities and groups them by physical
dimension: if two different masses and two different lengths appear in a
comparison, then two things differ, and R1_MULTI_VAR fires without any model
having been involved.

That is dimensional bookkeeping on explicit numbers, not keyword classification.
"""

from __future__ import annotations

import re

from .models import ExperimentAudit, ExperimentInput

# unit token -> (dimension name, canonical multiplier to a base unit)
UNITS: dict[str, tuple[str, float]] = {
    "mg": ("mass", 0.001), "g": ("mass", 1.0), "gram": ("mass", 1.0), "grams": ("mass", 1.0),
    "kg": ("mass", 1000.0), "kilogram": ("mass", 1000.0), "kilograms": ("mass", 1000.0),
    "mm": ("length", 0.1), "cm": ("length", 1.0), "m": ("length", 100.0),
    "meter": ("length", 100.0), "meters": ("length", 100.0),
    "metre": ("length", 100.0), "metres": ("length", 100.0),
    "inch": ("length", 2.54), "inches": ("length", 2.54),
    "ml": ("volume", 1.0), "millilitre": ("volume", 1.0), "milliliter": ("volume", 1.0),
    "l": ("volume", 1000.0), "litre": ("volume", 1000.0), "liter": ("volume", 1000.0),
    "litres": ("volume", 1000.0), "liters": ("volume", 1000.0),
    "s": ("time", 1.0), "sec": ("time", 1.0), "secs": ("time", 1.0),
    "second": ("time", 1.0), "seconds": ("time", 1.0),
    "min": ("time", 60.0), "mins": ("time", 60.0), "minute": ("time", 60.0), "minutes": ("time", 60.0),
    "hour": ("time", 3600.0), "hours": ("time", 3600.0),
    "day": ("time", 86400.0), "days": ("time", 86400.0),
    "c": ("temperature", 1.0), "celsius": ("temperature", 1.0), "degrees": ("angle", 1.0),
    "degree": ("angle", 1.0), "ml/min": ("flow", 1.0), "w": ("power", 1.0), "watt": ("power", 1.0),
    "watts": ("power", 1.0), "v": ("voltage", 1.0), "volt": ("voltage", 1.0), "volts": ("voltage", 1.0),
}

QUANTITY_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(" + "|".join(sorted(UNITS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

REPS_RE = re.compile(
    r"\b(?:repeat(?:ed|ing)?|run|do|perform|measure|test)?\s*(\d+)\s*"
    r"(?:times|trials|trial|repetitions|repeats|runs)\b",
    re.IGNORECASE,
)
REPS_WORD_RE = re.compile(r"\b(once|twice|three times|five times|ten times)\b", re.IGNORECASE)
WORD_REPS = {"once": 1, "twice": 2, "three times": 3, "five times": 5, "ten times": 10}

MEASURE_VERBS = ("measure", "record", "time", "count", "weigh", "observe", "note down", "track")


def _distinct(values: list[float]) -> int:
    out: list[float] = []
    for v in values:
        if not any(abs(v - o) < 1e-9 for o in out):
            out.append(v)
    return len(out)


def heuristic_extract(inp: ExperimentInput) -> ExperimentAudit:
    text = f"{inp.hypothesis}\n{inp.procedure}\n{inp.materials}"
    low = text.lower()

    # Group every stated quantity by physical dimension.
    by_dim: dict[str, list[float]] = {}
    for raw, unit in QUANTITY_RE.findall(text):
        dim, mult = UNITS[unit.lower()]
        by_dim.setdefault(dim, []).append(float(raw) * mult)

    # A dimension with two or more DIFFERENT stated values is a thing that varies.
    changed = [dim for dim, vals in by_dim.items() if _distinct(vals) > 1]
    # Time usually describes duration or measurement, not a manipulated setting.
    changed = [d for d in changed if d != "time"] or changed

    reps: int | None = None
    m = REPS_RE.search(text)
    if m:
        reps = int(m.group(1))
    else:
        w = REPS_WORD_RE.search(text)
        if w:
            reps = WORD_REPS[w.group(1).lower()]
        elif re.search(r"\beach\b.{0,24}\bonce\b", low) or re.search(r"\bone (?:swing|trial|time)\b", low):
            reps = 1

    # Measurement unit and outcome: look only at what the student says they will DO.
    # Materials is a shopping list - "two fishing weights (50 g)" is not a measurement plan,
    # and matching "weigh" inside "weights" there is exactly how you get a wrong unit.
    action_text = f"{inp.hypothesis}\n{inp.procedure}"
    action_low = action_text.lower()

    unit_found: str | None = None
    outcome: str | None = None
    for verb in MEASURE_VERBS:
        for vm in re.finditer(rf"\b{re.escape(verb)}(?:s|d|ed|ing)?\b", action_low):
            window = action_text[vm.end(): vm.end() + 90]
            if outcome is None:
                phrase = re.split(r"[.,;]| with | using | and then ", window.strip(), maxsplit=1)[0]
                phrase = " ".join(phrase.split()[:7]).strip()
                if len(phrase) > 2:
                    outcome = phrase
            qm = QUANTITY_RE.search(window)
            if qm:
                unit_found = qm.group(2)
                break
            bare = re.search(
                r"\bin (seconds?|cm|centimet(?:re|er)s?|grams?|millilit(?:re|er)s?|minutes?|degrees)\b",
                window, re.IGNORECASE)
            if bare:
                unit_found = bare.group(1)
                break
        if unit_found:
            break

    has_measure_verb = outcome is not None

    assumptions = [
        "Extracted by structural pre-parse (no language model). Only quantities you wrote "
        "with explicit units were detected."
    ]

    return ExperimentAudit(
        hypothesis=inp.hypothesis.strip(),
        independent_variable=changed[0] if changed else None,
        dependent_variable=outcome if has_measure_verb else None,
        controlled_variables=[],
        variables_changed=changed,
        measurement_method=("as described in your procedure" if has_measure_verb else None),
        measurement_unit=unit_found,
        planned_repetitions=reps,
        assumptions=assumptions,
        confidence=0.4,
    )
