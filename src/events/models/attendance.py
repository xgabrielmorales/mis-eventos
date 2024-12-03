from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from src.events.models.registration import Registration


class Attendance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_id: int = Field(foreign_key="registration.id")
    attendance_datetime: datetime = Field(default_factory=datetime.utcnow)
    confirmed: bool
    registration: Optional["Registration"] = Relationship(back_populates="attendances")
