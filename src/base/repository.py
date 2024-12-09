import logging
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)

logger = logging.getLogger(__name__)


@dataclass
class BaseRepository(Generic[T]):
    session: Session
    model_class: type[T]

    def get_by_id(self, instance_id: int) -> Optional[T]:
        query = select(self.model_class).where(
            self.model_class.id == instance_id,  # type: ignore[attr-defined]
        )

        with self.session as db:
            try:
                instance = db.exec(query).first()
                return instance
            except SQLAlchemyError as e:
                logger.error(f"Error getting by id: {e}")
                raise

    def get_all(self) -> list[T]:
        query = select(self.model_class)

        with self.session as db:
            try:
                instances = db.exec(query).all()
                return list(instances)
            except SQLAlchemyError as e:
                logger.error(f"Error getting all: {e}")
                raise

    def create(self, instance: T) -> T:
        with self.session as db:
            try:
                db.add(instance)
                db.commit()
                db.refresh(instance)
                return instance
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error creating instance: {e}")
                raise

    def update(self, instance: T) -> T:
        with self.session as db:
            try:
                db.add(instance)
                db.commit()
                db.refresh(instance)
                return instance
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error updating instance: {e}")
                raise

    def delete(self, instance: T) -> None:
        with self.session as db:
            try:
                db.delete(instance)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error deleting instance: {e}")
                raise
