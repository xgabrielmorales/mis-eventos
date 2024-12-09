import logging
from dataclasses import dataclass, field

from fastapi.exceptions import HTTPException

from src.events.graphql.nodes import AttendanceInput, AttendanceInputUpdate, AttendanceType
from src.events.models.attendance import Attendance
from src.events.repositories.attendance import AttendanceRepository

logger = logging.getLogger(__name__)


@dataclass
class AttendanceService:
    repository: AttendanceRepository = field(default_factory=AttendanceRepository)

    def get_by_id(self, attendance_id: int) -> AttendanceType:
        attendance = self.repository.get_by_id(instance_id=attendance_id)

        if not attendance:
            raise HTTPException(
                status_code=404,
                detail="Attendance does not exist or cannot be found.",
            )

        return AttendanceType(
            id=attendance.id,
            attendance_datetime=attendance.attendance_datetime,
            confirmed=attendance.confirmed,
            registration_id=attendance.registration_id,
        )

    def get_all(self) -> list[AttendanceType]:
        logger.info("Fetching all events.")

        attendances: list[AttendanceType] = []
        for attendance in self.repository.get_all():
            attendances.append(
                AttendanceType(
                    id=attendance.id,
                    attendance_datetime=attendance.attendance_datetime,
                    confirmed=attendance.confirmed,
                    registration_id=attendance.registration_id,
                ),
            )
        return attendances

    def create(
        self,
        attendance_data: AttendanceInput,
    ) -> AttendanceType:
        new_attendance = Attendance(
            attendance_datetime=attendance_data.attendance_datetime,
            confirmed=attendance_data.confirmed,
            registration_id=attendance_data.registration_id,
        )

        attendance = self.repository.create(instance=new_attendance)

        return AttendanceType(
            id=attendance.id,
            attendance_datetime=attendance.attendance_datetime,
            confirmed=attendance.confirmed,
            registration_id=attendance.registration_id,
        )

    def update(
        self,
        attendance_id: int,
        attendance_data: AttendanceInputUpdate,
    ) -> AttendanceType:
        attendance = self.repository.get_by_id(instance_id=attendance_id)

        if not attendance:
            logger.warning(f"Attendance with ID {attendance_id} not found.")
            raise HTTPException(
                status_code=404,
                detail="Attendance does not exist or cannot be found.",
            )

        attendance.registration_id = attendance_data.registration_id or attendance.registration_id
        attendance.attendance_datetime = (
            attendance_data.attendance_datetime or attendance.attendance_datetime
        )
        if attendance_data.confirmed is not None:
            attendance.confirmed = attendance_data.confirmed

        self.repository.update(attendance)

        return AttendanceType(
            id=attendance.id,
            attendance_datetime=attendance.attendance_datetime,
            confirmed=attendance.confirmed,
            registration_id=attendance.registration_id,
        )

    def delete(
        self,
        attendance_id: int,
    ) -> str:
        attendance = self.repository.get_by_id(instance_id=attendance_id)

        if not attendance:
            logger.warning(f"Attendance with ID {attendance_id} not found for deletion.")
            raise HTTPException(
                status_code=404,
                detail="Event does not exist or cannot be found.",
            )

        self.repository.delete(instance=attendance)

        return "Event deleted successfully"
