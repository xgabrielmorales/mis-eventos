from typing import Optional

import strawberry
from pydantic import PositiveInt

from src.events.schemas import ResourceTypeEnum


@strawberry.type
class ResourceType:
    id: int
    name: str
    type: ResourceTypeEnum
    quantity_available: PositiveInt
    event_id: int


@strawberry.input
class ResourceInput:
    name: str
    type: ResourceTypeEnum
    quantity_available: PositiveInt
    event_id: int


@strawberry.input
class ResourceInputUpdate:
    name: Optional[str] = None
    type: Optional[ResourceTypeEnum] = None
    quantity_available: Optional[PositiveInt] = None
    event_id: Optional[int] = None
