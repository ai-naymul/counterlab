"""Safety pre-filter.

A deliberate, bounded exception to "no keyword classification".

The forbidden pattern is using keywords as the decision rule for a nuanced
semantic judgement. This is not that. This filter is recall-oriented, it can
only ever ADD caution, and it never assigns a scientific-quality label or
decides the fatal flaw. A false positive costs a warning the student can read
past; a false negative could cost a burn. Tuned accordingly.

Hard blocks use AND-of-ORs so that "drink" alone is not enough - it has to
co-occur with a water-treatment context before we refuse.
"""

from __future__ import annotations

# (id, [group1, group2, ...], message, safe_alternative)
# Every group must match at least one term for the block to fire.
HARD_BLOCKS: list[tuple[str, list[list[str]], str, str]] = [
    (
        "POTABILITY",
        [
            ["drink", "drinking", "potable", "safe to consume", "ingest", "swallow", "taste"],
            ["water", "floodwater", "flood water", "pond", "river", "rain", "filter", "purif", "well water"],
        ],
        "This plan involves judging whether treated water is safe to drink. Water can look "
        "completely clear and still carry bacteria, viruses, and dissolved contaminants that "
        "cause serious illness. Clarity is not safety, and no home filter test can establish "
        "that water is potable.",
        "Test turbidity only, and never drink any of it. Make your own muddy water from clean "
        "tap water and garden soil, pour a fixed volume through each filter, and measure how "
        "clear the output is - either by timing how long a light takes to become visible "
        "through a fixed depth, or by photographing each sample against a printed grid and "
        "comparing. You are measuring clarity, and you say so on your board.",
    ),
    (
        "HUMAN_SUBJECTS",
        [
            ["feed", "feeding", "give", "administer", "dose", "dosing", "inject"],
            ["classmate", "friends", "students", "participants", "my family", "volunteers", "people", "children", "babies"],
        ],
        "This plan involves giving something to other people to consume or be exposed to. "
        "Experiments on human participants need ethics approval and informed consent, which a "
        "school project cannot provide.",
        "Redesign so that people are not the thing being tested. You can survey opinions with "
        "consent and anonymity, or test the material itself rather than its effect on a person.",
    ),
    (
        "MAINS_VOLTAGE",
        [
            ["mains", "wall socket", "wall outlet", "power outlet", "240v", "220v", "110v", "high voltage", "electric shock"],
            ["circuit", "wire", "wiring", "connect", "plug", "experiment", "test", "build"],
        ],
        "This plan involves mains electricity. Household voltage can kill, and it does so at "
        "currents far below what you would notice as a shock.",
        "Run the same investigation on batteries. A 9 V battery or a 4xAA pack demonstrates "
        "almost every circuit principle safely, and your measurements will be cleaner because "
        "the supply is steadier.",
    ),
    (
        "HAZARDOUS_SYNTHESIS",
        [
            ["make", "making", "synthesi", "produce", "create", "build", "brew"],
            ["explosive", "gunpowder", "thermite", "chlorine gas", "poison", "toxic gas", "napalm", "pepper spray"],
        ],
        "This plan involves producing a hazardous substance. That is outside what any school "
        "project should attempt, regardless of scale.",
        "Pick the underlying question instead - reaction rate, gas volume, energy released - "
        "and investigate it with baking soda and vinegar, or with a hand-warmer, where the "
        "chemistry is visible and nothing produced is dangerous.",
    ),
]

WARN_TERMS: dict[str, str] = {
    "fire": "Open flame is involved. Work with an adult present, keep water nearby, and tie back hair and sleeves.",
    "flame": "Open flame is involved. Work with an adult present, keep water nearby, and tie back hair and sleeves.",
    "burn": "Something is being burned. Do this outdoors or under a fume hood, with an adult present.",
    "candle": "Open flame is involved. Keep it away from paper and fabric, and never leave it unattended.",
    "boil": "Boiling liquid causes scalds. Use tongs or oven gloves and keep the handle turned inward.",
    "acid": "Acids can burn skin and eyes. Wear eye protection, and add acid to water rather than water to acid.",
    "bleach": "Bleach must never be mixed with ammonia, vinegar, or other cleaners - the combination releases toxic gas.",
    "ammonia": "Ammonia must never be mixed with bleach. Work somewhere well ventilated.",
    "knife": "A sharp blade is involved. Cut away from your hands, on a stable surface.",
    "blade": "A sharp blade is involved. Cut away from your hands, on a stable surface.",
    "mould": "Growing mould releases spores. Keep the container sealed and do not open it indoors.",
    "mold": "Growing mould releases spores. Keep the container sealed and do not open it indoors.",
    "bacteria": "Culturing bacteria can grow organisms you did not intend. Keep plates sealed and dispose of them without opening.",
    "battery": "Never short a battery across its terminals - it can overheat and vent.",
    "laser": "Never point a laser at eyes, and beware of reflections off glass and metal.",
    "microwave": "Do not microwave sealed containers or metal.",
    "drill": "Secure the workpiece before drilling and wear eye protection.",
}


class SafetyVerdict:
    def __init__(
        self,
        blocked: bool,
        notes: list[str],
        message: str | None = None,
        alternative: str | None = None,
        block_id: str | None = None,
    ) -> None:
        self.blocked = blocked
        self.notes = notes
        self.message = message
        self.alternative = alternative
        self.block_id = block_id


def check(*texts: str) -> SafetyVerdict:
    """Screen the student's raw text. Escalate only - never lowers a score."""
    blob = " ".join(t.lower() for t in texts if t)

    for block_id, groups, message, alternative in HARD_BLOCKS:
        if all(any(term in blob for term in group) for group in groups):
            return SafetyVerdict(True, [], message, alternative, block_id)

    notes: list[str] = []
    for term, note in WARN_TERMS.items():
        if term in blob and note not in notes:
            notes.append(note)

    return SafetyVerdict(False, notes[:4])
