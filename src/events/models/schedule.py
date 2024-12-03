from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.events.models.event import Event


class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    activity_title: str = Field(max_length=128)
    description: str = Field(max_length=1024)
    start_datetime: datetime
    end_datetime: datetime
    location: str = Field(max_length=256)
    event: Optional["Event"] = Relationship(back_populates="schedules")
