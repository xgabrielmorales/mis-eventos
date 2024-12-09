import logging
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from src.base.repository import BaseRepository
from src.core.database import engine
from src.events.models.event import Event

logger = logging.getLogger(__name__)


@dataclass
class EventRepository(BaseRepository[Event]):
    session: Session = Session(engine)
    model_class: type[Event] = Event

    def get_by_id(self, instance_id: int) -> Optional[Event]:
        query = (
            select(self.model_class)
            .where(
                self.model_class.id == instance_id,
            )
            .options(joinedload(self.model_class.organizer))  # type: ignore[arg-type]
        )

        with self.session as db:
            try:
                event = db.exec(query).first()
                logger.info(f"Retrieved event with ID {instance_id}.")
                return event
            except SQLAlchemyError as e:
                logger.error(f"Error retrieving event with ID {instance_id}: {e}")
                raise

    def get_all(self) -> list[Event]:
        query = select(
            self.model_class,
        ).options(joinedload(self.model_class.organizer))  # type: ignore[arg-type]

        with self.session as db:
            try:
                events = db.exec(query).all()
                logger.info("Retrieved all events.")
                return list(events)
            except SQLAlchemyError as e:
                logger.error(f"Error retrieving all events: {e}")
                raise
