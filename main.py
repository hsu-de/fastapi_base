from fastapi import FastAPI
from routes import mongo, mysql, base

# uvicorn main:app --reload

app = FastAPI(
    title="Base API",
    version="0.0.1",
    description='''
        Base setting for DE with FastAPI.
        Example:
            userData with mysql
            todo with mongoDB
    '''
)

app.include_router(base.router)
app.include_router(mongo.router)
app.include_router(mysql.router)