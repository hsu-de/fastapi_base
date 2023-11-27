from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.base import ResponseBase, ErrorMessage

router = APIRouter()

@router.get("/")
async def read_root():
    return JSONResponse(
        {**ResponseBase(message='Hello FastAPI.').model_dump(), 'object': 'object content'},
        status_code=status.HTTP_200_OK
    )

@router.get("/error")
async def error_message():
    return JSONResponse(
        ErrorMessage(message='Error response.').model_dump(),
        status_code=status.HTTP_400_BAD_REQUEST
    )