from fastapi import FastAPI
from routes import todo, mysql

# uvicorn main:app --reload

app = FastAPI(
    title="Base API",
    description="Base setting for DE with FastAPI",
    version="0.0.1"
)

app.include_router(todo.router)
app.include_router(mysql.router)