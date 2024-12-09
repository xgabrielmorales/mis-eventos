import strawberry

from src.auth.middleware.jwt_middleware import IsAuthenticated
from src.events.graphql.nodes import RegistrationType
from src.events.services.registration import RegistrationService


@strawberry.type
class ResgistrationQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def get_resgistration_by_id(self, registration_id: int) -> RegistrationType:
        registration_service = RegistrationService()
        return registration_service.get_by_id(registration_id=registration_id)
