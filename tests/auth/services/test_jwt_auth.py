from datetime import datetime, timedelta
from unittest.mock import MagicMock

import jwt
import pytest

from src.auth.schemas import TokenData
from src.auth.services.jwt_exceptions import (
    AuthJwtAccessTokenRequired,
    AuthJwtDecodeError,
    AuthJwtRefreshTokenRequired,
    InvalidHeaderError,
)
from src.auth.services.jwt_manager import JwtManager
from src.core.settings import settings


class TestAuthJWTService:
    def test_constructor(self):
        request = MagicMock()
        request.headers = {
            "authorization": "Bearer eyJhbGciOiIsIn9.eyJG4gRG9lINDIyfQ.Sfl36POk6yJV_adQssw5c",
        }

        authorize = JwtManager(request=request)

        assert authorize.token == request.headers["authorization"].split()[1]

    def test_jwt_identifier(self, authorize: JwtManager):
        assert isinstance(authorize._get_jwt_identifier(), str)

    def test_jwt_from_headers(self, authorize: JwtManager):
        authorization_header = "Bearer eyJhbGciOiIsIn9.eyJG4gRG9lINDIyfQ.Sfl36POk6yJV_adQssw5c"
        authorize._get_jwt_from_headers(auth=authorization_header)
        assert authorize.token == authorization_header.split()[1]

    def test_invalid_jwt_from_headers(self, authorize: JwtManager):
        with pytest.raises(InvalidHeaderError):
            authorize._get_jwt_from_headers(auth="random string")

    def test_int_from_datetime(self, authorize: JwtManager):
        now = datetime.now()
        assert authorize._get_int_from_datetime(now) == int(now.timestamp())

    def test__invalid_int_from_datetime(self, authorize: JwtManager):
        with pytest.raises(TypeError):
            authorize._get_int_from_datetime(None)  # type: ignore[arg-type]

    def test_create_valid_type_tokens(self, authorize: JwtManager):
        access_token = authorize.create_access_token(subject="1")
        refresh_token = authorize.create_refresh_token(subject="1")

        decoded_access_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        decoded_refresh_token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])

        assert decoded_access_token["type"] == "access"
        assert decoded_refresh_token["type"] == "refresh"

    def test_create_invalid_type_tokens(self, authorize: JwtManager):
        with pytest.raises(TypeError):
            authorize.create_access_token(subject=None)  # type: ignore[arg-type]

        with pytest.raises(TypeError):
            authorize.create_refresh_token(subject=None)  # type: ignore[arg-type]

    def test_create_valid_tokens(self, authorize: JwtManager):
        exp_time = int((datetime.now() + timedelta(minutes=1)).timestamp())

        assert isinstance(authorize._create_token("1", "access"), str)
        assert isinstance(authorize._create_token("1", "refresh"), str)
        assert isinstance(authorize._create_token("1", "access", exp_time), str)
        assert isinstance(authorize._create_token("1", "refresh", exp_time), str)

    def test_create_invalid_tokens(self, authorize: JwtManager):
        with pytest.raises(TypeError):
            authorize._create_token(subject=29.4, token_type="access")  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            authorize._create_token(subject="1", token_type="random")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            authorize._create_token(subject=1, token_type="access", exp_time=False)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            authorize._create_token(subject="1", token_type="access", exp_time=False)  # type: ignore[arg-type]

    def test_get_valid_jwt(self, authorize: JwtManager):
        access_token = authorize.create_access_token(subject="1")
        refresh_token = authorize.create_refresh_token(subject="1")

        assert isinstance(authorize.get_jwt(access_token), TokenData)
        assert isinstance(authorize.get_jwt(refresh_token), TokenData)

    def test_get_invalid_jwt(self, authorize: JwtManager):
        with pytest.raises(AuthJwtDecodeError):
            authorize.get_jwt("random_string")

    def test_verify_jwt_in_request(self, authorize: JwtManager):
        access_token = authorize.create_refresh_token(subject="1")

        with pytest.raises(ValueError):
            authorize._verify_jwt_in_request(access_token, "random_type")  # type: ignore[arg-type]

        access_token = authorize.create_access_token(subject="1")
        with pytest.raises(AuthJwtRefreshTokenRequired):
            authorize._verify_jwt_in_request(access_token, "refresh")

        refresh_token = authorize.create_refresh_token(subject="1")
        with pytest.raises(AuthJwtAccessTokenRequired):
            authorize._verify_jwt_in_request(refresh_token, "access")

    def test_valid_jwt_token_required(self, authorize: JwtManager):
        access_token = authorize.create_refresh_token(subject="1")
        authorize.token = access_token

        authorize.jwt_refresh_token_required()

        access_token = authorize.create_access_token(subject="1")
        authorize.token = access_token

        authorize.jwt_access_token_required()

    def test_invalid_jwt_token_required(self, authorize: JwtManager):
        access_token = authorize.create_access_token(subject="1")
        authorize.token = access_token
        with pytest.raises(AuthJwtRefreshTokenRequired):
            authorize.jwt_refresh_token_required()

        access_token = authorize.create_refresh_token(subject="1")
        authorize.token = access_token
        with pytest.raises(AuthJwtAccessTokenRequired):
            authorize.jwt_access_token_required()
