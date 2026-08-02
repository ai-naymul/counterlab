from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")

app = FastAPI(
    title="CounterLab",
    description="Red-team your experiment before you run it.",
    docs_url="/api",
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
