import strawberry

from src.auth.middleware.jwt_middleware import IsAuthenticated
from src.events.graphql.nodes import ResourceType
from src.events.services.resource import ResourceService


@strawberry.type
class ResourceQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def get_resource_by_id(self, resource_id: int) -> ResourceType:
        resource_service = ResourceService()
        return resource_service.get_by_id(resource_id=resource_id)

    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def get_all_events(self) -> list[ResourceType]:
        resource_service = ResourceService()
        return resource_service.get_all()
