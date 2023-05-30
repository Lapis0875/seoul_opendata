from __future__ import annotations

from typing import Optional, Required, TypedDict, TypeVar
from .establish_type import EstablishType
from .location import Location
from .facility import ChildSchool
from .user import Gender, ParentUser

# Response Data

class Message(TypedDict, total=False):
    message: str
    code: Required[str]
    api_version: str

M = TypeVar("M")    # Model for Response.
ModelOrMessage = M | Message

# Child Data
class ChildData(TypedDict):
    name: str
    age: int
    parent_id: str
    school_code: str | None

# Child Data
class ChildObject(TypedDict):
    name: str
    age: int
    parent: ParentUser
    school: ChildSchool | None

# Child Data
class ChildRead(TypedDict):
    uuid: str
    name: str
    age: int
    parent_id: str
    school_code: str | None

# Child Data
class ChildDelete(TypedDict):
    uuid: str
    name: str
    age: int
    parent_id: str
    school_code: str | None

# User Data

class UserCreate(TypedDict, total=False):
    id: Required[str]
    password: Required[str]
    name: Required[str]
    phone: Required[str]
    email: str
    age: Required[int]
    gender: Required[Gender]
    location: Required[Location]

class UserRead(TypedDict, total=False):
    id: Required[str]
    email: str
    phone: str

class UserUpdate(TypedDict, total=False):
    id: Required[str]     # id used to find user.
    # updatable data
    password: str 
    name: str
    email: str
    age: int
    location: Location

class UserDelete(TypedDict, total=False):
    id: Required[str]
    password: Required[str]
    phone: str

class UserData(TypedDict):
    name: str
    id: str
    phone: str
    email: Optional[str]
    password: str
    age: int
    gender: Gender
    location: Location

class UserLogin(TypedDict):
    id: str
    password: str

# Facility Data

class ChildSchoolCreate(TypedDict):
    code: str                  # 유치원 고유 id
    name: str                       # 시설명
    representerName: str            # 대표자명
    tel: str                        # 시설 연락처
    location: Location              # 지역
    address: str                    # 주소
    establishType: EstablishType    # 설립유형
    establishAt: str                # 설립일자
    openingTime: str                # 운영 시간

class ChildSchoolRead(TypedDict, total=False):
    code: Required[str]        # 유치원 고유 id
    name: str                       # 시설명

class ChildSchoolUpdate(TypedDict, total=False):
    code: Required[str]                  # 유치원 고유 id
    name: str                       # 시설명
    representerName: str            # 대표자명
    tel: str                        # 시설 연락처
    openingTime: str                # 운영 시간

class ChildSchoolDelete(TypedDict, total=False):
    code: Required[str]        # 유치원 고유 id
    name: str                       # 시설명

class ChildSchoolData(TypedDict):
    code: str                  # 유치원 고유 id
    name: str                       # 시설명
    representerName: str            # 대표자명
    tel: str                        # 시설 연락처
    location: Location              # 지역
    address: str                    # 주소
    establishType: EstablishType    # 설립유형
    establishAt: str                # 설립일자
    openingTime: str                # 운영 시간
    children: list[ChildData]
