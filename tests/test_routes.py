from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.fixtures import FIXTURES
from app.main import app
from app.models import AuditResponse

client = TestClient(app)


def form(key: str) -> dict:
    f = FIXTURES[key]
    return {
        "hypothesis": f["hypothesis"], "procedure": f["procedure"], "materials": f["materials"],
        "time_available": f["time_available"], "budget": f["budget"], "level": f["level"],
    }


def test_index_renders():
    r = client.get("/")
    assert r.status_code == 200
    assert "Red-team your experiment" in r.text


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["ok"] is True
    assert r.json()["mode"] in ("full", "rules-only")


@pytest.mark.parametrize("key", list(FIXTURES))
def test_audit_never_returns_5xx(key):
    r = client.post("/audit", data=form(key))
    assert r.status_code < 500


@pytest.mark.parametrize("key", list(FIXTURES))
def test_json_output_validates_against_the_schema(key):
    r = client.post("/audit?format=json", data=form(key))
    assert r.status_code == 200
    AuditResponse.model_validate(r.json())


def test_pendulum_html_shows_the_confound():
    r = client.post("/audit", data=form("pendulum"))
    assert "changed more than one thing at once" in r.text
    assert "I will reject my hypothesis if" in r.text


def test_valid_plan_html_says_no_fatal_flaw():
    r = client.post("/audit", data=form("valid"))
    assert "No fatal flaw detected" in r.text


def test_filter_renders_the_safety_page():
    r = client.post("/audit", data=form("filter"))
    assert "Safety stop" in r.text
    assert "What you can do instead" in r.text


def test_provenance_chips_are_shown():
    r = client.post("/audit", data=form("pendulum"))
    assert "structural check" in r.text


def test_missing_fields_gives_422_not_500():
    r = client.post("/audit", data={"hypothesis": "", "procedure": ""})
    assert r.status_code == 422
    assert "Please fill in" in r.text


def test_garbage_input_does_not_crash():
    r = client.post("/audit", data={"hypothesis": "?" * 5, "procedure": "\x00\x01 ??? " * 20})
    assert r.status_code < 500


def test_oversized_input_is_rejected_cleanly():
    r = client.post("/audit", data={"hypothesis": "a" * 9000, "procedure": "b" * 9000})
    assert r.status_code == 422


def test_no_secret_leaks_into_any_response():
    import os

    key = os.getenv("GEMINI_API_KEY")
    for k in FIXTURES:
        r = client.post("/audit", data=form(k))
        assert "GEMINI_API_KEY" not in r.text
        if key:
            assert key not in r.text
