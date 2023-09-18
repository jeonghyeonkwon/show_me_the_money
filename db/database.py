from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

from setting import settings

from datetime import datetime
import models

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_url}/{settings.db_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionFactory = sessionmaker(bind=engine)

from models import coin, slack, user, candle


Base.metadata.create_all(bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
