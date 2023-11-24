from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Annotated
from schema.mysql import UserBase
from models.mysql import Base, User, UserDetail
from models.base import ResponseBase, ErrorMessage
from config.database_mysql import engine, get_db
from sqlalchemy.orm import Session
import uuid

router = APIRouter(
    prefix='/mysql',
    tags=['mysql']
)

Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/users')
async def select_user(db: db_dependency,
                      skip: Annotated[int, Query(ge=0)] = 0,
                      limit: Annotated[int, Query(ge=1, le=100)] = 20):
    users = db.query(User).offset(skip).limit(limit).all()
    
    return JSONResponse(
        {**ResponseBase().model_dump(), 'users': jsonable_encoder(users)}
    )

@router.post('/user')
async def insert_user(user: UserBase,
                      db: db_dependency):
    db_user = UserDetail(**user.model_dump())
    db.add(db_user)
    db.commit()

    return JSONResponse(
        {**ResponseBase(message='user created.').model_dump(), 'user': jsonable_encoder({**user.model_dump(), 'id': db_user.id, 'createdAt': db_user.createdAt})},
        status_code=status.HTTP_201_CREATED
    )

@router.put('/user/{user_id}')
async def update_user(user_id: str,
                      user: UserBase,
                      db: db_dependency):
    user_id = uuid.UUID(user_id)
    db_user = db.query(UserDetail).filter(User.id == user_id).first()
    if not db_user:
        raise JSONResponse(
            ErrorMessage(message='user not found.').model_dump(),
            status_code=status.HTTP_404_NOT_FOUND
        )
    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email
    # 先寫死，再查查看更好的寫法
    db.commit()

    return JSONResponse(
        {**ResponseBase(message='user updated.').model_dump(), 'user': jsonable_encoder({**user.model_dump(), 'id': db_user.id, 'createdAt': db_user.createdAt})},
        status_code=status.HTTP_200_OK
    )

@router.delete('/user/{user_id}')
async def delete_user(user_id: str,
                      db: db_dependency):
    user_id = uuid.UUID(user_id)
    db_user = db.query(UserDetail).filter(User.id == user_id).first()
    if not db_user:
        raise JSONResponse(
            ErrorMessage(message='user not found.').model_dump(),
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(db_user)
    db.commit()

    return JSONResponse(
        ResponseBase(message='user deleted.').model_dump(),
        status_code=status.HTTP_200_OK
    )