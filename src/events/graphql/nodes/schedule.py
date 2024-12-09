from datetime import datetime
from typing import Optional

import strawberry


@strawberry.type
class ScheduleType:
    id: int
    activity_title: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    location: str
    event_id: int


@strawberry.input
class ScheduleInput:
    activity_title: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    location: str
    event_id: int


@strawberry.input
class ScheduleInputUpdate:
    activity_title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    location: Optional[str] = None
    event_id: Optional[int] = None
