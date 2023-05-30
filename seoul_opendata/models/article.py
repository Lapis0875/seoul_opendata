from datetime import date
from pydantic import BaseModel, Field

from seoul_opendata.models.facility import ChildSchool


class Article(BaseModel):
    """게시글 모델."""
    title: str
    content: str
    uploadAt: date
    childSchool: ChildSchool
