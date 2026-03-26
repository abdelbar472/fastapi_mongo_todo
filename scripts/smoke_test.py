import asyncio
import sys
from pathlib import Path

# Ensure local package imports work when running this script directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import close_mongo, get_todos_collection, ping_mongo
from app.schemas import TodoCreate, TodoUpdate
from app.services import create_todo, delete_todo, get_todo, list_todos, update_todo


async def _run() -> int:
    try:
        mongo_ok = await ping_mongo()
        if not mongo_ok:
            print("Mongo connectivity: FAILED")
            return 1

        print("Mongo connectivity: OK")
        collection = await get_todos_collection()
        await collection.delete_many({})

        created = await create_todo(TodoCreate(title="first todo", description="from smoke test"))
        fetched = await get_todo(created.id)
        updated = await update_todo(created.id, TodoUpdate(done=True))
        listed = await list_todos(done=True)
        await delete_todo(created.id)

        print(f"Created todo id: {created.id}")
        print(f"Fetched title: {fetched.title}")
        print(f"Updated done: {updated.done}")
        print(f"Completed todos found: {len(listed)}")
        return 0
    finally:
        await close_mongo()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_run()))

