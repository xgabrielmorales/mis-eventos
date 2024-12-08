import dataclasses
import logging

from fastapi.exceptions import HTTPException

from src.events.graphql.nodes import EventInput, EventInputUpdate, EventType
from src.events.models.event import Event
from src.events.repositories.event import EventRepository
from src.users.graphql.nodes import UserType

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class EventService:
    event_repository: EventRepository = dataclasses.field(default_factory=EventRepository)

    def get_by_id(self, event_id: int) -> EventType:
        logger.info(f"Fetching event with ID: {event_id}")
        event = self.event_repository.get_by_id(event_id=event_id)

        if not event:
            logger.warning(f"Event with ID {event_id} not found.")
            raise HTTPException(
                status_code=404,
                detail="Event does not exist or cannot be found.",
            )

        logger.info(f"Event with ID {event_id} retrieved successfully.")
        return EventType(
            id=event.id,
            title=event.title,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            capacity=event.capacity,
            status=event.status,
            organizer=UserType(
                id=event.organizer.id,
                first_name=event.organizer.first_name,
                last_name=event.organizer.last_name,
                username=event.organizer.username,
                role=event.organizer.role,
            ),
        )

    def get_all(self) -> list[EventType]:
        logger.info("Fetching all events.")
        events: list[EventType] = []
        for event in self.event_repository.get_all():
            events.append(
                EventType(
                    id=event.id,
                    title=event.title,
                    description=event.description,
                    start_date=event.start_date,
                    end_date=event.end_date,
                    location=event.location,
                    capacity=event.capacity,
                    status=event.status,
                    organizer=UserType(
                        id=event.organizer.id,
                        first_name=event.organizer.first_name,
                        last_name=event.organizer.last_name,
                        username=event.organizer.username,
                        role=event.organizer.role,
                    ),
                ),
            )
        logger.info(f"Total events fetched: {len(events)}")
        return events

    def create(self, event_data: EventInput) -> EventType:
        logger.info(f"Creating a new event with title: {event_data.title}")
        new_event = Event(
            title=event_data.title,
            description=event_data.description,
            start_date=event_data.start_date,
            end_date=event_data.end_date,
            location=event_data.location,
            capacity=event_data.capacity,
            status=event_data.status,
            organizer_id=event_data.organizer_id,
        )

        event_created = self.event_repository.create(new_event=new_event)
        logger.info(f"Event created with ID: {event_created.id}")

        event: Event = self.event_repository.get_by_id(event_id=event_created.id)  # type: ignore[assignment]

        return EventType(
            id=event.id,
            title=event.title,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            capacity=event.capacity,
            status=event.status,
            organizer=UserType(
                id=event.organizer.id,
                first_name=event.organizer.first_name,
                last_name=event.organizer.last_name,
                username=event.organizer.username,
                role=event.organizer.role,
            ),
        )

    def update(self, event_id: int, event_data: EventInputUpdate) -> EventType:
        logger.info(f"Updating event with ID: {event_id}")
        event = self.event_repository.get_by_id(event_id=event_id)

        if not event:
            logger.warning(f"Event with ID {event_id} not found for update.")
            raise HTTPException(
                status_code=404,
                detail="Event does not exist or cannot be found.",
            )

        fields_to_update = [
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "capacity",
            "status",
            "organizer_id",
        ]
        for field in fields_to_update:
            if getattr(event_data, field) is not None:
                setattr(event, field, getattr(event_data, field))
                logger.debug(f"Updated {field} for event ID {event_id}")

        self.event_repository.update(event=event)
        logger.info(f"Event with ID {event_id} updated successfully.")

        return EventType(
            id=event.id,
            title=event.title,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            capacity=event.capacity,
            status=event.status,
            organizer=UserType(
                id=event.organizer.id,
                first_name=event.organizer.first_name,
                last_name=event.organizer.last_name,
                username=event.organizer.username,
                role=event.organizer.role,
            ),
        )

    def delete(self, event_id: int) -> str:
        logger.info(f"Deleting event with ID: {event_id}")
        event = self.event_repository.get_by_id(event_id=event_id)

        if not event:
            logger.warning(f"Event with ID {event_id} not found for deletion.")
            raise HTTPException(
                status_code=404,
                detail="Event does not exist or cannot be found.",
            )

        self.event_repository.delete(event=event)
        logger.info(f"Event with ID {event_id} deleted successfully.")
        return "Event deleted successfully"
