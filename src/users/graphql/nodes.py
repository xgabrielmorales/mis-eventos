from typing import Optional

import strawberry

from src.users.schemas import Role


@strawberry.type
class UserType:
    id: int
    first_name: str
    last_name: str
    username: str
    role: Role


@strawberry.input
class UserInput:
    first_name: str
    last_name: str
    password: str
    username: str
    role: Role


@strawberry.input
class UserInputUpdate:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    role: Optional[Role] = None
