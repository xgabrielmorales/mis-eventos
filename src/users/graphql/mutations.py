import strawberry

from src.auth.middleware.jwt_middleware import IsAuthenticated
from src.users.graphql.nodes import UserInput, UserInputUpdate, UserType
from src.users.services.user import UserService


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, user_data: UserInput) -> UserType:
        user_service = UserService()

        return user_service.create(user_data=user_data)

    @strawberry.mutation(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def update_user(self, user_id: int, user_data: UserInputUpdate) -> UserType:
        user_service = UserService()

        return user_service.update(user_id=user_id, user_data=user_data)

    @strawberry.mutation(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def delete_user(self, user_id: int) -> str:
        user_service = UserService()

        return user_service.delete(user_id=user_id)
