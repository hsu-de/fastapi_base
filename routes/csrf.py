from fastapi import APIRouter, status, Depends, Request, Header, BackgroundTasks
from fastapi_restful.cbv import cbv
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from models.base import ResponseBase
from typing import Annotated
import datetime
# from dependendencies.csrf import depend_csrf # [Depends method]
from dependendencies.base import write_log


# router = APIRouter(
#     prefix='/csrf_token',
#     tags=['csrf_token']
#     # ,dependencies=[Depends(depend_csrf)] # [Depends method]
# )
router = APIRouter()


@cbv(router)
class CSRFRouter:
    background_tasks: BackgroundTasks
    csrf_protect: CsrfProtect = Depends(CsrfProtect)

    @router.get("/get")
    async def get_csrf(self):
        csrf_token, signed_token = self.csrf_protect.generate_csrf_tokens()
        self.background_tasks.add_task(write_log, '{} [csrf_token]{}, {}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), csrf_token, signed_token))
        response = JSONResponse(
            {**ResponseBase(message='Got csrf_token.').model_dump(), 'csrf_token': csrf_token},
            status_code=status.HTTP_200_OK
        )
        self.csrf_protect.set_csrf_cookie(signed_token, response)
        return response

    @router.get("/check")
    async def check_csrf(self, request: Request, XSRF_Token: Annotated[str, Header()]):
        await self.csrf_protect.validate_csrf(request)
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
