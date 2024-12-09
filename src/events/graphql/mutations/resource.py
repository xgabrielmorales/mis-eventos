import strawberry

from src.events.graphql.nodes import (
    ResourceInput,
    ResourceInputUpdate,
    ResourceType,
)
from src.events.services.resource import ResourceService


@strawberry.type
class ResourceMutation:
    @strawberry.mutation
    def create_resource(
        self,
        resource_data: ResourceInput,
    ) -> ResourceType:
        resource_service = ResourceService()
        return resource_service.create(
            resource_data=resource_data,
        )

    @strawberry.mutation
    def update_resource(
        self,
        resource_id: int,
        resource_data: ResourceInputUpdate,
    ) -> ResourceType:
        resource_service = ResourceService()
        return resource_service.update(
            resource_id=resource_id,
            resource_data=resource_data,
        )

    @strawberry.mutation
    def delete_resource(
        self,
        resource_id: int,
    ) -> str:
        resource_service = ResourceService()
        return resource_service.delete(
            resource_id=resource_id,
        )
