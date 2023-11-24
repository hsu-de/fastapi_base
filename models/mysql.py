from sqlalchemy import Uuid, Boolean, Column, Integer, String, DateTime
# from sqlalchemy.dialects.postgresql import UUID
from config.database_mysql import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = 'userData'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    username = Column(String(64), unique=True)
    email = Column(String(128), unique=True)
    createdAt = Column(DateTime, default=datetime.utcnow)

class UserDetail(User):
    __tablename__ = 'userData'
    __table_args__ = {'extend_existing': True} # 使用 extend_existing=True 來擴展現有的資料表定義

    password = Column(String(256))
    birthday = Column(DateTime)
    accountLevel = Column(Integer, default=0)
    isRecommended = Column(Boolean, default=False)

# class Post(Base):
#     __tablename__ = 'posts'

#     id = Column(Uuid, primary_key=True, default=uuid.uuid4)
#     title = Column(String(64))
#     content = Column(String(128))
#     user_id = Column(Uuid)