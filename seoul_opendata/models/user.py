from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Literal, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from seoul_opendata.models.facility import DayCareCenter, Kindergarten

class Gender(StrEnum):
    Male = M = "Male"
    Female = F = "Female"

class UserBase(BaseModel):
    """유저 공통 정보 모델."""
    id: str
    password: str
    name: str
    phone: str
    email: Optional[str]
    age: int
    gender: Gender

class ParentUser(UserBase):
    """부모 유저 모델."""

    enrolled: bool = False  # 자녀가 유치원에 가입했는지 여부를 기록.
