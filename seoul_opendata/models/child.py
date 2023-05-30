from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from seoul_opendata.models.child_school import ChildSchool
    from seoul_opendata.models.user import ParentUser

class Child(BaseModel):
    """아이 정보 모델."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    age: int
    parent: ParentUser
    school: ChildSchool | None = None
    
    def dict(self, *args, **kwargs):
        data: dict = super().dict(*args, **kwargs)
        data.pop("parent")
        data["parentId"] = self.parent.id
        
        data.pop("school")
        data["schoolCode"] = self.school.code if self.school else None
