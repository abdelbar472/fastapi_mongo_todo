import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.db import close_mongo, connect_to_mongo, ping_mongo
from app.models import InvalidTodoIdError
from app.routers import router as todos_router
from app.services import EmptyTodoUpdateError, TodoNotFoundError


# Open Mongo on startup and always close it on shutdown.
@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo()


app = FastAPI(title="fast_mongo", version="0.1.0", lifespan=lifespan)
app.include_router(todos_router)


@app.exception_handler(InvalidTodoIdError)
async def invalid_todo_id_handler(_: Request, exc: InvalidTodoIdError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(TodoNotFoundError)
async def todo_not_found_handler(_: Request, exc: TodoNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(EmptyTodoUpdateError)
async def empty_todo_update_handler(_: Request, exc: EmptyTodoUpdateError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "fast_mongo TODO API is running"}


@app.get("/health")
async def health() -> dict[str, bool | str]:
    # Report API health and whether Mongo is reachable right now.
    mongo_ok = await ping_mongo()
    return {
        "status": "ok" if mongo_ok else "degraded",
        "mongo": mongo_ok,
    }


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))

    import uvicorn

    uvicorn.run("app.main:app", host=host, port=port, reload=True)

