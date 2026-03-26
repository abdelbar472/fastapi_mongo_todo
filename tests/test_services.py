import pytest

from app.schemas import TodoUpdate
from app.services import EmptyTodoUpdateError, update_todo


@pytest.mark.asyncio
async def test_update_todo_rejects_empty_patch_payload() -> None:
    with pytest.raises(EmptyTodoUpdateError):
        await update_todo("65f1f0f0f0f0f0f0f0f0f0f0", TodoUpdate())

