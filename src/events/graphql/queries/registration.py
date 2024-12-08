import strawberry

from src.events.graphql.nodes import RegistrationType
from src.events.services.registration import RegistrationService


@strawberry.type
class ResgistrationQuery:
    @strawberry.field
    def get_resgistration_by_id(self, registration_id: int) -> RegistrationType:
        registration_service = RegistrationService()
        return registration_service.get_by_id(registration_id=registration_id)
