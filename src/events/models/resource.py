from typing import TYPE_CHECKING, Optional

from pydantic import PositiveInt, field_validator
from sqlmodel import Field, Relationship, SQLModel

from src.events.schemas import ResourceType

if TYPE_CHECKING:
    from src.events.models.event import Event


class Resource(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=128)
    type: ResourceType
    quantity_available: PositiveInt

    event_id: int = Field(foreign_key="event.id")
    event: Optional["Event"] = Relationship(back_populates="resources")

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name must not be empty")

        return v

    @field_validator("type")
    def valid_resource_type(cls, v: ResourceType) -> ResourceType:
        if v not in ResourceType:
            raise ValueError("Invalid resource type")

        return v

    @field_validator("quantity_available")
    def quantity_positive(cls, v: PositiveInt) -> PositiveInt:
        if v <= 0:
            raise ValueError("Quantity available must be positive")

        return v
