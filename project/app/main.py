import logging

from fastapi import FastAPI

from app.api import ping
from app.api import summaries
from app.db import init_db


logger = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(
        summaries.router,
        prefix="/summaries",
        tags=["summaries"],
    )
    return application


app = create_application()


@app.on_event("startup")
async def statup_event():
    logger.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shuting down...")
