import logging
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.core.database import engine
from src.events.models.registration import Registration

logger = logging.getLogger(__name__)


@dataclass
class RegistrationRepository:
    session: Session = Session(engine)

    def get_by_id(self, registration_id: int) -> Optional[Registration]:
        query = select(Registration).where(Registration.id == registration_id)

        with self.session as db:
            try:
                registration = db.exec(query).first()
                return registration
            except SQLAlchemyError as e:
                logger.error(f"Error retrieving registration with ID {registration_id}: {e}")
                raise

    def create(self, new_registration: Registration) -> Registration:
        with self.session as db:
            try:
                db.add(new_registration)
                db.commit()
                db.refresh(new_registration)
                return new_registration
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error creating registration: {e}")
                raise

    def update(self, registration: Registration) -> Registration:
        with self.session as db:
            try:
                db.add(registration)
                db.commit()
                db.refresh(registration)
                return registration
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error updating registration with ID {registration.id}: {e}")
                raise

    def delete(self, registration: Registration) -> None:
        with self.session as db:
            try:
                db.delete(registration)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error deleting registration with ID {registration.id}: {e}")
                raise
