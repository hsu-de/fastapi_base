from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Annotated
from schema.mysql import UserBase, UserSchema
from models.mysql import Base, User, UserDetail
from models.base import ResponseBase, ErrorMessage
from config.database_mysql import engine, get_db, async_get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid



router = APIRouter(
    prefix='/mysql',
    tags=['mysql']
)

Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]
async_db_dependency = Annotated[AsyncSession, Depends(async_get_db)]

@router.get('/users')
async def select_user(db: async_db_dependency,
                      skip: Annotated[int, Query(ge=0)] = 0,
                      limit: Annotated[int, Query(ge=1, le=100)] = 20):
    # users = db.query(UserDetail).offset(skip).limit(limit).all()
    query = select(UserDetail).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return JSONResponse(
        {**ResponseBase().model_dump(), 'users': jsonable_encoder(users)}
    )

@router.post('/user')
async def insert_user(user: UserBase,
                      db: db_dependency):
    email_check = db.query(User).filter(User.email == user.email).first()
    if email_check != None:
        return JSONResponse(
            ErrorMessage(message='email already existed.', details=f'{user.email}').model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    db_user = UserDetail(**user.model_dump())
    db.add(db_user)
    db.commit()

    return JSONResponse(
        {**ResponseBase(message='user created.').model_dump(), 'user': jsonable_encoder({**user.model_dump(), 'id': db_user.id, 'createdAt': db_user.createdAt})},
        status_code=status.HTTP_201_CREATED
    )

@router.put('/user/{user_id}')
async def update_user(user_id: str,
                      user: UserSchema,
                      db: db_dependency):
    user_id = uuid.UUID(user_id)
    db_user = db.query(UserDetail).filter(UserDetail.id == user_id).first()
    if not db_user:
        raise JSONResponse(
            ErrorMessage(message='user not found.').model_dump(),
            status_code=status.HTTP_404_NOT_FOUND
        )
    user_data = user.model_dump(exclude_unset=True)
    db.query(UserDetail).filter(UserDetail.id == user_id).update(user_data)
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