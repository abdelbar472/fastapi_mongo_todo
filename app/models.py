from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId


class InvalidTodoIdError(ValueError):
    pass


@dataclass(frozen=True)
class Todo:
    id: str
    title: str
    description: str | None
    done: bool
    created_at: datetime
    updated_at: datetime


def parse_todo_id(todo_id: str) -> ObjectId:
    try:
        return ObjectId(todo_id)
    except (InvalidId, TypeError):
        raise InvalidTodoIdError("Invalid todo id format")


def build_new_todo_document(title: str, description: str | None) -> dict[str, Any]:
    now = datetime.now(UTC)
    return {
        "title": title,
        "description": description,
        "done": False,
        "created_at": now,
        "updated_at": now,
    }


def build_update_document(fields: dict[str, Any]) -> dict[str, Any]:
    updates = {key: value for key, value in fields.items() if value is not None}
    updates["updated_at"] = datetime.now(UTC)
    return updates


def todo_from_document(document: dict[str, Any]) -> Todo:
    return Todo(
        id=str(document["_id"]),
        title=document["title"],
        description=document.get("description"),
        done=document.get("done", False),
        created_at=document["created_at"],
        updated_at=document["updated_at"],
    )
