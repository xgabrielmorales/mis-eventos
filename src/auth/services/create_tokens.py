from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.auth.graphql.nodes import AuthDataType, AuthGrantedDataType
from src.auth.services.jwt_manager import JwtManager
from src.core.database import engine
from src.core.password import verify_password
from src.users.models import User


@dataclass
class JwtAuthentication:
    session: Session = Session(engine)

    def create_auth_tokens(self, auth_data: AuthDataType) -> AuthGrantedDataType:
        query = select(User).where(User.username == auth_data.username)
        user = self.session.exec(query).first()

        if user is None or not verify_password(auth_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        jwt_manager = JwtManager()
        access_token = jwt_manager.create_access_token(subject=str(user.id))
        refresh_token = jwt_manager.create_refresh_token(subject=str(user.id))

        return AuthGrantedDataType(access_token=access_token, refresh_token=refresh_token)

    def refresh_auth_tokens(self, authorize: JwtManager) -> AuthGrantedDataType:
        authorize.jwt_refresh_token_required()
        token = authorize.get_jwt()

        access_token = authorize.create_access_token(subject=str(token.sub))
        refresh_token = authorize.create_refresh_token(subject=str(token.sub))

        return AuthGrantedDataType(access_token=access_token, refresh_token=refresh_token)
