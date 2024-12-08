from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from src.events.models.registration import Registration


class Attendance(SQLModel, table=True):
    id: int = Field(primary_key=True)
    attendance_datetime: datetime = Field(default_factory=datetime.utcnow)
    confirmed: bool

    registration_id: int = Field(foreign_key="registration.id")
    registration: Optional["Registration"] = Relationship(back_populates="attendances")
