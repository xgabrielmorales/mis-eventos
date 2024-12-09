import strawberry

from src.auth.middleware.jwt_middleware import IsAuthenticated
from src.events.graphql.nodes import AttendanceType
from src.events.services.attendance import AttendanceService


@strawberry.type
class AttendanceQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def get_attendance_by_id(self, attendance_id: int) -> AttendanceType:
        attendance_service = AttendanceService()
        return attendance_service.get_by_id(attendance_id=attendance_id)

    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[misc]
    def get_all_attendances(self) -> list[AttendanceType]:
        attendance_service = AttendanceService()
        return attendance_service.get_all()
