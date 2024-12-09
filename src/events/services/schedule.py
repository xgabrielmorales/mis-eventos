import logging
from dataclasses import dataclass, field

from fastapi.exceptions import HTTPException

from src.events.graphql.nodes import ScheduleInput, ScheduleInputUpdate, ScheduleType
from src.events.models.schedule import Schedule
from src.events.repositories.schedule import ScheduleRepository

logger = logging.getLogger(__name__)


@dataclass
class ScheduleService:
    repository: ScheduleRepository = field(default_factory=ScheduleRepository)

    def get_by_id(self, schedule_id: int) -> ScheduleType:
        schedule = self.repository.get_by_id(instance_id=schedule_id)

        if not schedule:
            raise HTTPException(
                status_code=404,
                detail="Schedule does not exist or cannot be found.",
            )

        return ScheduleType(
            id=schedule.id,
            activity_title=schedule.activity_title,
            description=schedule.description,
            start_datetime=schedule.start_datetime,
            end_datetime=schedule.end_datetime,
            location=schedule.location,
            event_id=schedule.event_id,
        )

    def get_all(self) -> list[ScheduleType]:
        logger.info("Fetching all events.")

        schedules: list[ScheduleType] = []
        for schedule in self.repository.get_all():
            schedules.append(
                ScheduleType(
                    id=schedule.id,
                    activity_title=schedule.activity_title,
                    description=schedule.description,
                    start_datetime=schedule.start_datetime,
                    end_datetime=schedule.end_datetime,
                    location=schedule.location,
                    event_id=schedule.event_id,
                ),
            )
        return schedules

    def create(
        self,
        schedule_data: ScheduleInput,
    ) -> ScheduleType:
        new_schedule = Schedule(
            activity_title=schedule_data.activity_title,
            description=schedule_data.description,
            start_datetime=schedule_data.start_datetime,
            end_datetime=schedule_data.end_datetime,
            location=schedule_data.location,
            event_id=schedule_data.event_id,
        )

        schedule = self.repository.create(instance=new_schedule)

        return ScheduleType(
            id=schedule.id,
            activity_title=schedule.activity_title,
            description=schedule.description,
            start_datetime=schedule.start_datetime,
            end_datetime=schedule.end_datetime,
            location=schedule.location,
            event_id=schedule.event_id,
        )

    def update(
        self,
        schedule_id: int,
        schedule_data: ScheduleInputUpdate,
    ) -> ScheduleType:
        schedule = self.repository.get_by_id(instance_id=schedule_id)

        if not schedule:
            logger.warning(f"Schedule with ID {schedule_id} not found.")
            raise HTTPException(
                status_code=404,
                detail="Schedule does not exist or cannot be found.",
            )

        schedule.activity_title = schedule_data.activity_title or schedule.activity_title
        schedule.description = schedule_data.description or schedule.description
        schedule.end_datetime = schedule_data.end_datetime or schedule.end_datetime
        schedule.event_id = schedule_data.event_id or schedule.event_id
        schedule.location = schedule_data.location or schedule.location
        schedule.start_datetime = schedule_data.start_datetime or schedule.start_datetime

        self.repository.update(schedule)

        return ScheduleType(
            id=schedule.id,
            activity_title=schedule.activity_title,
            description=schedule.description,
            start_datetime=schedule.start_datetime,
            end_datetime=schedule.end_datetime,
            location=schedule.location,
            event_id=schedule.event_id,
        )

    def delete(
        self,
        schedule_id: int,
    ) -> str:
        schedule = self.repository.get_by_id(instance_id=schedule_id)

        if not schedule:
            logger.warning(f"Schedule with ID {schedule_id} not found for deletion.")
            raise HTTPException(
                status_code=404,
                detail="Event does not exist or cannot be found.",
            )

        self.repository.delete(instance=schedule)

        return "Event deleted successfully"
