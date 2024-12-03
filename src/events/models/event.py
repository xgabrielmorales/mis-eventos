from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.events.schemas import EventStatus

if TYPE_CHECKING:
    from src.events.models.resource import Resource
    from src.events.models.schedule import Schedule
    from src.users.models import User


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=128)
    description: str = Field(max_length=1024)
    start_date: datetime
    end_date: datetime
    location: str = Field(max_length=256)
    capacity: int
    status: EventStatus
    organizer_id: int = Field(foreign_key="user.id")
    organizer: Optional["User"] = Relationship(back_populates="events")
    schedules: list["Schedule"] = Relationship(back_populates="event")
    resources: list["Resource"] = Relationship(back_populates="event")
