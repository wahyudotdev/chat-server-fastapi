import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT, database_name


class Database:
    client: AsyncIOMotorClient = None


database = Database()


async def get_db_client():
    return database.client


def get_database(dbname: str = None) -> AsyncIOMotorDatabase:
    if not database.client:
        logging.info("Connect to Database....")
        database.client = AsyncIOMotorClient(str(MONGODB_URL),
                                             maxPoolSize=MAX_CONNECTIONS_COUNT,
                                             minPoolSize=MIN_CONNECTIONS_COUNT)
        logging.info("Successful Connection to the database")

    return database.client[dbname] if dbname else database.client[database_name]
