from fastapi import HTTPException, BackgroundTasks, Request, Header, Depends
from fastapi_csrf_protect import CsrfProtect
from typing import Annotated

async def depend_csrf(request: Request, csrf_protect: CsrfProtect = Depends(), XSRF_Token: Annotated[str, Header()]=''):
   await csrf_protect.validate_csrf(request)