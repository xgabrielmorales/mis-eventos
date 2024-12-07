import strawberry

from src.users.graphql.nodes import UserType
from src.users.services.user import UserService


@strawberry.type
class UserQuery:
    @strawberry.field
    def get_user_by_id(self, user_id: int) -> UserType:
        return UserService.get_by_id(user_id=user_id)

    @strawberry.field
    def get_all_users(self) -> list[UserType]:
        return UserService.get_all()
