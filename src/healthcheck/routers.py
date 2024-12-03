from fastapi import APIRouter, status
from sqlalchemy.exc import OperationalError
from sqlmodel import text

from src.core.database import SessionDep
from src.healthcheck.schemas import HealthCheckData, Status

router = APIRouter(tags=["Health Checks"])


@router.get(
    path="/healthcheck",
    description="Service health check status",
    status_code=status.HTTP_200_OK,
)
def healthcheck(postgres_db: SessionDep) -> HealthCheckData:
    try:
        postgres_db.exec(text("SELECT 1"))  # type: ignore[call-overload]
        postgres_status = Status.HEALTHY
    except OperationalError:
        postgres_status = Status.UNHEALTHY

    return HealthCheckData(
        app=Status.HEALTHY,
        postgresql=postgres_status,
    )
