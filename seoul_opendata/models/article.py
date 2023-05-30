from datetime import date
from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from seoul_opendata.utils.dateutils import date2yyyy_mm_dd

from .child_school import ChildSchool
from .location import Location

class Article(BaseModel):
    """게시글 모델."""
    id: UUID = Field(default_factory=uuid4)
    title: str
    content: str
    attachments: list[str]
    location: Location
    childSchool: ChildSchool | None = Field(default=None, )
    uploadAt: date = Field(default_factory=date.today)
    
    def dict(self, *args, **kwargs) -> dict[str, Any]:
        data: dict[str, Any] = super().dict(*args, exclude={"id", "uploadAt", "childSchool"}, **kwargs)
        data["id"] = str(self.id)
        data["uploadAt"] = date2yyyy_mm_dd(self.uploadAt)
        data["childSchoolId"] = self.childSchool.code if self.childSchool else None
        return data
