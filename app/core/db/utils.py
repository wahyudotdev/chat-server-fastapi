import logging
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .mongodb import database


async def connect_to_database():
    if not database.client:
        logging.info("Connect to te database...")
        database.client = AsyncIOMotorClient(str(MONGODB_URL),
                                             maxPoolSize=MAX_CONNECTIONS_COUNT,
                                             minPoolSize=MIN_CONNECTIONS_COUNT
                                             )
        logging.info("Successful Connection to the database!")


async def close_mongo_connection():
    logging.info("Close the database Connection...")
    database.client.close()
    logging.info("Database Connection is closed")