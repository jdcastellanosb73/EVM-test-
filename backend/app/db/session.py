from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.db.engine import get_engine


def get_session(engine: Annotated[Engine, Depends(get_engine)]) -> Iterator[Session]:
    with Session(engine) as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_session)]
