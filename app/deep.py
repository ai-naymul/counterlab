"""Deep Audit - three adversarial lenses in parallel, plus evidence.

Originally written as a Render Workflow (see workflows/main.py). Render
Workflows turned out to require billing information, so this project does not
use them and does not enter that prize track. The same fan-out runs here in
process instead: three independent lenses via asyncio.gather, each with its own
failure handling, reconciled by plain code.

Same shape, no durable retries. workflows/main.py is the version that would run
on a paid Render plan; nothing here depends on it.
"""

from __future__ import annotations

import asyncio
import logging
import os

import httpx

from . import evidence
from .models import EvidenceCard, ExperimentInput
from .providers.gemini_provider import ANALYSE_CHAIN, GUARD, _body, _call

log = logging.getLogger("counterlab.deep")

LENS_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "severity": {"type": "string", "enum": ["fatal", "major", "minor"]},
                    "reason": {"type": "string"},
                },
                "required": ["title", "severity", "reason"],
            },
        },
        "verdict_one_line": {"type": "string"},
    },
    "required": ["findings", "verdict_one_line"],
}

LENSES: dict[str, tuple[str, str]] = {
    "confound": (
        "Hidden confounds",
        "You hunt for CONFOUNDS only. What else differs between the setups that the student has "
        "not noticed? What drifts over the course of the experiment - time of day, temperature, "
        "the student getting better at the procedure, batch differences in materials? "
        "Ignore every other kind of problem.",
    ),
    "measurement": (
        "Measurement validity",
        "You attack MEASUREMENT VALIDITY only. Is the instrument precise enough to detect the "
        "effect being claimed? Is the thing measured actually the thing in the hypothesis, or "
        "only correlated with it? Where do human reaction time, parallax, rounding, or "
        "judgement creep in? Ignore every other kind of problem.",
    ),
    "feasibility": (
        "Can this actually be done",
        "You attack FEASIBILITY only. Can a school student really finish this with the stated "
        "time, budget and materials? What runs out, breaks, takes far longer than expected, or "
        "needs an adult? Ignore every other kind of problem.",
    ),
}


async def _lens(client: httpx.AsyncClient, key: str, lens: str, body: str) -> dict | None:
    label, instruction = LENSES[lens]
    prompt = (
        f"{instruction}\n\n{GUARD}\n\n"
        "Return an empty findings list if this lens turns up nothing. An empty list is a valid "
        "answer and is better than inventing a problem.\n\n"
        f"<student_submission>\n{body}\n</student_submission>"
    )
    for model in [m.strip() for m in ANALYSE_CHAIN if m.strip()]:
        try:
            r = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                params={"key": key},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0,
                        "responseMimeType": "application/json",
                        "responseSchema": LENS_SCHEMA,
                    },
                },
            )
            r.raise_for_status()
            import json as _json

            data = _json.loads(r.json()["candidates"][0]["content"]["parts"][0]["text"])
            return {"lens": lens, "label": label, **data}
        except Exception as e:  # noqa: BLE001
            log.warning("lens %s on %s failed: %s", lens, model, type(e).__name__)
            continue
    return None


async def run(inp: ExperimentInput, concept: str) -> dict:
    """Never raises. Partial results are fine and are reported as partial."""
    key = os.getenv("GEMINI_API_KEY")
    body = _body(inp)

    async def ev() -> list[EvidenceCard]:
        return await asyncio.to_thread(evidence.fetch, concept, 4, True)

    if not key:
        cards = await ev()
        return {"available": False, "lenses": [], "evidence": [c.model_dump() for c in cards],
                "failed": 3, "reason": "No language model is configured."}

    async with httpx.AsyncClient(timeout=45) as client:
        results = await asyncio.gather(
            *[_lens(client, key, name, body) for name in LENSES],
            ev(),
            return_exceptions=True,
        )

    lenses = [r for r in results[:-1] if isinstance(r, dict)]
    cards = results[-1] if isinstance(results[-1], list) else []

    rank = {"fatal": 0, "major": 1, "minor": 2}
    for lr in lenses:
        lr["findings"] = sorted(
            (lr.get("findings") or []), key=lambda f: rank.get(f.get("severity"), 3)
        )[:4]

    return {
        "available": bool(lenses),
        "lenses": lenses,
        "evidence": [c.model_dump() for c in cards],
        "failed": len(LENSES) - len(lenses),
        "total_findings": sum(len(lr.get("findings") or []) for lr in lenses),
    }
