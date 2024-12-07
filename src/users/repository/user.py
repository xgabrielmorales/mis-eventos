from typing import Optional

from sqlmodel import Session, select

from src.core.database import engine
from src.users.models.user import User


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)

        with Session(engine) as db:
            user = db.exec(query).first()

        return user

    @staticmethod
    def get_all() -> list[User]:
        query = select(User)

        with Session(engine) as db:
            users = db.exec(query).all()

        return list(users)

    @staticmethod
    def create(new_user: User) -> User:
        with Session(engine) as db:
            try:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
            except Exception as e:
                db.rollback()
                raise e

        return new_user

    @staticmethod
    def update(user: User) -> User:
        with Session(engine) as db:
            try:
                db.add(user)
                db.commit()
                db.refresh(user)
            except Exception as e:
                db.rollback()
                raise e

        return user

    @staticmethod
    def delete(user: User) -> None:
        with Session(engine) as db:
            try:
                db.delete(user)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
