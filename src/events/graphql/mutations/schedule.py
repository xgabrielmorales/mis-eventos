import strawberry

from src.events.graphql.nodes import (
    ScheduleInput,
    ScheduleInputUpdate,
    ScheduleType,
)
from src.events.services.schedule import ScheduleService


@strawberry.type
class ScheduleMutation:
    @strawberry.mutation
    def create_schedule(
        self,
        schedule_data: ScheduleInput,
    ) -> ScheduleType:
        schedule_service = ScheduleService()
        return schedule_service.create(
            schedule_data=schedule_data,
        )

    @strawberry.mutation
    def update_schedule(
        self,
        schedule_id: int,
        schedule_data: ScheduleInputUpdate,
    ) -> ScheduleType:
        schedule_service = ScheduleService()
        return schedule_service.update(
            schedule_id=schedule_id,
            schedule_data=schedule_data,
        )

    @strawberry.mutation
    def delete_schedule(
        self,
        schedule_id: int,
    ) -> str:
        schedule_service = ScheduleService()
        return schedule_service.delete(
            schedule_id=schedule_id,
        )
