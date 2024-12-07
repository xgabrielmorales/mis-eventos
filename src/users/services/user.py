from fastapi.exceptions import HTTPException

from src.core.password import hash_password
from src.users.graphql.nodes import UserInput, UserInputUpdate, UserType
from src.users.models.user import User
from src.users.repository.user import UserRepository


class UserService:
    @staticmethod
    def get_by_id(user_id: int) -> UserType:
        user = UserRepository.get_by_id(user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User does not exist or cannot be found.",
            )

        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=user.role,
        )

    @staticmethod
    def get_all() -> list[UserType]:
        users: list[UserType] = []
        for user in UserRepository.get_all():
            users.append(
                UserType(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    username=user.username,
                    role=user.role,
                ),
            )

        return users

    @staticmethod
    def create(user_data: UserInput) -> UserType:
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            password=hash_password(user_data.password),
            role=user_data.role,
        )

        user = UserRepository.create(new_user=new_user)

        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=user.role,
        )

    @staticmethod
    def update(user_id: int, user_data: UserInputUpdate) -> UserType:
        user = UserRepository.get_by_id(user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User does not exist or cannot be found.",
            )

        fields_to_update = ["first_name", "last_name", "username", "role"]
        for field in fields_to_update:
            setattr(user, field, getattr(user_data, field) or getattr(user, field))

        if user_data.password:
            user.password = hash_password(user_data.password)

        UserRepository.update(user=user)

        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=user.role,
        )

    @staticmethod
    def delete(user_id: int) -> str:
        user = UserRepository.get_by_id(user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User does not exists or cannot be found.",
            )

        UserRepository.delete(user=user)

        return "User deleted successfully"
