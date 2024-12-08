from pydantic import field_validator
from sqlmodel import Field, SQLModel

from src.users.schemas import Role


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    username: str = Field(max_length=128, unique=True)
    password: str = Field(max_length=128)
    role: Role

    @field_validator("first_name", "last_name")
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value

    @field_validator("password")
    def password_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

    @field_validator("username")
    def username_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Username must not be empty")
        return value
