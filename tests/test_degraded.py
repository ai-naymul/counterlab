"""Degraded mode.

The claim being tested: CounterLab is not a wrapper. Take the model away and it
still finds the confound. If any of these fail, the claim is false.
"""

from __future__ import annotations

import httpx
import pytest

from app import service
from app.fixtures import FIXTURES
from app.models import ExperimentInput
from app.providers.base import ProviderUnavailable
from app.providers.fixture_provider import BrokenProvider, FixtureProvider


def pendulum() -> ExperimentInput:
    f = FIXTURES["pendulum"]
    return ExperimentInput(
        hypothesis=f["hypothesis"], procedure=f["procedure"], materials=f["materials"],
        time_available=f["time_available"], budget=f["budget"], level=f["level"],
    )


def test_no_provider_still_finds_the_confound():
    r = service.audit(pendulum(), provider=None)
    assert r.degraded_mode is True
    assert r.fatal_flaw.id == "R1_MULTI_VAR"


@pytest.mark.parametrize("boom", [
    ProviderUnavailable("down"),
    httpx.ReadTimeout("slow"),
    ValueError("garbage json"),
    KeyError("candidates"),
    RuntimeError("something unexpected"),
])
def test_every_provider_failure_degrades_instead_of_raising(boom):
    r = service.audit(pendulum(), provider=FixtureProvider(fail_with=boom))
    assert r.degraded_mode is True
    assert r.fatal_flaw.id == "R1_MULTI_VAR"


def test_broken_provider_degrades():
    r = service.audit(pendulum(), provider=BrokenProvider())
    assert r.degraded_mode is True
    assert r.verdict == "fatal_flaw"


def test_degraded_mode_states_a_reason():
    r = service.audit(pendulum(), provider=BrokenProvider())
    assert r.degraded_reason


def test_degraded_mode_lowers_confidence():
    r = service.audit(pendulum(), provider=BrokenProvider())
    assert r.confidence <= 0.45


def test_degraded_mode_admits_reduced_coverage():
    r = service.audit(pendulum(), provider=BrokenProvider())
    assert any("rules-only" in a.lower() for a in r.assumptions)


def test_degraded_mode_still_produces_a_prereg_card():
    r = service.audit(pendulum(), provider=BrokenProvider())
    assert r.prereg and r.prereg.rejection_condition


def test_degraded_mode_still_produces_repairs():
    r = service.audit(pendulum(), provider=BrokenProvider())
    assert r.minimal_repairs


def test_safety_gate_works_without_a_provider():
    f = FIXTURES["filter"]
    r = service.audit(
        ExperimentInput(hypothesis=f["hypothesis"], procedure=f["procedure"],
                        materials=f["materials"]),
        provider=BrokenProvider(),
    )
    assert r.verdict == "safety_stop"


def test_junk_field_values_are_coerced_rather_than_crashing():
    """A model that returns 'confidence: banana' should not take the request down."""
    from app.providers.gemini_provider import GeminiProvider

    a = GeminiProvider._to_audit(
        {"confidence": "not-a-number", "planned_repetitions": "x",
         "variables_changed": ["mass", "length"]},
        pendulum(),
    )
    assert 0.0 <= a.confidence <= 1.0
    assert a.planned_repetitions is None
    assert a.variables_changed == ["mass", "length"]


def test_confidence_out_of_range_is_clamped():
    from app.providers.gemini_provider import GeminiProvider

    assert GeminiProvider._to_audit({"confidence": 47.0}, pendulum()).confidence == 1.0
    assert GeminiProvider._to_audit({"confidence": -3.0}, pendulum()).confidence == 0.0


def test_empty_model_payload_normalises_rather_than_crashing():
    from app.providers.gemini_provider import GeminiProvider

    a = GeminiProvider._to_audit({}, pendulum())
    assert a.independent_variable is None
    assert a.planned_repetitions is None
    assert a.variables_changed == []
