from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Child(BaseModel):
    """아이 정보 모델."""
    uuid: UUID = Field(default_factory=uuid4)
    name: str
    age: int
    parent: ParentUser
    school: ChildSchool | None = None

if TYPE_CHECKING:
    from seoul_opendata.models.facility import ChildSchool
    from seoul_opendata.models.user import ParentUser
    Child.update_forward_refs(ParentUser=ParentUser, ChildSchool=ChildSchool)
