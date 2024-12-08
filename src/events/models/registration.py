from datetime import datetime

from pydantic import field_validator
from sqlmodel import Field, SQLModel

from src.events.schemas import RegistrationStatus


class Registration(SQLModel, table=True):
    id: int = Field(primary_key=True)
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    status: RegistrationStatus

    event_id: int = Field(foreign_key="event.id")
    attendee_id: int = Field(foreign_key="user.id")

    @field_validator("status")
    def valid_status(cls, v: RegistrationStatus) -> RegistrationStatus:
        if v not in RegistrationStatus:
            raise ValueError("Invalid registration status")
        return v
