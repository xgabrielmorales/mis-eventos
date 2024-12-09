import logging
from dataclasses import dataclass

from sqlmodel import Session

from src.base.repository import BaseRepository
from src.core.database import engine
from src.users.models.user import User

logger = logging.getLogger(__name__)


@dataclass
class UserRepository(BaseRepository[User]):
    session: Session = Session(engine)
    model_class: type[User] = User
