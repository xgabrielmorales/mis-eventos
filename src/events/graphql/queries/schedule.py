import strawberry

from src.auth.middleware.jwt_middleware import IsAuthenticated
from src.events.graphql.nodes import ScheduleType
from src.events.services.schedule import ScheduleService


@strawberry.type
class ScheduleQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def get_schedule_by_id(self, schedule_id: int) -> ScheduleType:
        schedule_service = ScheduleService()
        return schedule_service.get_by_id(schedule_id=schedule_id)

    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def get_all_schedules(self) -> list[ScheduleType]:
        schedule_service = ScheduleService()
        return schedule_service.get_all()
