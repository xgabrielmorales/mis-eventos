from dataclasses import dataclass
from typing import Optional

from sqlmodel import Session, select

from src.core.database import engine
from src.users.models.user import User


@dataclass
class UserRepository:
    session: Session = Session(engine)

    def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)

        with self.session as db:
            user = db.exec(query).first()

        return user

    def get_all(self) -> list[User]:
        query = select(User)

        with self.session as db:
            users = db.exec(query).all()

        return list(users)

    def create(self, new_user: User) -> User:
        with self.session as db:
            try:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
            except Exception as e:
                db.rollback()
                raise e

        return new_user

    def update(self, user: User) -> User:
        with self.session as db:
            try:
                db.add(user)
                db.commit()
                db.refresh(user)
            except Exception as e:
                db.rollback()
                raise e

        return user

    def delete(self, user: User) -> None:
        with self.session as db:
            try:
                db.delete(user)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
