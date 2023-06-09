from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from seoul_opendata.utils.dateutils import date2str
from .location import Location
from .establish_type import EstablishType
from .user import UserBase
from .child import Child


class ChildSchool(BaseModel):
    """유치원, 어린이집 모두가 공통으로 가지는 정보를 표현하는 모델."""
    code: str                                           # 유치원 고유 id
    name: str                                           # 시설명
    representerName: str                                # 대표자명
    tel: str                                            # 시설 연락처
    location: Location                                  # 지역
    address: str                                        # 주소
    establishType: EstablishType                        # 설립유형
    establishAt: date                                   # 설립일자
    openingTime: str                                    # 운영 시간
    articles: list[UUID]                                # 시설이 등록한 게시글 id 목록
    children: list[Child] = Field(default_factory=list)    # 해당 시설에 등록된 아이들
    
    def __init__(self, **data):
        datestr: str = data["establishAt"]
        data["establishAt"] = date(int(datestr[:4]), int(datestr[4:6]), int(datestr[6:]))
        super().__init__(**data)
    
    def dict(self, *args, **kwargs) -> dict[str, Any]:
        data: dict = super().dict(*args, **kwargs)
        dateObj: date = data["establishAt"]
        data["establishAt"] = date2str(self.establishAt)
        data["children"] = [c.id for c in self.children]
        return data

class ChildSchoolUser(UserBase):
    """기관 유저 모델."""
    childSchool: ChildSchool
    email: str

    @property
    def children(self) -> list[Child]:
        return self.childSchool.children
    