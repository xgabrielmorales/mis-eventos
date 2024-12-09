import dataclasses
import logging

from fastapi.exceptions import HTTPException

from src.core.password import hash_password
from src.users.graphql.nodes import UserInput, UserInputUpdate, UserType
from src.users.models.user import User
from src.users.repository.user import UserRepository

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class UserService:
    repository: UserRepository = dataclasses.field(default_factory=UserRepository)

    def get_by_id(self, user_id: int) -> UserType:
        logger.info(f"Fetching user with ID: {user_id}")
        user = self.repository.get_by_id(instance_id=user_id)

        if not user:
            logger.warning(f"User with ID {user_id} not found.")
            raise HTTPException(
                status_code=404,
                detail="User does not exist or cannot be found.",
            )

        logger.info(f"User with ID {user_id} retrieved successfully.")
        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=user.role,
        )

    def get_all(self) -> list[UserType]:
        logger.info("Fetching all users.")
        users: list[UserType] = []
        for user in self.repository.get_all():
            users.append(
                UserType(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    username=user.username,
                    role=user.role,
                ),
            )
        logger.info(f"Total users fetched: {len(users)}")
        return users

    def create(self, user_data: UserInput) -> UserType:
        logger.info(f"Creating a new user with username: {user_data.username}")
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            password=hash_password(user_data.password),
            role=user_data.role,
        )

        user = self.repository.create(instance=new_user)
        logger.info(f"User created with ID: {user.id}")
        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=user.role,
        )

    def update(self, user_id: int, user_data: UserInputUpdate) -> UserType:
        logger.info(f"Updating user with ID: {user_id}")
        user = self.repository.get_by_id(instance_id=user_id)

        if not user:
            logger.warning(f"User with ID {user_id} not found for update.")
            raise HTTPException(
                status_code=404,
                detail="User does not exist or cannot be found.",
            )

        fields_to_update = ["first_name", "last_name", "username", "role"]
        for field in fields_to_update:
            setattr(user, field, getattr(user_data, field) or getattr(user, field))
            logger.debug(f"Updated {field} for user ID {user_id}")

        if user_data.password:
            user.password = hash_password(user_data.password)
            logger.debug(f"Password updated for user ID {user_id}")

        self.repository.update(instance=user)
        logger.info(f"User with ID {user_id} updated successfully.")

        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=user.role,
        )

    def delete(self, user_id: int) -> str:
        logger.info(f"Deleting user with ID: {user_id}")
        user = self.repository.get_by_id(instance_id=user_id)

        if not user:
            logger.warning(f"User with ID {user_id} not found for deletion.")
            raise HTTPException(
                status_code=404,
                detail="User does not exist or cannot be found.",
            )

        self.repository.delete(instance=user)
        logger.info(f"User with ID {user_id} deleted successfully.")
        return "User deleted successfully"
