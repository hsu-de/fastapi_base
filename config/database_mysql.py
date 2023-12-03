from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_engine('mysql+pymysql://root:rootpassword@localhost:3306/fastapi')
async_engine = create_async_engine('mysql+aiomysql://root:rootpassword@localhost:3306/fastapi')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def async_get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()