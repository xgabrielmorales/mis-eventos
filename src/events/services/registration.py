import logging
from dataclasses import dataclass, field

from fastapi.exceptions import HTTPException

from src.events.graphql.nodes import RegistrationInput, RegistrationInputUpdate, RegistrationType
from src.events.models.registration import Registration
from src.events.repositories.registration import RegistrationRepository

logger = logging.getLogger(__name__)


@dataclass
class RegistrationService:
    repository: RegistrationRepository = field(default_factory=RegistrationRepository)

    def get_by_id(self, registration_id: int) -> RegistrationType:
        registration = self.repository.get_by_id(registration_id=registration_id)

        if not registration:
            raise HTTPException(
                status_code=404,
                detail="Registration does not exist or cannot be found.",
            )

        return RegistrationType(
            id=registration.id,
            registration_date=registration.registration_date,
            status=registration.status,
        )

    def create(
        self,
        registration_data: RegistrationInput,
    ) -> RegistrationType:
        new_registration = Registration(
            status=registration_data.status,
            event_id=registration_data.event_id,
            attendee_id=registration_data.attendee_id,
        )

        registration = self.repository.create(new_registration)

        return RegistrationType(
            id=registration.id,
            registration_date=registration.registration_date,
            status=registration.status,
        )

    def update(
        self,
        registration_id: int,
        registration_data: RegistrationInputUpdate,
    ) -> RegistrationType:
        registration = self.repository.get_by_id(registration_id)

        if not registration:
            logger.warning(f"Registration with ID {registration_id} not found.")
            raise HTTPException(
                status_code=404,
                detail="Registration does not exist or cannot be found.",
            )

        registration.status = registration_data.status or registration.status
        self.repository.update(registration)

        return RegistrationType(
            id=registration.id,
            registration_date=registration.registration_date,
            status=registration.status,
        )

    def delete(
        self,
        registration_id: int,
    ) -> str:
        registration = self.repository.get_by_id(registration_id=registration_id)

        if not registration:
            logger.warning(f"Registration with ID {registration_id} not found for deletion.")
            raise HTTPException(
                status_code=404,
                detail="Event does not exist or cannot be found.",
            )

        self.repository.delete(registration)

        return "Event deleted successfully"
