from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.events.schemas import ResourceType

if TYPE_CHECKING:
    from src.events.models.event import Event


class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=128)
    type: ResourceType
    quantity_available: int
    event_id: int = Field(foreign_key="event.id")
    event: Optional["Event"] = Relationship(back_populates="resources")
