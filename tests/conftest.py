from collections.abc import Generator

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import Session, create_engine

from src.auth.services.jwt_manager import JwtManager
from src.core.settings import settings
from src.users.repository.user import UserRepository
from src.users.services.user import UserService

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


@pytest.fixture(scope="function", name="authorize")
def jwt_manager():
    return JwtManager()


@pytest.fixture(scope="function")
def user_repository(session: Session) -> UserRepository:
    return UserRepository(session=session)


@pytest.fixture(scope="function")
def user_service(user_repository: Session) -> UserRepository:
    return UserService(user_repository=user_repository)
