from datetime import UTC

import pytest

from app.models import (
    InvalidTodoIdError,
    build_new_todo_document,
    build_update_document,
    parse_todo_id,
)


def test_parse_todo_id_rejects_invalid_value() -> None:
    with pytest.raises(InvalidTodoIdError):
        parse_todo_id("not-an-object-id")


def test_build_new_todo_document_sets_defaults() -> None:
    document = build_new_todo_document("Buy milk", "2 liters")

    assert document["title"] == "Buy milk"
    assert document["description"] == "2 liters"
    assert document["done"] is False
    assert document["created_at"].tzinfo == UTC
    assert document["updated_at"].tzinfo == UTC


def test_build_update_document_drops_none_and_keeps_updated_at() -> None:
    document = build_update_document({"title": "New title", "description": None, "done": True})

    assert document["title"] == "New title"
    assert document["done"] is True
    assert "description" not in document
    assert "updated_at" in document

