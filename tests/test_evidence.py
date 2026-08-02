"""Evidence layer: keyless, silent on failure, and it never sees student text."""

from __future__ import annotations

import asyncio

import pytest

from app import deep, evidence
from app.models import ExperimentInput


def test_concepts_are_fixed_strings_not_student_text():
    """The privacy claim: nothing the student wrote can reach a search provider.

    Every outbound query comes from this fixed table, keyed by rule id.
    """
    for rule_id, concept in evidence.CONCEPT_FOR_RULE.items():
        assert isinstance(concept, str) and concept
        assert concept in (
            "confounding variable", "dependent and independent variables",
            "units of measurement", "repeated measurements experimental error",
            "scientific control", "measurement validity",
        )


def test_unknown_rule_falls_back_to_a_fixed_concept():
    assert evidence.concept_for("NOT_A_RULE") == evidence.DEFAULT_CONCEPT
    assert evidence.concept_for(None) == evidence.DEFAULT_CONCEPT


def test_evidence_never_raises_when_the_network_is_gone(monkeypatch):
    class Boom:
        def __init__(self, *a, **k): raise OSError("no network")

    monkeypatch.setattr(evidence.httpx, "Client", Boom)
    assert evidence.fetch("confounding variable") == []


def test_evidence_survives_a_bad_response(monkeypatch):
    class FakeResp:
        def raise_for_status(self): pass
        def json(self): return {"unexpected": "shape"}

    class FakeClient:
        def __init__(self, *a, **k): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def get(self, *a, **k): return FakeResp()

    monkeypatch.setattr(evidence.httpx, "Client", FakeClient)
    assert evidence.fetch("confounding variable") == []


def test_html_markup_is_stripped_from_snippets():
    assert evidence._clean('a <span class="searchmatch">confounder</span> is') == "a confounder is"
    assert "&amp;" not in evidence._clean("salt &amp; water")


def test_deep_audit_degrades_without_a_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(evidence, "fetch", lambda *a, **k: [])
    inp = ExperimentInput(hypothesis="h test", procedure="p test procedure here")
    d = asyncio.run(deep.run(inp, "confounding variable"))
    assert d["available"] is False
    assert d["lenses"] == []
    assert d["reason"]


def test_deep_audit_reports_partial_failure_rather_than_dying(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "x")

    async def one_works(client, key, lens, body):
        return {"lens": lens, "label": "L", "findings": [], "verdict_one_line": "ok"} \
            if lens == "confound" else None

    monkeypatch.setattr(deep, "_lens", one_works)
    monkeypatch.setattr(evidence, "fetch", lambda *a, **k: [])
    inp = ExperimentInput(hypothesis="h test", procedure="p test procedure here")
    d = asyncio.run(deep.run(inp, "confounding variable"))
    assert d["available"] is True
    assert d["failed"] == 2


def test_deep_audit_route_refuses_a_blocked_plan():
    from fastapi.testclient import TestClient

    from app.fixtures import FIXTURES
    from app.main import app

    f = FIXTURES["filter"]
    r = TestClient(app).post("/deep-audit", data={
        "hypothesis": f["hypothesis"], "procedure": f["procedure"], "materials": f["materials"]})
    assert r.status_code == 200
    body = r.json()
    assert body["available"] is False
    assert "safety" in body["reason"].lower()


@pytest.mark.parametrize("bad", [{}, {"hypothesis": "x"}, {"procedure": ""}])
def test_deep_audit_route_never_5xxs(bad):
    from fastapi.testclient import TestClient

    from app.main import app

    assert TestClient(app).post("/deep-audit", data=bad).status_code < 500
