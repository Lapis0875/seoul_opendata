from datetime import date

from pydantic import BaseModel
from seoul_opendata.models.establish_type import EstablishType

from seoul_opendata.models.location import Location
from seoul_opendata.models.playloads import ChildSchoolData
from seoul_opendata.models.user import UserBase


class ChildSchool(BaseModel):
    """유치원, 어린이집 모두가 공통으로 가지는 정보를 표현하는 모델."""
    code: str                  # 유치원 고유 id
    name: str                       # 시설명
    representerName: str            # 대표자명
    tel: str                        # 시설 연락처
    location: Location              # 지역
    address: str                    # 주소
    establishType: EstablishType    # 설립유형
    establishAt: date               # 설립일자
    openingTime: str                # 운영 시간
    
    def __init__(self, **data):
        datestr: str = data["establishAt"]
        data["establishAt"] = date(int(datestr[:4]), int(datestr[4:6]), int(datestr[6:]))
        super().__init__(**data)
    
    def dict(self) -> ChildSchoolData:
        data: ChildSchoolData = super().dict()
        dateObj: date = data["establishAt"]
        data["establishAt"] = f"{dateObj.year}{dateObj.month:02d}{dateObj.day}"
        return data

class FacilityUser(UserBase):
    """기관 유저 모델."""
    facility: ChildSchool
    