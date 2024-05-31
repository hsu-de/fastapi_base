from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
from contextlib import contextmanager


engine = create_engine(os.getenv('MYSQL_URL', 'mysql+pymysql://root:rootpassword@localhost:3306/fastapi'))
async_engine = create_async_engine(
    os.getenv('ASYNC_MYSQL_URL', 'mysql+aiomysql://root:rootpassword@localhost:3306/fastapi')
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(SessionLocal)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

Base = declarative_base()


@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()


async def async_get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db


async def init_db():
    Base.metadata.create_all(bind=engine)
