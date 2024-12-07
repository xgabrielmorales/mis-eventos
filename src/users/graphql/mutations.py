import strawberry

from src.users.graphql.nodes import UserInput, UserInputUpdate, UserType
from src.users.services.user import UserService


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, user_data: UserInput) -> UserType:
        return UserService.create(user_data=user_data)

    @strawberry.mutation
    def update_user(self, user_id: int, user_data: UserInputUpdate) -> UserType:
        return UserService.update(user_id=user_id, user_data=user_data)

    @strawberry.mutation
    def delete_user(self, user_id: int) -> str:
        return UserService.delete(user_id=user_id)
