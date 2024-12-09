from datetime import datetime
from typing import Optional

import strawberry


@strawberry.type
class AttendanceType:
    id: int
    attendance_datetime: datetime
    confirmed: bool
    registration_id: int


@strawberry.input
class AttendanceInput:
    attendance_datetime: datetime
    confirmed: bool
    registration_id: int


@strawberry.input
class AttendanceInputUpdate:
    attendance_datetime: Optional[datetime] = None
    confirmed: Optional[bool] = None
    registration_id: Optional[int] = None
