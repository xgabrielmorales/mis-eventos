import strawberry

from src.healthcheck.graphql.nodes import HealthCheckType
from src.healthcheck.repository import HealthCheckRepository


@strawberry.type
class HealthCheckQuery:
    @strawberry.field
    def status(self) -> HealthCheckType:
        status = HealthCheckRepository.status()
        return HealthCheckType(**status.model_dump())
