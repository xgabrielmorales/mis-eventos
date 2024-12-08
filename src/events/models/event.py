from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from pydantic import PositiveInt, ValidationInfo, field_validator
from sqlmodel import Field, Relationship, SQLModel

from src.events.schemas import EventStatus

if TYPE_CHECKING:
    from src.events.models.resource import Resource
    from src.events.models.schedule import Schedule
    from src.users.models import User


class Event(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=128)
    description: str = Field(max_length=1024)
    start_date: datetime
    end_date: datetime
    location: str = Field(max_length=256)
    capacity: PositiveInt
    status: EventStatus

    organizer_id: int = Field(foreign_key="user.id")
    organizer: "User" = Relationship(back_populates="events")
    schedules: list["Schedule"] = Relationship(back_populates="event")
    resources: list["Resource"] = Relationship(back_populates="event")

    @field_validator("title")
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("location")
    def location_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Location cannot be empty")
        return v

    @field_validator("capacity")
    def capacity_positive(cls, v: PositiveInt) -> PositiveInt:
        if v < 1:
            raise ValueError("Capacity must be at least 1")
        return v

    @field_validator("end_date")
    def end_after_start(cls, v: datetime, info: ValidationInfo) -> datetime:
        start_date = info.data.get("start_date")
        if start_date and v <= start_date:
            raise ValueError("end_date must be after start_date")
        return v

    @field_validator("start_date")
    def start_date_not_too_far_back(cls, v: datetime) -> datetime:
        one_month_ago = datetime.now() - timedelta(days=30)
        if v < one_month_ago:
            raise ValueError("start_date cannot be earlier than one month ago")
        return v
