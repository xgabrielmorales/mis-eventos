import logging
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from src.core.database import engine
from src.events.models.event import Event

logger = logging.getLogger(__name__)


@dataclass
class EventRepository:
    session: Session = Session(engine)

    def get_by_id(self, event_id: int) -> Optional[Event]:
        query = select(Event).where(Event.id == event_id).options(joinedload(Event.organizer))  # type: ignore[arg-type]

        with self.session as db:
            try:
                event = db.exec(query).first()
                logger.info(f"Retrieved event with ID {event_id}.")
                return event
            except SQLAlchemyError as e:
                logger.error(f"Error retrieving event with ID {event_id}: {e}")
                raise

    def get_all(self) -> list[Event]:
        query = select(Event).options(joinedload(Event.organizer))  # type: ignore[arg-type]

        with self.session as db:
            try:
                events = db.exec(query).all()
                logger.info("Retrieved all events.")
                return list(events)
            except SQLAlchemyError as e:
                logger.error(f"Error retrieving all events: {e}")
                raise

    def create(self, new_event: Event) -> Event:
        with self.session as db:
            try:
                db.add(new_event)
                db.commit()
                db.refresh(new_event)
                logger.info(f"Created new event with ID {new_event.id}.")
                return new_event
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error creating event: {e}")
                raise

    def update(self, event: Event) -> Event:
        with self.session as db:
            try:
                db.add(event)
                db.commit()
                db.refresh(event)
                logger.info(f"Updated event with ID {event.id}.")
                return event
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error updating event with ID {event.id}: {e}")
                raise

    def delete(self, event: Event) -> None:
        with self.session as db:
            try:
                db.delete(event)
                db.commit()
                logger.info(f"Deleted event with ID {event.id}.")
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error deleting event with ID {event.id}: {e}")
                raise
