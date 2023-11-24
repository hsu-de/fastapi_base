from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from schema.mysql import PostBase, UserBase
import models.mysql as mysqlModel
from config.database_mysql import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/mysql',
    tags=['mysql']
)

mysqlModel.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/users/', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = mysqlModel.User(**user.model_dump())
    db.add(db_user)
    db.commit()

    return {
        "success": True,
        "message": "user created."
    }