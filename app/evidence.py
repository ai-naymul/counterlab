"""Evidence cards from keyless sources.

Wikipedia first (fast, canonical on methodology concepts), OpenAlex second
(scholarly). No API key, no account, nothing to run out.

PRIVACY: only a short CONCEPT query derived from the finding is sent upstream -
never the student's hypothesis, procedure, or materials. test_evidence.py
asserts this.

Retrieved text is untrusted. It is stripped of markup, truncated, and only ever
displayed - it is never concatenated into a prompt.
"""

from __future__ import annotations

import html
import logging
import os
import re

import httpx

from .models import EvidenceCard

log = logging.getLogger("counterlab.evidence")

UA = f"CounterLab/1.0 (STEMist Hacks IV project; {os.getenv('COUNTERLAB_CONTACT_EMAIL', 'contact@example.com')})"
TIMEOUT = float(os.getenv("COUNTERLAB_EVIDENCE_TIMEOUT", "8"))

# Rule id -> the concept a student should read about. Fixed strings, so nothing
# the student wrote can leak into an outbound request.
CONCEPT_FOR_RULE: dict[str, str] = {
    "R1_MULTI_VAR": "confounding variable",
    "R2_NO_DV": "dependent and independent variables",
    "R3_NO_IV": "dependent and independent variables",
    "R4_NO_UNIT": "units of measurement",
    "R5_SINGLE_TRIAL": "repeated measurements experimental error",
    "R6_NO_REPS_STATED": "repeated measurements experimental error",
    "R7_NO_CONTROL": "scientific control",
    "R8_IV_IN_CONTROLLED": "scientific control",
    "R9_NO_MEASUREMENT": "measurement validity",
}
DEFAULT_CONCEPT = "design of experiments"


def concept_for(rule_id: str | None) -> str:
    return CONCEPT_FOR_RULE.get(rule_id or "", DEFAULT_CONCEPT)


def _clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return html.unescape(text).strip()


def _wikipedia(client: httpx.Client, query: str, limit: int) -> list[EvidenceCard]:
    r = client.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "query", "list": "search", "srsearch": query,
                "srlimit": limit, "format": "json"},
    )
    r.raise_for_status()
    out = []
    for hit in r.json().get("query", {}).get("search", []):
        title = _clean(hit.get("title", ""))
        if not title:
            continue
        out.append(EvidenceCard(
            title=title,
            url=f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            snippet=_clean(hit.get("snippet", ""))[:240],
            origin="Wikipedia",
        ))
    return out


def _openalex(client: httpx.Client, query: str, limit: int) -> list[EvidenceCard]:
    r = client.get(
        "https://api.openalex.org/works",
        params={"search": query, "per-page": limit,
                "mailto": os.getenv("COUNTERLAB_CONTACT_EMAIL", "")},
    )
    r.raise_for_status()
    out = []
    for w in r.json().get("results", []):
        title = _clean(w.get("title") or w.get("display_name") or "")
        url = w.get("doi") or w.get("id")
        if not title or not url:
            continue
        year = w.get("publication_year")
        out.append(EvidenceCard(
            title=title[:160],
            url=url,
            snippet=f"Research paper{f', {year}' if year else ''}.",
            origin="OpenAlex",
        ))
    return out


def fetch(concept: str, limit: int = 3, scholarly: bool = False) -> list[EvidenceCard]:
    """Never raises. Missing cards are a silent, acceptable outcome."""
    cards: list[EvidenceCard] = []
    try:
        with httpx.Client(timeout=TIMEOUT, headers={"User-Agent": UA}) as client:
            try:
                cards += _wikipedia(client, concept, limit)
            except Exception as e:  # noqa: BLE001
                log.warning("wikipedia unavailable: %s", type(e).__name__)
            if scholarly and len(cards) < limit:
                try:
                    cards += _openalex(client, concept, limit - len(cards))
                except Exception as e:  # noqa: BLE001
                    log.warning("openalex unavailable: %s", type(e).__name__)
    except Exception as e:  # noqa: BLE001
        log.warning("evidence layer unavailable: %s", type(e).__name__)
    return cards[:limit]
