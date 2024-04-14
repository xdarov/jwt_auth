import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

db_user = "postgres"
db_pass = os.environ.get("POSTGRES_PASSWORD", "strongpassword")
db_host = os.environ.get("POSTGRES_HOST", "localhost")
db_port = os.environ.get("POSTGRES_PORT", 45432) 
db_name = "postgres"
db_connection = f'postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

engine = create_engine(db_connection)
Base.metadata.create_all(engine)

async_engine = create_async_engine(db_connection, echo=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, future=True)
 