"""Deterministic engine. No network, no key, no model."""

from __future__ import annotations

import pytest

from app.merge import build_response
from app.models import ExperimentAudit
from app.rules import pick_fatal, run_rules


def audit(**kw) -> ExperimentAudit:
    base = dict(
        hypothesis="h",
        independent_variable="temperature",
        dependent_variable="rise height",
        controlled_variables=["flour amount"],
        variables_changed=["temperature"],
        measurement_method="ruler against the tin",
        measurement_unit="cm",
        planned_repetitions=5,
    )
    base.update(kw)
    return ExperimentAudit(**base)


def ids(a: ExperimentAudit) -> set[str]:
    return {f.id for f in run_rules(a)}


# --- each rule fires on its own trigger -------------------------------------

def test_r1_fires_on_two_changed_variables():
    assert "R1_MULTI_VAR" in ids(audit(variables_changed=["mass", "length"]))


def test_r2_fires_when_no_dependent_variable():
    assert "R2_NO_DV" in ids(audit(dependent_variable=None))


def test_r3_fires_when_no_independent_variable():
    assert "R3_NO_IV" in ids(audit(independent_variable=None))


def test_r4_fires_when_unit_missing():
    assert "R4_NO_UNIT" in ids(audit(measurement_unit=None))


def test_r5_fires_below_three_trials():
    assert "R5_SINGLE_TRIAL" in ids(audit(planned_repetitions=1))


def test_r6_fires_when_repetitions_unstated():
    assert "R6_NO_REPS_STATED" in ids(audit(planned_repetitions=None))


def test_r7_fires_when_nothing_controlled():
    assert "R7_NO_CONTROL" in ids(audit(controlled_variables=[]))


def test_r8_fires_when_iv_also_controlled():
    a = audit(independent_variable="temperature", controlled_variables=["Temperature"])
    assert "R8_IV_IN_CONTROLLED" in ids(a)  # case-insensitive


def test_r9_fires_when_no_measurement_method():
    assert "R9_NO_MEASUREMENT" in ids(audit(measurement_method=None))


# --- and stays quiet on a sound plan ----------------------------------------

def test_sound_plan_triggers_nothing():
    assert ids(audit()) == set()


def test_sound_plan_is_a_pass():
    r = build_response(audit=audit())
    assert r.verdict == "pass"
    assert r.fatal_flaw is None


def test_exactly_three_trials_is_acceptable():
    assert "R5_SINGLE_TRIAL" not in ids(audit(planned_repetitions=3))


# --- ranking ----------------------------------------------------------------

def test_only_one_fatal_flaw_is_promoted():
    r = build_response(audit=audit(variables_changed=["a", "b"], dependent_variable=None))
    assert r.fatal_flaw is not None
    assert sum(1 for f in [r.fatal_flaw] if f.severity == "fatal") == 1
    # the other fatal is still reported, just not as THE flaw
    assert "R2_NO_DV" in {f.id for f in r.other_findings}


def test_multi_var_outranks_missing_dv():
    r = build_response(audit=audit(variables_changed=["a", "b"], dependent_variable=None))
    assert r.fatal_flaw.id == "R1_MULTI_VAR"


def test_deterministic_fatal_outranks_model_fatal():
    from app.models import Finding

    model = [Finding(id="M1", title="model thinks this is fatal", severity="fatal",
                     reason="r", source="model")]
    r = build_response(audit=audit(variables_changed=["a", "b"]), model_findings=model)
    assert r.fatal_flaw.source == "deterministic"


def test_pick_fatal_returns_none_when_clean():
    assert pick_fatal(run_rules(audit())) is None


# --- rules never reach the network ------------------------------------------

def test_rules_module_imports_no_network_library():
    import pathlib

    src = pathlib.Path("app/rules.py").read_text()
    for banned in ("httpx", "requests", "urllib", "socket", "aiohttp"):
        assert banned not in src, f"rules.py must stay offline, found {banned}"


# --- repairs and pre-registration are always produced -----------------------

def test_fatal_flaw_always_comes_with_a_repair():
    r = build_response(audit=audit(variables_changed=["mass", "length"]))
    assert r.minimal_repairs
    assert r.cheapest_falsification_test


@pytest.mark.parametrize("kw", [
    {}, {"variables_changed": ["a", "b"]}, {"dependent_variable": None},
    {"planned_repetitions": None}, {"independent_variable": None},
])
def test_prereg_card_always_has_a_rejection_condition(kw):
    r = build_response(audit=audit(**kw))
    assert r.prereg is not None
    assert r.prereg.rejection_condition.strip()
    assert r.prereg.planned_repetitions >= 3
