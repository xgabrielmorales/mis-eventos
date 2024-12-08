from collections.abc import Generator

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import Session, create_engine

from src.core.settings import settings

engine = create_engine(
    url=settings.POSTGRES_URL,  # type: ignore[arg-type]
    echo=False,
    poolclass=NullPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=Session,
)


@pytest.fixture(scope="function", name="session")
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
