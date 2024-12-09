import logging
from dataclasses import dataclass, field

from fastapi.exceptions import HTTPException

from src.events.graphql.nodes import ResourceInput, ResourceInputUpdate, ResourceType
from src.events.models.resource import Resource
from src.events.repositories.resource import ResourceRepository

logger = logging.getLogger(__name__)


@dataclass
class ResourceService:
    repository: ResourceRepository = field(default_factory=ResourceRepository)

    def get_by_id(self, resource_id: int) -> ResourceType:
        resource = self.repository.get_by_id(instance_id=resource_id)

        if not resource:
            raise HTTPException(
                status_code=404,
                detail="Resource does not exist or cannot be found.",
            )

        return ResourceType(
            id=resource.id,
            name=resource.name,
            type=resource.type,
            quantity_available=resource.quantity_available,
            event_id=resource.event_id,
        )

    def get_all(self) -> list[ResourceType]:
        logger.info("Fetching all events.")

        resources: list[ResourceType] = []
        for resource in self.repository.get_all():
            resources.append(
                ResourceType(
                    id=resource.id,
                    name=resource.name,
                    type=resource.type,
                    quantity_available=resource.quantity_available,
                    event_id=resource.event_id,
                ),
            )
        return resources

    def create(
        self,
        resource_data: ResourceInput,
    ) -> ResourceType:
        new_resource = Resource(
            name=resource_data.name,
            type=resource_data.type,
            quantity_available=resource_data.quantity_available,
            event_id=resource_data.event_id,
        )

        resource = self.repository.create(instance=new_resource)

        return ResourceType(
            id=resource.id,
            name=resource.name,
            type=resource.type,
            quantity_available=resource.quantity_available,
            event_id=resource.event_id,
        )

    def update(
        self,
        resource_id: int,
        resource_data: ResourceInputUpdate,
    ) -> ResourceType:
        resource = self.repository.get_by_id(instance_id=resource_id)

        if not resource:
            logger.warning(f"Resource with ID {resource_id} not found.")
            raise HTTPException(
                status_code=404,
                detail="Resource does not exist or cannot be found.",
            )

        resource.name = resource_data.name or resource.name
        resource.type = resource_data.type or resource.type
        resource.quantity_available = (
            resource_data.quantity_available or resource.quantity_available
        )
        resource.event_id = resource_data.event_id or resource.event_id

        self.repository.update(resource)

        return ResourceType(
            id=resource.id,
            name=resource.name,
            type=resource.type,
            quantity_available=resource.quantity_available,
            event_id=resource.event_id,
        )

    def delete(
        self,
        resource_id: int,
    ) -> str:
        resource = self.repository.get_by_id(instance_id=resource_id)

        if not resource:
            logger.warning(f"Resource with ID {resource_id} not found for deletion.")
            raise HTTPException(
                status_code=404,
                detail="Event does not exist or cannot be found.",
            )

        self.repository.delete(instance=resource)

        return "Event deleted successfully"
