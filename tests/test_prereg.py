"""Pre-registration card must be internally consistent and readable."""

from __future__ import annotations

import pytest

from app import prereg
from app.models import ExperimentAudit
from app.rules import MIN_TRIALS


def a(**kw) -> ExperimentAudit:
    base = dict(hypothesis="h", independent_variable="mass", dependent_variable="swing time",
                measurement_unit="seconds", measurement_method="stopwatch", planned_repetitions=1)
    base.update(kw)
    return ExperimentAudit(**base)


@pytest.mark.parametrize("supplied", [
    "I will reject my hypothesis if the heavier bob is not faster.",
    "i will reject my hypothesis if the heavier bob is not faster.",
    "I will reject my hypothesis, if the heavier bob is not faster.",
    "I WILL REJECT MY HYPOTHESIS IF the heavier bob is not faster.",
])
def test_repeated_stem_is_stripped(supplied):
    card = prereg.build(a(), rejection_condition=supplied)
    assert not card.rejection_condition.lower().startswith("i will reject")
    assert "heavier bob is not faster" in card.rejection_condition


def test_rejection_without_the_stem_is_left_alone():
    card = prereg.build(a(), rejection_condition="the averages overlap.")
    assert card.rejection_condition == "the averages overlap."


def test_trial_count_matches_the_stopping_rule():
    """A card saying '3 trials' above a rule saying 'stop after 5' is a defect."""
    card = prereg.build(a(), stopping_rule="Stop after I have performed 5 trials for each mass.")
    assert card.planned_repetitions == 5


def test_absurd_trial_counts_are_ignored():
    card = prereg.build(a(), stopping_rule="do 900 trials")
    assert card.planned_repetitions == MIN_TRIALS


def test_below_minimum_trial_counts_are_ignored():
    card = prereg.build(a(), stopping_rule="just 1 trial is enough")
    assert card.planned_repetitions >= MIN_TRIALS


def test_student_count_is_respected_when_already_sufficient():
    card = prereg.build(a(planned_repetitions=8))
    assert card.planned_repetitions == 8


def test_card_text_renders_without_placeholders():
    text = prereg.as_text(prereg.build(a()))
    assert "I WILL REJECT MY HYPOTHESIS IF" in text
    assert "None" not in text
    assert "{" not in text
