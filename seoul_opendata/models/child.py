from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from seoul_opendata.models.facility import ChildSchool

from seoul_opendata.models.user import ParentUser


class Child(BaseModel):
    """아이 정보 모델."""
    uuid: UUID = Field(default_factory=uuid4)
    name: str
    age: int
    parent: ParentUser
    school: ChildSchool | None = None
