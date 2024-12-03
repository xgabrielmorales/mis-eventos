from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from src.events.schemas import RegistrationStatus


class Registration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    attendee_id: int = Field(foreign_key="user.id")
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    status: RegistrationStatus
