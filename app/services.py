from app.db import get_todos_collection
from app.models import (
    Todo,
    build_new_todo_document,
    build_update_document,
    parse_todo_id,
    todo_from_document,
)
from app.repository import delete_todo_by_id, find_todo_by_id, find_todos, insert_todo, update_todo_by_id
from app.schemas import TodoCreate, TodoUpdate


class TodoNotFoundError(ValueError):
    pass


class EmptyTodoUpdateError(ValueError):
    pass


def _parse_object_id(todo_id: str):
    return parse_todo_id(todo_id)


async def create_todo(payload: TodoCreate) -> Todo:
    document = build_new_todo_document(payload.title, payload.description)

    collection = await get_todos_collection()
    document = await insert_todo(collection, document)
    return todo_from_document(document)


async def list_todos(done: bool | None = None) -> list[Todo]:
    collection = await get_todos_collection()
    documents = await find_todos(collection, done=done)
    return [todo_from_document(document) for document in documents]


async def get_todo(todo_id: str) -> Todo:
    collection = await get_todos_collection()
    object_id = _parse_object_id(todo_id)
    document = await find_todo_by_id(collection, object_id)
    if document is None:
        raise TodoNotFoundError("Todo not found")

    return todo_from_document(document)


async def update_todo(todo_id: str, payload: TodoUpdate) -> Todo:
    partial_fields = payload.model_dump(exclude_unset=True)
    if not partial_fields:
        raise EmptyTodoUpdateError("At least one field is required for update")

    collection = await get_todos_collection()
    object_id = _parse_object_id(todo_id)

    updates = build_update_document(partial_fields)

    updated_document = await update_todo_by_id(collection, object_id, updates)
    if updated_document is None:
        raise TodoNotFoundError("Todo not found")

    return todo_from_document(updated_document)


async def delete_todo(todo_id: str) -> None:
    collection = await get_todos_collection()
    object_id = _parse_object_id(todo_id)
    was_deleted = await delete_todo_by_id(collection, object_id)
    if not was_deleted:
        raise TodoNotFoundError("Todo not found")

