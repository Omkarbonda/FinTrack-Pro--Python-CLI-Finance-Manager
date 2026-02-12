from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_NAME = 'fintrack.db'
Base = declarative_base()

def init_db():
    engine = create_engine(f'sqlite:///{DB_NAME}')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
