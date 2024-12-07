import strawberry

from src.healthcheck.schemas import Status


@strawberry.type
class HealthCheckType:
    app: Status
    postgresql: Status
