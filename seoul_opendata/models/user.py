from __future__ import annotations

from enum import StrEnum
from typing import Optional
from pydantic import BaseModel, Field

from .location import Location
from .child import Child
    

class Gender(StrEnum):
    Male = M = "Male"
    Female = F = "Female"

class UserBase(BaseModel):
    """유저 공통 정보 모델."""
    id: str
    password: str
    name: str
    tel: str
    email: Optional[str]

class ParentUser(UserBase):
    """부모 유저 모델."""

    gender: Gender
    enrolled: bool = False                                  # 자녀가 유치원에 가입했는지 여부를 기록.
    children: list[Child] = Field(default_factory=list)     # 자녀 목록
    location: Location                                      # 거주 지역
