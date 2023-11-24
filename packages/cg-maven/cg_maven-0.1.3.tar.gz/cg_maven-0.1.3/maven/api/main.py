import logging

from fastapi import FastAPI

from maven.api.endpoints.case import case_router
from maven.maven_db.client_connection import get_client
from maven.maven_db.config import Config, connection_config

app = FastAPI()

LOG = logging.getLogger("__name__")


@app.get("/")
async def root():
    return {"message": "Welcome to Maven :) "}


@app.on_event("startup")
def startup_db_client(config: Config = connection_config):
    app.mongodb_client = get_client(config)


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(case_router, prefix="/api", tags=["case"])
