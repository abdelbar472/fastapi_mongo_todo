import os
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase


# Reuse one async client across the app process.
_mongo_client: Optional[AsyncIOMotorClient] = None


def get_mongo_uri() -> str:
    return os.getenv("MONGO_URI", "mongodb://localhost:27017")


def get_mongo_db_name() -> str:
    return os.getenv("MONGO_DB", "fast_mongo")


async def connect_to_mongo() -> AsyncIOMotorClient:
    global _mongo_client

    if _mongo_client is None:
        # Keep timeout short so startup and health checks fail quickly when DB is down.
        _mongo_client = AsyncIOMotorClient(get_mongo_uri(), serverSelectionTimeoutMS=2000)

    # Force a quick round trip so startup fails fast when Mongo is unavailable.
    await _mongo_client.admin.command("ping")
    return _mongo_client


async def close_mongo() -> None:
    global _mongo_client

    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None


async def ping_mongo() -> bool:
    try:
        client = await connect_to_mongo()
        await client.admin.command("ping")
        return True
    except Exception:
        # Health endpoints should degrade gracefully instead of crashing the API.
        return False


async def get_database() -> AsyncIOMotorDatabase:
    client = await connect_to_mongo()
    return client[get_mongo_db_name()]


async def get_todos_collection() -> AsyncIOMotorCollection:
    database = await get_database()
    return database["todos"]


