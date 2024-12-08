import strawberry

from src.events.graphql.nodes import (
    RegistrationInput,
    RegistrationInputUpdate,
    RegistrationType,
)
from src.events.services.registration import RegistrationService


@strawberry.type
class RegistrationMutation:
    @strawberry.mutation
    def create_registration(
        self,
        registration_data: RegistrationInput,
    ) -> RegistrationType:
        registration_service = RegistrationService()
        return registration_service.create(
            registration_data=registration_data,
        )

    @strawberry.mutation
    def update_registration(
        self,
        registration_id: int,
        registration_data: RegistrationInputUpdate,
    ) -> RegistrationType:
        registration_service = RegistrationService()
        return registration_service.update(
            registration_id=registration_id,
            registration_data=registration_data,
        )

    @strawberry.mutation
    def delete_registration(
        self,
        registration_id: int,
    ) -> str:
        registration_service = RegistrationService()
        return registration_service.delete(
            registration_id=registration_id,
        )
