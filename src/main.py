from logging import config

from fastapi import FastAPI

from src.healthcheck.routers import router as healthcheck_router

config.fileConfig(
    fname="logging.ini",
    disable_existing_loggers=False,
)

app = FastAPI(
    title="Mis Eventos",
    description="Service responsible for event management and process automation.",
    version="0.1.0",
)

app.include_router(router=healthcheck_router)
