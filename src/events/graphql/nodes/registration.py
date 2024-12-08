from datetime import datetime

import strawberry

from src.events.schemas import RegistrationStatus


@strawberry.type
class RegistrationType:
    id: int
    registration_date: datetime
    status: RegistrationStatus


@strawberry.input
class RegistrationInput:
    registration_date: datetime
    status: RegistrationStatus
    event_id: int
    attendee_id: int


@strawberry.input
class RegistrationInputUpdate:
    registration_date: datetime
    status: RegistrationStatus
