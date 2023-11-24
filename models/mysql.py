from sqlalchemy import Uuid, Boolean, Column, Integer, String
# from sqlalchemy.dialects.postgresql import UUID
from config.database_mysql import Base
import uuid

class User(Base):
    __tablename__ = 'userData'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    username = Column(String(64), unique=True)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String(64))
    content = Column(String(128))
    user_id = Column(Uuid)