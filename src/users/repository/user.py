import logging
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.core.database import engine
from src.users.models.user import User

logger = logging.getLogger(__name__)


@dataclass
class UserRepository:
    session: Session = Session(engine)

    def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)

        with self.session as db:
            try:
                user = db.exec(query).first()
                logger.info(f"Retrieved user with ID {user_id}.")
                return user
            except SQLAlchemyError as e:
                logger.error(f"Error retrieving user with ID {user_id}: {e}")
                raise

    def get_all(self) -> list[User]:
        query = select(User)

        with self.session as db:
            try:
                users = db.exec(query).all()
                logger.info("Retrieved all users.")
                return list(users)
            except SQLAlchemyError as e:
                logger.error(f"Error retrieving all users: {e}")
                raise

    def create(self, new_user: User) -> User:
        with self.session as db:
            try:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                logger.info(f"Created new user with ID {new_user.id}.")
                return new_user
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error creating user: {e}")
                raise

    def update(self, user: User) -> User:
        with self.session as db:
            try:
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"Updated user with ID {user.id}.")
                return user
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error updating user with ID {user.id}: {e}")
                raise

    def delete(self, user: User) -> None:
        with self.session as db:
            try:
                db.delete(user)
                db.commit()
                logger.info(f"Deleted user with ID {user.id}.")
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error deleting user with ID {user.id}: {e}")
                raise
