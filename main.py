from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes import mongo, mysql, base, csrf
from models.base import ErrorMessage
from models.csrf import CsrfSettings
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from contextlib import asynccontextmanager
from config.database_mysql import init_db
# uvicorn main:app --reload


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Base API",
    version="0.0.1",
    description='''
        Here is the basic FastAPI configuration written by **D.E.**.

        which includes:
        * userData CRUD exsamples using MySQL
        * todo CRUD exsamples using MongoDB

        You can build more endpoints on top of this foundation.
    ''',
    lifespan=lifespan
)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


app.include_router(base.router)
app.include_router(mongo.router)
app.include_router(mysql.router, prefix='/mysql', tags=['mysql'])
app.include_router(csrf.router, prefix='/csrf_token', tags=['csrf_token'])


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(
        ErrorMessage(message='csrf_token check fail.', explain=exc.message).model_dump(),
        status_code=exc.status_code
    )
