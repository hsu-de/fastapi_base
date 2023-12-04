from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Annotated
from config.database_mongodb import db, async_db
from config.response_sample import responses
from models.mongo import Todo
from models.base import ResponseBase, ErrorMessage
from schema.mongo import individual_serial, list_serial
from bson import ObjectId

router = APIRouter(
    prefix='/mongo',
    tags=['mongo']
)

# GET
@router.get('/todos')
async def get_todos(skip: Annotated[int, Query(ge=0)] = 0,
                    limit: Annotated[int, Query(ge=1, le=100)] = 20):
    # todos = list_serial(db.todo_collection.find())
    cursor = async_db.todo_collection.find().skip(skip).limit(limit)
    result = await cursor.to_list(limit)

    return JSONResponse(
        {**ResponseBase().model_dump(), 'todos': list_serial(result)},
        status_code=status.HTTP_200_OK
    )

# POST
@router.post('/todo')
async def post_todo(todo: Todo):
    result = db.todo_collection.insert_one(dict(todo))

    return JSONResponse(
        {**ResponseBase(message='todo inserted.').model_dump(), 'todo': {**todo.model_dump(), 'id': str(result.inserted_id)}},
        status_code=status.HTTP_201_CREATED
    )

# PUT
@router.put('/todo/{todo_id}')
async def put_todo(todo_id:str, todo: Todo):
    result = db.todo_collection.find_one_and_update(
        {"_id": ObjectId(todo_id)},
        {"$set": dict(todo)},
        return_document=True
    )
    if not result:
        return JSONResponse(
            ErrorMessage(message=f'todo not found.', details=todo_id).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(
        {**ResponseBase(message=f'todo({todo_id}) updated.').model_dump(), 'todo': individual_serial(result)},
        status_code=status.HTTP_200_OK
    )

# DELETE
@router.delete('/todo/{todo_id}')
async def delete_todo(todo_id: str):
    result = db.todo_collection.find_one_and_delete(
        {"_id": ObjectId(todo_id)}
    )
    if not result:
        return JSONResponse(
            ErrorMessage(message=f'todo not found.', details=todo_id).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(
        ResponseBase(message=f'todo({todo_id}) has been deleted.').model_dump(),
        status_code=status.HTTP_200_OK
    )