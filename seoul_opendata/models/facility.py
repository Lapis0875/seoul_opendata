from pydantic import BaseModel


class FacilityBase(BaseModel):
    """유치원, 어린이집 모두가 공통으로 가지는 정보를 표현하는 모델."""

    name: str           # 시설명
    phone: str          # 시설 연락처
    location: None      # should be typed later.


class Kindergarten(FacilityBase):
    """유치원 모델."""


class DayCareCenter(FacilityBase):
    """유치원 모델."""