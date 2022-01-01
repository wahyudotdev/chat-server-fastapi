import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.core.db.utils import close_mongo_connection, connect_to_database
from app.core.config import config
from app.api.v1.router import router

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Chat API",
    openapi_url= config.API_V1_STR + "/openapi.json",
    docs_url= config.API_V1_STR + "/docs",
    redoc_url= config.API_V1_STR + "/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_event_handler("startup", connect_to_database)
@app.on_event("startup")
async def startup_event():
    await connect_to_database()

app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(router, prefix=config.API_V1_STR)
