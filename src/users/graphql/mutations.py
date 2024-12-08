import strawberry

from src.users.graphql.nodes import UserInput, UserInputUpdate, UserType
from src.users.services.user import UserService


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, user_data: UserInput) -> UserType:
        user_service = UserService()

        return user_service.create(user_data=user_data)

    @strawberry.mutation
    def update_user(self, user_id: int, user_data: UserInputUpdate) -> UserType:
        user_service = UserService()

        return user_service.update(user_id=user_id, user_data=user_data)

    @strawberry.mutation
    def delete_user(self, user_id: int) -> str:
        user_service = UserService()

        return user_service.delete(user_id=user_id)
