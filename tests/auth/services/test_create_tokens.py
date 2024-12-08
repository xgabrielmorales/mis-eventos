import pytest
from fastapi import HTTPException
from sqlmodel import Session

from src.auth.graphql.nodes import AuthDataType
from src.auth.services.create_tokens import JwtAuthentication
from src.users.graphql.nodes import UserInput
from src.users.services.user import UserService
from tests.users.factories.user import UserFactory


class TestCreateTokens:
    def test_user_login_valid_credentials(
        self,
        session: Session,
        user_service: UserService,
    ):
        new_user = UserFactory()
        user_data = UserInput(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            username=new_user.username,
            password=new_user.password,
            role=new_user.role,
        )
        user_service.create(user_data=user_data)

        auth_data = AuthDataType(
            username=new_user.username,
            password=new_user.password,
        )

        jwt_auth = JwtAuthentication(session=session)
        auth_granted_data = jwt_auth.create_auth_tokens(auth_data=auth_data)

        assert isinstance(auth_granted_data.access_token, str)
        assert isinstance(auth_granted_data.refresh_token, str)

    def test_user_login_invalid_credentials(
        self,
        session: Session,
        user_service: UserService,
    ):
        new_user = UserFactory()
        user_data = UserInput(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            username=new_user.username,
            password=new_user.password,
            role=new_user.role,
        )
        user_service.create(user_data=user_data)

        auth_data = AuthDataType(
            username=new_user.username,
            password="Wrong password",
        )

        jwt_auth = JwtAuthentication(session=session)
        with pytest.raises(HTTPException) as exc_info:
            jwt_auth.create_auth_tokens(auth_data=auth_data)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid username or password"
