# fast_mongo TODO API

Simple FastAPI TODO app connected to MongoDB.

## What is included

- `app/main.py`: FastAPI app with health and TODO routes
- `app/db.py`: async Mongo connection and collection helpers
- `app/models.py`: domain entity + document mapping helpers
- `app/schemas.py`: API request/response contracts
- `app/services.py`: persistence orchestration using domain helpers
- `app/routers.py`: HTTP routes under `/todos`
- `scripts/smoke_test.py`: CRUD smoke test harness
- `requirements.txt`: Python dependencies
- `.env.example`: example environment values

## Prerequisites

- Python 3.10+
- MongoDB available at `mongodb://localhost:27017` (your running `rag-mongo` container already matches this)

## Install

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Activate venv (recommended)

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, `python` points to the project environment, so this command works:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Run the API

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/todos`
- `http://127.0.0.1:8000/docs`

## TODO endpoints

- `POST /todos` create todo
- `GET /todos` list todos (optional `?done=true|false`)
- `GET /todos/{todo_id}` get one todo
- `PATCH /todos/{todo_id}` update title/description/done
- `DELETE /todos/{todo_id}` delete todo

Example create request body:

```json
{
  "title": "Buy milk",
  "description": "2 liters"
}
```

## Run smoke test

```powershell
python scripts\smoke_test.py
```

## Run unit tests

```powershell
python -m pytest -q
```

## Optional: start Mongo with compose

```powershell
docker compose up -d
```

