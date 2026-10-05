from fastapi import Request
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

CONNECTIVITY_PROBE = text("SELECT 1")


def create_db_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True)


def get_engine(request: Request) -> Engine:
    engine: Engine = request.app.state.engine
    return engine


def is_database_reachable(engine: Engine) -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(CONNECTIVITY_PROBE)
    except SQLAlchemyError:
        return False
    return True
