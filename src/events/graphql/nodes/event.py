from datetime import datetime
from typing import Optional

import strawberry
from pydantic import PositiveInt

from src.events.schemas import EventStatusEnum
from src.users.graphql.nodes import UserType


@strawberry.type
class EventType:
    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    capacity: PositiveInt
    status: EventStatusEnum
    organizer: UserType


@strawberry.input
class EventInput:
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    capacity: PositiveInt
    status: EventStatusEnum
    organizer_id: int


@strawberry.input
class EventInputUpdate:
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    capacity: Optional[PositiveInt] = None
    status: Optional[EventStatusEnum] = None
    organizer_id: Optional[int] = None
