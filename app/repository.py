from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection


async def insert_todo(collection: AsyncIOMotorCollection, document: dict[str, Any]) -> dict[str, Any]:
    result = await collection.insert_one(document)
    document["_id"] = result.inserted_id
    return document


async def find_todos(
    collection: AsyncIOMotorCollection, *, done: bool | None = None, limit: int = 100
) -> list[dict[str, Any]]:
    filter_query: dict[str, Any] = {}
    if done is not None:
        filter_query["done"] = done

    cursor = collection.find(filter_query).sort("created_at", -1)
    return await cursor.to_list(length=limit)


async def find_todo_by_id(collection: AsyncIOMotorCollection, object_id: ObjectId) -> dict[str, Any] | None:
    return await collection.find_one({"_id": object_id})


async def update_todo_by_id(
    collection: AsyncIOMotorCollection,
    object_id: ObjectId,
    updates: dict[str, Any],
) -> dict[str, Any] | None:
    await collection.update_one({"_id": object_id}, {"$set": updates})
    return await collection.find_one({"_id": object_id})


async def delete_todo_by_id(collection: AsyncIOMotorCollection, object_id: ObjectId) -> bool:
    result = await collection.delete_one({"_id": object_id})
    return result.deleted_count > 0

