import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal

import jwt
from fastapi import Request

from src.auth.schemas import TokenData
from src.auth.services.jwt_exceptions import (
    AuthJwtAccessTokenRequired,
    AuthJwtDecodeError,
    AuthJwtRefreshTokenRequired,
    InvalidHeaderError,
)
from src.core.settings import settings


class JwtManager:
    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=30)
    algorithm = "HS256"
    header_type = "Bearer"
    header_name = "Authorization"
    token: str | bytes | None = None

    def __init__(
        self,
        request: Request = None,  # type: ignore[assignment]
    ):
        if request:
            auth: str | None = request.headers.get(self.header_name.lower())

            if auth:
                self._get_jwt_from_headers(auth)

    def _get_jwt_from_headers(self, auth: str) -> None:
        header_name, header_type = self.header_name, self.header_type

        parts = auth.split()

        # <HeaderType> <JWT>
        # Example: Bearer eyJhbGciOiIsIn9.eyJG4gRG9lINDIyfQ.Sfl36POk6yJV_adQssw5c
        if not re.match(r"{}\s".format(header_type), auth) or len(parts) != 2:
            detail = f"Bad {header_name} header. Expected value '{header_type} <JWT>'"
            raise InvalidHeaderError(status_code=422, detail=detail)

        self.token = parts[1]

    def _get_jwt_identifier(self) -> str:
        return str(uuid.uuid4())

    def _get_int_from_datetime(self, value: datetime) -> int:
        if not isinstance(value, datetime):
            raise TypeError("a datetime is required")

        return int(value.timestamp())

    def _create_token(
        self,
        subject: str,
        token_type: Literal["access", "refresh"],
        exp_time: int | None = None,
    ) -> str:
        if type(subject) is not str:
            raise TypeError("subject must be a String")

        if token_type not in ["access", "refresh"]:
            raise ValueError("token_type must be a String and must be either 'access' or 'refresh'")

        if exp_time is not None and type(exp_time) is not int:
            raise TypeError("exp_time must be an Integer or None")

        reserved_claims: dict[str, str | int] = {
            "iat": self._get_int_from_datetime(datetime.now(timezone.utc)),
            "sub": subject,
            "jti": self._get_jwt_identifier(),
        }
        custom_claims: dict[str, str | int] = {
            "type": token_type,
        }

        if exp_time:
            custom_claims["exp"] = exp_time

        token = TokenData.model_validate({**reserved_claims, **custom_claims})

        return jwt.encode(
            payload=token.model_dump(),
            key=settings.SECRET_KEY,
            algorithm=self.algorithm,
        )

    def create_access_token(self, subject: str) -> str:
        if not isinstance(subject, str):
            raise TypeError("subject must be a string")

        now = datetime.now(timezone.utc)

        return self._create_token(
            subject=subject,
            token_type="access",
            exp_time=self._get_int_from_datetime(now + self.access_token_expires),
        )

    def create_refresh_token(self, subject: str) -> str:
        if not isinstance(subject, str):
            raise TypeError("subject must be a string")

        now = datetime.now(timezone.utc)

        return self._create_token(
            subject=subject,
            token_type="refresh",
            exp_time=self._get_int_from_datetime(now + self.refresh_token_expires),
        )

    def get_jwt(self, encoded_token: str | bytes | None = None) -> TokenData:
        token = encoded_token or self.token

        try:
            raw_jwt = jwt.decode(
                jwt=token,  # type: ignore[arg-type]
                key=settings.SECRET_KEY,
                algorithms=self.algorithm,
            )
        except Exception as err:
            raise AuthJwtDecodeError(status_code=422, detail=str(err))

        return TokenData(**raw_jwt)

    def _verify_jwt_in_request(
        self,
        token: str | bytes,
        token_type: Literal["access", "refresh"],
    ) -> None:
        if token_type not in ["access", "refresh"]:
            raise ValueError("token_type must be a string and must be either 'access' or 'refresh'")

        if self.get_jwt(token).type != token_type:
            detail = "Only {} tokens are allowed".format(token_type)
            if token_type == "access":
                raise AuthJwtAccessTokenRequired(status_code=422, detail=detail)
            if token_type == "refresh":
                raise AuthJwtRefreshTokenRequired(status_code=422, detail=detail)

    def jwt_refresh_token_required(self) -> None:
        self._verify_jwt_in_request(self.token, "refresh")  # type: ignore[arg-type]

    def jwt_access_token_required(self) -> None:
        self._verify_jwt_in_request(self.token, "access")  # type: ignore[arg-type]
