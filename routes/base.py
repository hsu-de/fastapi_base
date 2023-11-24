from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.base import ResponseBase, ErrorMessage

router = APIRouter()

@router.get("/")
async def read_root():
    response = ResponseBase(
        message='Hello FastAPI.'
    )
    return JSONResponse(
        {**jsonable_encoder(response), 'object': 'object content'},
        status_code=status.HTTP_200_OK
    )

@router.get("/error")
async def error_message():
    response = ErrorMessage(
        success=False,
        message='Error response.'
    )
    return JSONResponse(
        jsonable_encoder(response),
        status_code=status.HTTP_400_BAD_REQUEST
    )