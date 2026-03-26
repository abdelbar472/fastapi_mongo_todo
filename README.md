# fast_mongo TODO API

Small, maintainable TODO API built with FastAPI + MongoDB (Motor async driver).

## Features

- Async FastAPI app with MongoDB persistence
- Layered design: routers -> services -> repository -> database
- Domain logic isolated in `app/models.py`
- Health endpoint with Mongo connectivity status
- Postman collection included for quick API testing

## Tech stack

- Python 3.10+
- FastAPI
- Uvicorn
- MongoDB + Motor
- Pytest (+ `pytest-asyncio`)

## Project structure

```text
fast_mongo/
  app/
    main.py        # app bootstrap + lifespan + exception mapping
    db.py          # Mongo client/database/collection helpers
    models.py      # domain model + id/document helpers
    schemas.py     # request/response DTOs (Pydantic)
    repository.py  # raw Mongo operations
    services.py    # use cases/business flow
    routers.py     # HTTP endpoints (/todos)
  scripts/
    smoke_test.py  # end-to-end CRUD smoke test
  tests/
    test_models.py
    test_services.py
  docker-compose.yml
  fast_mongo.postman_collection.json
  requirements.txt
```

## Quick start (Windows / PowerShell)

### 1) Start MongoDB

If you already run Mongo on `localhost:27017` (for example container `rag-mongo`), skip this.

```powershell
docker compose up -d
```

### 2) Create and activate virtual environment

```powershell
Set-Location "D:\codes\fast_mongo"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4) Run API (your preferred command)

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

> Important: run the command after activating `.venv`. If not, global Python may be used and can fail with `ModuleNotFoundError: No module named 'motor'`.

## Configuration

Defaults from `app/db.py` and `app/main.py`:

- `MONGO_URI` (default: `mongodb://localhost:27017`)
- `MONGO_DB` (default: `fast_mongo`)
- `HOST` (default: `127.0.0.1`)
- `PORT` (default: `8000`)

Set env vars in PowerShell before run:

```powershell
$env:MONGO_URI = "mongodb://localhost:27017"
$env:MONGO_DB = "fast_mongo"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## API endpoints

- `GET /` - basic service message
- `GET /health` - API + Mongo health
- `POST /todos` - create todo
- `GET /todos` - list todos
- `GET /todos?done=true|false` - filter by completion
- `GET /todos/{todo_id}` - get one todo
- `PATCH /todos/{todo_id}` - partial update (`title`, `description`, `done`)
- `DELETE /todos/{todo_id}` - delete todo

Example create body:

```json
{
  "title": "Buy milk",
  "description": "2 liters"
}
```

## Postman collection

Import `fast_mongo.postman_collection.json` into Postman.

- Collection variable `baseUrl` defaults to `http://127.0.0.1:8000`
- `Create Todo` request auto-saves returned id into `todoId`
- Then run `Get/Update/Delete` using `{{todoId}}`

## Tests

Run smoke test (real Mongo required):

```powershell
python scripts\smoke_test.py
```

Run unit tests:

```powershell
python -m pytest -q
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'motor'`

You are likely using global Python instead of project `.venv`.

```powershell
Set-Location "D:\codes\fast_mongo"
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### API not reachable on port 8000

```powershell
netstat -ano | findstr :8000
```

If no listener appears, restart uvicorn and check startup logs.

