from fastapi import APIRouter, status

from app.schemas import TodoCreate, TodoOut, TodoUpdate, todo_to_out
from app.services import create_todo, delete_todo, get_todo, list_todos, update_todo

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
async def create_todo_endpoint(payload: TodoCreate) -> TodoOut:
    todo = await create_todo(payload)
    return todo_to_out(todo)


@router.get("", response_model=list[TodoOut])
async def list_todos_endpoint(done: bool | None = None) -> list[TodoOut]:
    todos = await list_todos(done=done)
    return [todo_to_out(todo) for todo in todos]


@router.get("/{todo_id}", response_model=TodoOut)
async def get_todo_endpoint(todo_id: str) -> TodoOut:
    todo = await get_todo(todo_id)
    return todo_to_out(todo)


@router.patch("/{todo_id}", response_model=TodoOut)
async def update_todo_endpoint(todo_id: str, payload: TodoUpdate) -> TodoOut:
    todo = await update_todo(todo_id, payload)
    return todo_to_out(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_endpoint(todo_id: str) -> None:
    await delete_todo(todo_id)
