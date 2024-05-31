from sqlalchemy import Uuid, Boolean, Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy_util import URLType
from config.database_mysql import Base
import uuid, enum

from .mixins import Timestamp


class Role(enum.IntEnum):
    no_setting = 0
    normal = 1
    creator = 2
    super_user = 3


class User(Base):
    __tablename__ = 'userData'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    displayName = Column(String(64), unique=True)
    email = Column(String(128), unique=True, nullable=False)

    post = relationship('Post', back_populates='creator')


class UserDetail(Timestamp, User):
    __tablename__ = 'userData'
    __table_args__ = {'extend_existing': True}  # 使用 extend_existing=True 來擴展現有的資料表定義

    password = Column(String(256))
    birthday = Column(DateTime)
    role = Column(Enum(Role), default=1)
    accountLevel = Column(Integer, default=0)
    isRecommended = Column(Boolean, default=False)


class Post(Timestamp, Base):
    __tablename__ = 'posts'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String(64), nullable=False)
    content = Column(String(256))
    user_id = Column(Uuid, ForeignKey('userData.id'), nullable=False)

    creator = relationship('User', back_populates='post')
