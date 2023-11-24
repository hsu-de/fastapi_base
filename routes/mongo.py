from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database_mongodb import collection_name
from config.response_sample import responses
from models.mongo import Todo
from schema.mongo import individual_serial, list_serial
from bson import ObjectId

router = APIRouter(
    prefix='/mongo',
    tags=['mongo']
)

# GET
@router.get('/')
async def get_todos():
    todos = list_serial(collection_name.find())
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "todos": todos
        }
    )

# POST
@router.post('/', responses=responses)
async def post_todo(todo: Todo):
    result = collection_name.insert_one(dict(todo))
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "success": True,
            "message": "todo inserted.",
            "todo": {**todo.model_dump(), 'id': str(result.inserted_id)}
        }
    )

# PUT
@router.put('/{todo_id}')
async def put_todo(todo_id:str, todo: Todo):
    result = collection_name.find_one_and_update(
        {"_id": ObjectId(todo_id)},
        {"$set": dict(todo)},
        return_document=True
    )
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": f"todo({todo_id}) not found."
            }
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": f"todo({todo_id}) updated.",
            "todo": individual_serial(result)
        }
    )

# DELETE
@router.delete('/{todo_id}')
async def delete_todo(todo_id: str):
    result = collection_name.find_one_and_delete(
        {"_id": ObjectId(todo_id)}
    )
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": f"todo({todo_id}) not found."
            }
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": f"todo({todo_id}) has been deleted."
        }
    )