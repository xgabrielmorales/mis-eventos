import dataclasses

from fastapi.exceptions import HTTPException

from src.core.password import hash_password
from src.users.graphql.nodes import UserInput, UserInputUpdate, UserType
from src.users.models.user import User
from src.users.repository.user import UserRepository


@dataclasses.dataclass
class UserService:
    user_repository: UserRepository = dataclasses.field(default_factory=UserRepository)

    def get_by_id(self, user_id: int) -> UserType:
        user = self.user_repository.get_by_id(user_id=user_id)

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

    def get_all(self) -> list[UserType]:
        users: list[UserType] = []
        for user in self.user_repository.get_all():
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

    def create(self, user_data: UserInput) -> UserType:
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            password=hash_password(user_data.password),
            role=user_data.role,
        )

        user = self.user_repository.create(new_user=new_user)

        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=user.role,
        )

    def update(self, user_id: int, user_data: UserInputUpdate) -> UserType:
        user = self.user_repository.get_by_id(user_id=user_id)

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

        self.user_repository.update(user=user)

        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=user.role,
        )

    def delete(self, user_id: int) -> str:
        user = self.user_repository.get_by_id(user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User does not exist or cannot be found.",
            )

        self.user_repository.delete(user=user)

        return "User deleted successfully"
