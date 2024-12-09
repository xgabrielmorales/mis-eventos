import logging
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.base.repository import BaseRepository
from src.core.database import engine
from src.events.models.registration import Registration

logger = logging.getLogger(__name__)


@dataclass
class RegistrationRepository(BaseRepository[Registration]):
    session: Session = Session(engine)
    model_class: type[Registration] = Registration

    def get_by_id(self, instance_id: int) -> Optional[Registration]:
        query = select(Registration).where(Registration.id == instance_id)

        with self.session as db:
            try:
                registration = db.exec(query).first()
                return registration
            except SQLAlchemyError as e:
                logger.error(f"Error retrieving registration with ID {instance_id}: {e}")
                raise
