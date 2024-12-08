import pytest
from sqlmodel import Session

from src.users.repository.user import UserRepository


@pytest.fixture(scope="function")
def user_repository(session: Session) -> UserRepository:
    return UserRepository(session=session)
