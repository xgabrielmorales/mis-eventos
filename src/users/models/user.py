from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from src.users.schemas import Role

if TYPE_CHECKING:
    from src.events.models.event import Event


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    email: EmailStr
    password: str = Field(max_length=128)
    role: Role
    events: list["Event"] = Relationship(back_populates="organizer")
