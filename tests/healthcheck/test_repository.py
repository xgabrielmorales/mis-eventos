from unittest.mock import patch

from sqlalchemy.exc import OperationalError

from src.healthcheck.repository import HealthCheckRepository
from src.healthcheck.schemas import HealthCheckData, Status


def test_status_healthy() -> None:
    with patch("src.healthcheck.repository.Session") as mock_session:
        mock_session.return_value.__enter__.return_value.exec.return_value = None

        result = HealthCheckRepository.status()
        assert result == HealthCheckData(app=Status.HEALTHY, postgresql=Status.HEALTHY)


def test_status_unhealthy() -> None:
    with patch("src.healthcheck.repository.Session") as mock_session:
        mock_session.return_value.__enter__.side_effect = OperationalError("mock", "mock", "mock")  # type: ignore[arg-type]

        result = HealthCheckRepository.status()
        assert result == HealthCheckData(app=Status.HEALTHY, postgresql=Status.UNHEALTHY)
