from datetime import datetime

from pydantic import BaseModel, Field

from app.models import Todo


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    done: bool | None = None


class TodoOut(BaseModel):
    id: str
    title: str
    description: str | None
    done: bool
    created_at: datetime
    updated_at: datetime


def todo_to_out(todo: Todo) -> TodoOut:
    return TodoOut(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        done=todo.done,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )


