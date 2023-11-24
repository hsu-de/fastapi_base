from pydantic import BaseModel

class ResponseBase(BaseModel):
    success: bool = True
    message: str|None = None

class ErrorMessage(ResponseBase):
    errorType: str|None = None
    explain: str|None = None
    details: str|None = None