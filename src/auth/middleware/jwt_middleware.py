from typing import Any

from strawberry.permission import BasePermission
from strawberry.types import Info

from src.auth.services.jwt_exceptions import AuthJwtException
from src.auth.services.jwt_manager import JwtManager


class IsAuthenticated(BasePermission):
    message = "User is not Authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs: dict[str, Any]) -> bool:
        request = info.context["request"]

        try:
            jwt_manager = JwtManager(request=request)
            jwt_manager.jwt_access_token_required()
        except AuthJwtException:
            return False

        return True
