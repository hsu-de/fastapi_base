from pydantic import BaseModel, EmailStr, Field

# pip install pydantic[email]
from datetime import datetime


class UserBase(BaseModel):
    displayName: str
    password: str
    email: EmailStr

    # class Config:
    #     json_schema_extra = {
    #         "examples": [
    #             {
    #                 "username": "user01",
    #                 "password": "user01_password",
    #                 "email": "user01@example.com"
    #             }
    #         ]
    #     }


class UserSchema(UserBase):
    birthday: datetime
    role: int = Field(default=0, description="role id of user", ge=0, lt=2)
    accountLevel: int
    isRecommended: bool


# class PostBase(BaseModel):
#     title: str
#     content: str
#     user_id: int
