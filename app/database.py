from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

DATABASE_URL = 'sqlite:///./blog.db'

engine = create_engine(DATABASE_URL,connect_args = {
    'check_same_thread':False
})

SessionLocal = sessionmaker(
    autocommit=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass