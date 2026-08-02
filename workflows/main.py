"""CounterLab Deep Audit - a Render Workflow.

Why this is a workflow and not another function call:

The instant audit answers in ~4 seconds and is what the student actually uses.
Deep Audit is the opposite shape of work - three independent adversarial passes
over the same plan, each with a different lens, run in parallel, each able to
fail and retry on its own, then reconciled. It is slow by nature and nobody
should be watching a spinner for it.

That is what Render Workflows are for: durable, retryable, fan-out task runs off
the request path. The web service triggers it and polls.

If this whole service is deleted, the product still works. That is deliberate.
"""

from __future__ import annotations

import asyncio
import json
import os

from render_sdk import Retry, Workflows

from app import evidence
from app.models import ExperimentInput
from app.providers.gemini_provider import (
    ANALYSE_CHAIN,
    GUARD,
    _body,
    _call_with_chain,
)

app = Workflows(default_timeout=600)

RETRY = Retry(max_retries=3, wait_duration_ms=1200, backoff_scaling=1.5)

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

LENSES = {
    "confound": (
        "You hunt for CONFOUNDS only. What else differs between the setups that the student "
        "has not noticed? What varies over the course of the experiment - time of day, "
        "temperature drift, the student getting better at the procedure, batch differences in "
        "materials? Ignore every other kind of problem."
    ),
    "measurement": (
        "You attack MEASUREMENT VALIDITY only. Is the instrument precise enough to see the "
        "effect being claimed? Is the thing measured actually the thing in the hypothesis, or "
        "just correlated with it? Where does human reaction time, parallax, rounding, or "
        "judgement enter? Ignore every other kind of problem."
    ),
    "feasibility": (
        "You attack FEASIBILITY and SAFETY only. Can a school student actually complete this "
        "with the stated time, budget and materials? What breaks, runs out, takes far longer "
        "than expected, or needs an adult? Ignore every other kind of problem."
    ),
}


def _run_lens(lens: str, body: str) -> dict:
    import httpx

    key = os.environ["GEMINI_API_KEY"]
    prompt = (
        f"{LENSES[lens]}\n\n{GUARD}\n\n"
        "Return an empty findings list if this lens turns up nothing. That is a valid answer "
        "and is better than inventing a problem.\n\n"
        f"<student_submission>\n{body}\n</student_submission>"
    )
    with httpx.Client(timeout=60) as client:
        result, model = _call_with_chain(client, ANALYSE_CHAIN, prompt, LENS_SCHEMA, key)
    result["lens"] = lens
    result["model"] = model
    return result


@app.task(retry=RETRY, timeout_seconds=180)
def confound_hunter(body: str) -> dict:
    return _run_lens("confound", body)


@app.task(retry=RETRY, timeout_seconds=180)
def measurement_validity(body: str) -> dict:
    return _run_lens("measurement", body)


@app.task(retry=RETRY, timeout_seconds=180)
def safety_feasibility(body: str) -> dict:
    return _run_lens("feasibility", body)


@app.task(retry=RETRY, timeout_seconds=120)
def gather_evidence(concept: str) -> list[dict]:
    return [c.model_dump() for c in evidence.fetch(concept, limit=4, scholarly=True)]


@app.task(timeout_seconds=300)
def synthesize(lenses: list[dict], evidence_cards: list[dict]) -> dict:
    """Reconcile the lenses. Plain code - no model gets to overrule the count."""
    all_findings, by_lens = [], {}
    for res in lenses:
        if not isinstance(res, dict):
            continue
        lens = res.get("lens", "?")
        by_lens[lens] = res.get("verdict_one_line", "")
        for f in res.get("findings", []) or []:
            f = dict(f)
            f["lens"] = lens
            all_findings.append(f)

    rank = {"fatal": 0, "major": 1, "minor": 2}
    all_findings.sort(key=lambda f: rank.get(f.get("severity", "minor"), 3))

    return {
        "findings": all_findings,
        "by_lens": by_lens,
        "evidence": evidence_cards,
        "fatal_count": sum(1 for f in all_findings if f.get("severity") == "fatal"),
        "lens_count": len(by_lens),
    }


@app.task(timeout_seconds=900)
async def deep_audit(payload: dict) -> dict:
    """Entry point. Three lenses plus evidence, all in parallel, then reconcile."""
    inp = ExperimentInput(**payload["input"])
    body = _body(inp)
    concept = payload.get("concept") or "design of experiments"

    confound, measurement, feasibility, ev = await asyncio.gather(
        confound_hunter(body),
        measurement_validity(body),
        safety_feasibility(body),
        gather_evidence(concept),
        return_exceptions=True,
    )

    lenses = [r for r in (confound, measurement, feasibility) if isinstance(r, dict)]
    cards = ev if isinstance(ev, list) else []
    failed = 3 - len(lenses)

    out = await synthesize(lenses, cards)
    out["lenses_failed"] = failed
    return out


if __name__ == "__main__":
    print("registering CounterLab workflow tasks", json.dumps(sorted(LENSES)))
    app.start()
