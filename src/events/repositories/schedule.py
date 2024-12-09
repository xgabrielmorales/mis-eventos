import logging
from dataclasses import dataclass

from sqlmodel import Session

from src.base.repository import BaseRepository
from src.core.database import engine
from src.events.models.schedule import Schedule

logger = logging.getLogger(__name__)


@dataclass
class ScheduleRepository(BaseRepository[Schedule]):
    session: Session = Session(engine)
    model_class: type[Schedule] = Schedule
