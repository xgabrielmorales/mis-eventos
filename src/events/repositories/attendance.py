import logging
from dataclasses import dataclass

from sqlmodel import Session

from src.base.repository import BaseRepository
from src.core.database import engine
from src.events.models.attendance import Attendance

logger = logging.getLogger(__name__)


@dataclass
class AttendanceRepository(BaseRepository[Attendance]):
    session: Session = Session(engine)
    model_class: type[Attendance] = Attendance
