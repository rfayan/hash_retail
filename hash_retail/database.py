from os import environ
from typing import Iterator
from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

PG_USER = environ["DATABASE_USERNAME"]
PG_PASS = quote(environ["DATABASE_PASSWORD"])
PG_HOST = environ["DATABASE_HOST"]
PG_PORT = environ["DATABASE_PORT"]
PG_DB = environ["DATABASE_NAME"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Verify if all tables exist. If they do not, create them
def verify_and_create_db_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Iterator[Session]:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
