from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from src.events.schemas import RegistrationStatusEnum

if TYPE_CHECKING:
    from src.events.models.attendance import Attendance


class Registration(SQLModel, table=True):
    id: int = Field(primary_key=True)
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    status: RegistrationStatusEnum

    event_id: int = Field(foreign_key="event.id")
    attendee_id: int = Field(foreign_key="user.id")

    attendances: list["Attendance"] = Relationship(back_populates="registration")

    @field_validator("status")
    def valid_status(cls, v: RegistrationStatusEnum) -> RegistrationStatusEnum:
        if v not in RegistrationStatusEnum:
            raise ValueError("Invalid registration status")
        return v
