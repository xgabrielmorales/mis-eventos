from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import ValidationInfo, field_validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.events.models.event import Event


class Schedule(SQLModel, table=True):
    id: int = Field(primary_key=True)
    activity_title: str = Field(max_length=128)
    description: str = Field(max_length=1024)
    start_datetime: datetime
    end_datetime: datetime
    location: str = Field(max_length=256)

    event_id: int = Field(foreign_key="event.id")
    event: Optional["Event"] = Relationship(back_populates="schedules")

    @field_validator("end_datetime")
    def end_after_start(cls, v: datetime, info: ValidationInfo) -> datetime:
        start = info.data.get("start_datetime")
        if start and v <= start:
            raise ValueError("end_datetime must be after start_datetime")
        return v

    @field_validator("activity_title")
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Activity title cannot be empty")
        return v

    @field_validator("location")
    def location_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Location cannot be empty")
        return v
