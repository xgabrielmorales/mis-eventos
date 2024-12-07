from sqlalchemy.exc import OperationalError
from sqlmodel import text
from sqlmodel.orm.session import Session

from src.core.database import engine
from src.healthcheck.schemas import HealthCheckData, Status


class HealthCheckRepository:
    @staticmethod
    def status() -> HealthCheckData:
        try:
            with Session(engine) as session:
                session.exec(text("SELECT 1"))  # type: ignore[call-overload]
            postgres_status = Status.HEALTHY
        except OperationalError:
            postgres_status = Status.UNHEALTHY

        return HealthCheckData(
            app=Status.HEALTHY,
            postgresql=postgres_status,
        )
