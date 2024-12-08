import strawberry
from strawberry.types import Info

from src.auth.graphql.nodes import AuthDataType, AuthGrantedDataType
from src.auth.services.create_tokens import JwtAuthentication
from src.auth.services.jwt_manager import JwtManager


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    def create_token(self, auth_data: AuthDataType) -> AuthGrantedDataType:
        jwt_authentication = JwtAuthentication()
        return jwt_authentication.create_auth_tokens(auth_data=auth_data)

    @strawberry.mutation
    def refresh_token(self, info: Info) -> AuthGrantedDataType:
        authorize = JwtManager(request=info.context["request"])

        jwt_authentication = JwtAuthentication()
        return jwt_authentication.refresh_auth_tokens(authorize=authorize)
