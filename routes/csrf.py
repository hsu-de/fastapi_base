from fastapi import APIRouter, HTTPException, status, Depends, Request, Header, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from models.base import ResponseBase
from typing import Annotated
import datetime
# from dependendencies.csrf import depend_csrf # [Depends method]
from dependendencies.base import write_log


router = APIRouter(
    prefix='/csrf_token',
    tags=['csrf_token']
    # ,dependencies=[Depends(depend_csrf)] # [Depends method]
)

@router.get("/get")
async def get_csrf(background_tasks: BackgroundTasks, csrf_protect: CsrfProtect = Depends()):
   csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
   background_tasks.add_task(write_log, '{} [csrf_token]{}, {}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), csrf_token, signed_token))
   response = JSONResponse(
        {**ResponseBase(message='Got csrf_token.').model_dump(), 'csrf_token': csrf_token},
        status_code=status.HTTP_200_OK
   )
   csrf_protect.set_csrf_cookie(signed_token, response)
   return response

@router.get("/check")
async def check_csrf(request: Request, XSRF_Token: Annotated[str, Header()], csrf_protect: CsrfProtect = Depends()):
   await csrf_protect.validate_csrf(request)
   return JSONResponse(
        {**ResponseBase(message='csrf_token check ok!').model_dump()},
        status_code=status.HTTP_200_OK
   )

# [Depends method]
# @router.get("/depend_csrf_check")
# async def depend_check_csrf():
#    return JSONResponse(
#         {**ResponseBase(message='csrf_token check ok!').model_dump()},
#         status_code=status.HTTP_200_OK
#    )