from enum import StrEnum

from pydantic import BaseModel


class Status(StrEnum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthCheckData(BaseModel):
    app: Status
    postgresql: Status
