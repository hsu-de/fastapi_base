from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes import mongo, mysql, base, csrf

from models.base import ErrorMessage
from models.csrf import CsrfSettings
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

# uvicorn main:app --reload

app = FastAPI(
    title="Base API",
    version="0.0.1",
    description='''
        Here is the basic FastAPI configuration written by **D.E.**.
        
        which includes:
        * userData CRUD exsamples using MySQL
        * todo CRUD exsamples using MongoDB

        You can build more endpoints on top of this foundation.
    '''
)

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

app.include_router(base.router)
app.include_router(mongo.router)
app.include_router(mysql.router)
app.include_router(csrf.router)

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(
        ErrorMessage(message='csrf_token check fail.', explain=exc.message).model_dump(),
        status_code=exc.status_code
    )