from fastapi import APIRouter, status, Depends, Query, Request
from fastapi_restful.cbv import cbv
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Annotated
from schema.mysql import UserBase, UserSchema
from models.mysql import Base, User, UserDetail
from models.base import ResponseBase, ErrorMessage
from config.database_mysql import engine, get_db, async_get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, desc, asc
import uuid


router = APIRouter()


@cbv(router)
class MySQLRouter:
    # db: Session, Depends(get_db)
    db: AsyncSession = Depends(async_get_db)

    @router.get('/users')
    async def select_user(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        sortBy: Annotated[str, Query()] = 'createdAt',
        sortOrder: Annotated[str, Query()] = 'asc',
    ):

        stmt = select(UserDetail).offset(skip).limit(limit)
        sortOrder = desc if sortOrder.lower() == "desc" else asc
        sorted_stmt = stmt.order_by(sortOrder(getattr(UserDetail, sortBy, UserDetail.createdAt)))
        result = await self.db.execute(sorted_stmt)
        users = result.scalars().all()

        return JSONResponse({**ResponseBase().model_dump(), 'users': jsonable_encoder(users)})

    @router.get('/filter_users')
    async def filter_select_user(
        self,
        request: Request,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        sortBy: Annotated[str, Query()] = 'createdAt',
        sortOrder: Annotated[str, Query()] = 'asc',
    ):

        params = dict(request.query_params)
        stmt = select(UserDetail).offset(skip).limit(limit)
        sortOrder = desc if sortOrder.lower() == "desc" else asc
        sorted_stmt = stmt.order_by(sortOrder(getattr(UserDetail, sortBy, UserDetail.createdAt)))
        # filter
        for key, value in params.items():
            key_name = key.split(':')
            if hasattr(UserDetail, key_name[0]):
                if len(key_name) == 1:
                    sorted_stmt = sorted_stmt.where(getattr(UserDetail, key) == value)
                else:
                    match key_name[1]:
                        case 'lt':
                            sorted_stmt = sorted_stmt.where(getattr(UserDetail, key_name[0]) < value)
                        case 'lte':
                            sorted_stmt = sorted_stmt.where(getattr(UserDetail, key_name[0]) <= value)
                        case 'gt':
                            sorted_stmt = sorted_stmt.where(getattr(UserDetail, key_name[0]) > value)
                        case 'gte':
                            sorted_stmt = sorted_stmt.where(getattr(UserDetail, key_name[0]) >= value)

        result = await self.db.execute(sorted_stmt)
        users = result.scalars().all()

        return JSONResponse({**ResponseBase().model_dump(), 'users': jsonable_encoder(users)})

    @router.post('/user')
    async def insert_user(self, user: UserBase):

        stmt = select(User).where(User.email == user.email)
        result = await self.db.execute(stmt)
        email_check = result.scalar_one_or_none()
        if email_check is not None:
            return JSONResponse(
                ErrorMessage(message='email already existed.', details=f'{user.email}').model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        stmt = insert(UserDetail).values(**user.model_dump())
        result = await self.db.execute(stmt)
        await self.db.commit()
        return JSONResponse(
            {
                **ResponseBase(message='user created.').model_dump(),
                'user': jsonable_encoder({**user.model_dump(), 'id': str(result.inserted_primary_key[0])}),
            },
            status_code=status.HTTP_201_CREATED,
        )

    @router.put('/user/{user_id}')
    async def update_user(self, user_id: str, user: UserSchema):
        user_id = uuid.UUID(user_id)
        stmt = select(UserDetail).where(UserDetail.id == user_id)
        result = await self.db.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            return JSONResponse(
                ErrorMessage(message='user not found.').model_dump(), status_code=status.HTTP_404_NOT_FOUND
            )

        await self.db.reset()  # for reset session's value
        user_data = user.model_dump(exclude_unset=True)
        stmt = update(UserDetail).where(UserDetail.id == user_id).values(user_data)
        await self.db.execute(stmt)
        await self.db.commit()
        return JSONResponse(
            {
                **ResponseBase(message='user updated.').model_dump(),
                # 'user': jsonable_encoder({**user.model_dump(), 'id': db_user.id, 'createdAt': db_user.createdAt}),
            },
            status_code=status.HTTP_200_OK,
        )

    @router.delete('/user/{user_id}')
    async def delete_user(self, user_id: str):
        user_id = uuid.UUID(user_id)
        stmt = select(UserDetail).where(UserDetail.id == user_id)
        result = await self.db.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            return JSONResponse(
                ErrorMessage(message='user not found.').model_dump(), status_code=status.HTTP_404_NOT_FOUND
            )

        stmt = delete(UserDetail).where(UserDetail.id == user_id)
        await self.db.execute(stmt)
        await self.db.commit()
        return JSONResponse(ResponseBase(message='user deleted.').model_dump(), status_code=status.HTTP_200_OK)
