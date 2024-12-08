import strawberry

from src.events.graphql.nodes import EventType
from src.events.services.event import EventService


@strawberry.type
class EventQuery:
    @strawberry.field
    def get_event_by_id(self, event_id: int) -> EventType:
        event_service = EventService()
        return event_service.get_by_id(event_id=event_id)

    @strawberry.field
    def get_all_events(self) -> list[EventType]:
        event_service = EventService()
        return event_service.get_all()
