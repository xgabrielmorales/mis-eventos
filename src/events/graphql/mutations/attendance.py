import strawberry

from src.events.graphql.nodes import (
    AttendanceInput,
    AttendanceInputUpdate,
    AttendanceType,
)
from src.events.services.attendance import AttendanceService


@strawberry.type
class AttendanceMutation:
    @strawberry.mutation
    def create_attendance(
        self,
        attendance_data: AttendanceInput,
    ) -> AttendanceType:
        attendance_service = AttendanceService()
        return attendance_service.create(
            attendance_data=attendance_data,
        )

    @strawberry.mutation
    def update_attendance(
        self,
        attendance_id: int,
        attendance_data: AttendanceInputUpdate,
    ) -> AttendanceType:
        attendance_service = AttendanceService()
        return attendance_service.update(
            attendance_id=attendance_id,
            attendance_data=attendance_data,
        )

    @strawberry.mutation
    def delete_attendance(
        self,
        attendance_id: int,
    ) -> str:
        attendance_service = AttendanceService()
        return attendance_service.delete(
            attendance_id=attendance_id,
        )
