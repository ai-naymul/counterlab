from __future__ import annotations

from app import safety, service
from app.fixtures import FIXTURES
from app.models import ExperimentInput


def inp(key: str) -> ExperimentInput:
    f = FIXTURES[key]
    return ExperimentInput(
        hypothesis=f["hypothesis"], procedure=f["procedure"], materials=f["materials"],
        time_available=f["time_available"], budget=f["budget"], level=f["level"],
    )


def test_floodwater_filter_is_a_safety_stop():
    r = service.audit(inp("filter"), provider=None)
    assert r.verdict == "safety_stop"


def test_safety_stop_explains_clarity_is_not_potability():
    r = service.audit(inp("filter"), provider=None)
    blob = " ".join(r.safety_notes).lower()
    assert "clarity is not safety" in blob or "safe to drink" in blob


def test_safety_stop_offers_a_safe_alternative():
    r = service.audit(inp("filter"), provider=None)
    assert r.safe_alternative
    assert "turbidity" in r.safe_alternative.lower()


def test_safety_stop_gives_no_filtration_procedure():
    """A refusal that still hands over the method is not a refusal."""
    r = service.audit(inp("filter"), provider=None)
    blob = (" ".join(r.safety_notes) + " " + (r.safe_alternative or "")).lower()
    assert "never drink" in blob or "not for drinking" in blob or "never drink any of it" in blob
    assert r.fatal_flaw is None  # no design coaching on a blocked plan
    assert not r.minimal_repairs


def test_safety_stop_skips_the_model_entirely():
    """Blocked input must not be forwarded to a third party."""
    from app.providers.fixture_provider import FixtureProvider

    class Tripwire(FixtureProvider):
        def analyse(self, i):  # noqa: ANN001
            raise AssertionError("blocked input must never reach the provider")

    r = service.audit(inp("filter"), provider=Tripwire())
    assert r.verdict == "safety_stop"


def test_mains_voltage_blocks():
    v = safety.check("Does voltage affect brightness?",
                     "I will connect the bulb to the wall socket and build the circuit.", "")
    assert v.blocked and v.block_id == "MAINS_VOLTAGE"


def test_human_subjects_blocks():
    v = safety.check("Does sugar affect focus?",
                     "I will feed my classmates energy drinks and test them.", "")
    assert v.blocked and v.block_id == "HUMAN_SUBJECTS"


def test_ordinary_experiment_is_not_blocked():
    v = safety.check("Heavier bobs swing faster",
                     "I will time a pendulum with a stopwatch and a ruler.", "string, weights")
    assert not v.blocked


def test_warnings_escalate_but_do_not_block():
    v = safety.check("Does salt change boiling point?",
                     "I will boil water on the stove and measure the temperature.", "")
    assert not v.blocked
    assert v.notes, "boiling should raise a caution note"


def test_warnings_never_change_the_verdict():
    """The lexicon may only add caution. It must not create or remove a flaw."""
    i = ExperimentInput(
        hypothesis="Salt raises the boiling point of water.",
        procedure="I will boil 500 ml of water with 10 g of salt and 500 ml without, "
                  "measure the temperature in celsius with a thermometer, and repeat 5 times. "
                  "I will keep the pan and the stove setting the same.",
    )
    r = service.audit(i, provider=None)
    assert r.verdict != "safety_stop"
    assert r.safety_notes  # cautions present
