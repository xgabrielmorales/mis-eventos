import pytest
from fastapi.exceptions import HTTPException
from sqlmodel import Session

from src.users.graphql.nodes import UserInput, UserInputUpdate
from src.users.repository.user import UserRepository
from src.users.services.user import UserService
from tests.users.factories.user import UserFactory


class TestUserService:
    def test_get_by_id(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        new_user = UserFactory()
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        user_service = UserService(repository=user_repository)
        user = user_service.get_by_id(user_id=new_user.id)

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
        user_service = UserService()

        try:
            user_service.get_by_id(user_id=999)
        except HTTPException as e:
            assert e.status_code == 404
            assert e.detail == "User does not exist or cannot be found."

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

        user_service = UserService(repository=user_repository)
        fetched_users = user_service.get_all()

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
        user_data = UserInput(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            username=new_user.username,
            password=new_user.password,
            role=new_user.role,
        )

        user_service = UserService(repository=user_repository)
        created_user = user_service.create(user_data=user_data)

        assert created_user.id is not None
        assert created_user.first_name == user_data.first_name
        assert created_user.last_name == user_data.last_name
        assert created_user.username == user_data.username
        assert created_user.role == user_data.role

    def test_update(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        user = UserFactory()
        session.add(user)
        session.commit()
        session.refresh(user)

        user_data = UserInputUpdate(
            first_name="Updated",
            last_name=None,
            username=None,
            password=None,
            role=None,
        )

        user_service = UserService(repository=user_repository)
        updated_user = user_service.update(user_id=user.id, user_data=user_data)

        assert updated_user.first_name == "Updated"

    def test_update_not_found(
        self,
        user_repository: UserRepository,
    ) -> None:
        user_data = UserInputUpdate(
            first_name="Updated",
            last_name=None,
            username=None,
            password=None,
            role=None,
        )

        user_service = UserService(repository=user_repository)
        with pytest.raises(HTTPException) as exc_info:
            user_service.update(user_id=999, user_data=user_data)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User does not exist or cannot be found."

    def test_delete(
        self,
        session: Session,
        user_repository: UserRepository,
    ) -> None:
        user = UserFactory()
        session.add(user)
        session.commit()
        session.refresh(user)

        user_service = UserService(repository=user_repository)
        response = user_service.delete(user_id=user.id)

        assert response == "User deleted successfully"

        deleted_user = user_repository.get_by_id(instance_id=user.id)

        assert deleted_user is None

    def test_delete_not_found(
        self,
        user_repository: UserRepository,
    ) -> None:
        user_service = UserService(repository=user_repository)

        with pytest.raises(HTTPException) as exc_info:
            user_service.delete(user_id=999)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User does not exist or cannot be found."
