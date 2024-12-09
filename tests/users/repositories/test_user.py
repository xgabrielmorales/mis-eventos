import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session

from src.users.repository.user import UserRepository
from tests.users.factories.user import UserFactory


class TestUserRepository:
    def test_get_by_id(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        new_user = UserFactory()
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        user = user_repository.get_by_id(instance_id=new_user.id)

        assert user is not None
        assert user.id == new_user.id
        assert user.first_name == new_user.first_name
        assert user.last_name == new_user.last_name
        assert user.username == new_user.username
        assert user.role == new_user.role

    def test_get_by_id_not_found(
        self,
        user_repository: UserRepository,
    ) -> None:
        user = user_repository.get_by_id(instance_id=9999)
        assert user is None

    def test_get_all(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        user_1 = UserFactory()
        session.add(user_1)

        user_2 = UserFactory()
        session.add(user_2)
        session.commit()

        fetched_users = user_repository.get_all()

        assert len(fetched_users) == 2

        assert fetched_users[0].first_name == user_1.first_name
        assert fetched_users[0].last_name == user_1.last_name
        assert fetched_users[0].role == user_1.role

        assert fetched_users[1].first_name == user_2.first_name
        assert fetched_users[1].last_name == user_2.last_name
        assert fetched_users[1].role == user_2.role

    def test_create(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        new_user = UserFactory()
        created_user = user_repository.create(new_user)

        assert created_user.id is not None
        assert created_user.first_name == new_user.first_name
        assert created_user.last_name == new_user.last_name
        assert created_user.username == new_user.username
        assert created_user.role == new_user.role

    def test_create_duplicate_username(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        user_1 = UserFactory()
        user_repository.create(user_1)

        user_2 = UserFactory(username=user_1.username)
        with pytest.raises(IntegrityError):
            user_repository.create(user_2)

    def test_update(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        user = UserFactory()
        user_repository.create(user)

        user = user_repository.get_by_id(instance_id=user.id)
        user.first_name = "UpdatedName"

        updated_user = user_repository.update(user)

        assert updated_user.first_name == "UpdatedName"

    def test_delete(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        user = UserFactory()
        user_repository.create(user)

        user = user_repository.get_by_id(instance_id=user.id)

        user_repository.delete(user)

        deleted_user = user_repository.get_by_id(instance_id=user.id)

        assert deleted_user is None

    def test_delete_nonexistent_user(
        self,
        user_repository: UserRepository,
    ) -> None:
        nonexistent_user = UserFactory(id=9999)
        with pytest.raises(SQLAlchemyError):
            user_repository.delete(nonexistent_user)

    def test_create_missing_fields(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        incomplete_user = UserFactory(first_name=None)
        with pytest.raises(IntegrityError):
            user_repository.create(incomplete_user)

    def test_get_all_empty(
        self,
        user_repository: UserRepository,
    ) -> None:
        fetched_users = user_repository.get_all()
        assert fetched_users == []
