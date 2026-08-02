from __future__ import annotations

import logging

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from . import prereg, service
from .fixtures import FIXTURES
from .models import ExperimentInput

log = logging.getLogger("counterlab.routes")
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "fixtures": FIXTURES, "mode": service.mode()}
    )


@router.get("/healthz")
def healthz():
    return {"ok": True, "mode": service.mode()}


@router.post("/audit", response_class=HTMLResponse)
async def audit(
    request: Request,
    hypothesis: str = Form(""),
    procedure: str = Form(""),
    materials: str = Form(""),
    time_available: str = Form("unspecified"),
    budget: str = Form("unspecified"),
    level: str = Form("high_school"),
    language: str = Form("en"),
    format: str = "",
):
    try:
        inp = ExperimentInput(
            hypothesis=hypothesis, procedure=procedure, materials=materials,
            time_available=time_available, budget=budget, level=level, language=language,
        )
    except ValidationError:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request, "fixtures": FIXTURES, "mode": service.mode(),
                "error": "Please fill in both your hypothesis and your procedure "
                         "(at least a few words each).",
                "form": {"hypothesis": hypothesis, "procedure": procedure, "materials": materials},
            },
            status_code=422,
        )

    try:
        result = service.audit(inp)
    except Exception as e:  # noqa: BLE001 - /audit must never 500
        log.exception("unexpected failure, falling back to rules-only: %s", e)
        from .extract import heuristic_extract
        from .merge import build_response

        result = build_response(
            audit=heuristic_extract(inp), degraded_mode=True,
            degraded_reason="Something went wrong internally, so only structural checks ran.",
        )

    if request.query_params.get("format") == "json":
        return JSONResponse(result.model_dump())

    template = "safety.html" if result.verdict == "safety_stop" else "result.html"
    return templates.TemplateResponse(
        template,
        {
            "request": request, "r": result, "inp": inp,
            "prereg_text": prereg.as_text(result.prereg) if result.prereg else "",
        },
    )


@router.post("/prereg.txt", response_class=PlainTextResponse)
async def prereg_txt(text: str = Form("")):
    return text
