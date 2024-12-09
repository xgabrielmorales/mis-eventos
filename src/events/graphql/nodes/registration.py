from datetime import datetime

import strawberry

from src.events.schemas import RegistrationStatusEnum


@strawberry.type
class RegistrationType:
    id: int
    registration_date: datetime
    status: RegistrationStatusEnum


@strawberry.input
class RegistrationInput:
    registration_date: datetime
    status: RegistrationStatusEnum
    event_id: int
    attendee_id: int


@strawberry.input
class RegistrationInputUpdate:
    registration_date: datetime
    status: RegistrationStatusEnum
