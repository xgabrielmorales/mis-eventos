import strawberry

from src.events.graphql.nodes import EventInput, EventInputUpdate, EventType
from src.events.services.event import EventService


@strawberry.type
class EventMutation:
    @strawberry.mutation
    def create_event(self, event_data: EventInput) -> EventType:
        event_service = EventService()
        return event_service.create(event_data=event_data)

    @strawberry.mutation
    def update_event(self, event_id: int, event_data: EventInputUpdate) -> EventType:
        event_service = EventService()
        return event_service.update(event_id=event_id, event_data=event_data)

    @strawberry.mutation
    def delete_event(self, event_id: int) -> str:
        event_service = EventService()
        return event_service.delete(event_id=event_id)
