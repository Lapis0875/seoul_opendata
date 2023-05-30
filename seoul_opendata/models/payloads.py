from __future__ import annotations
from datetime import date
from turtle import st

from typing import Optional, Required, TypedDict, TypeVar

from pydantic import BaseModel, Field
from .establish_type import EstablishType
from .location import Location
from .child_school import ChildSchool
from .user import Gender, ParentUser

# Response Data

class Message(BaseModel):
    message: str
    code: str
    apiVersion: Optional[str] = Field(default=None)

M = TypeVar("M")    # Model for Response.
ModelOrMessage = M | Message

# Child Data
class ChildCreate(BaseModel):
    name: str
    age: int
    parentId: str
    schoolCode: Optional[str] = Field(default=None)

# Child Data
class ChildData(TypedDict):
    id: str
    name: str
    age: int
    parentId: str
    schoolCode: Optional[str]

# Child Data
class ChildRead(BaseModel):
    id: str
    name: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    parentId: Optional[str] = Field(default=None)
    schoolCode: Optional[str] = Field(default=None)

# Child Data
class ChildUpdate(BaseModel):
    id: str
    parentId: str
    name: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    schoolCode: Optional[str] = Field(default=None)

# Child Data
class ChildDelete(BaseModel):
    id: str
    name: str
    age: int
    parentId: str
    schoolCode: Optional[str] = Field(default=None)

# User Data

class UserCreate(BaseModel):
    id: str
    password: str
    name: str
    tel: str
    gender: Gender
    location: Location
    email: Optional[str] = Field(default=None)

class UserRead(BaseModel):
    id: str
    email: Optional[str] = Field(default=None)
    tel: Optional[str] = Field(default=None)

class UserUpdate(BaseModel):
    id: str                 # id used to find user.
    # updatable data
    password: str
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    gender: Optional[Gender] = Field(default=None)
    location: Optional[Location] = Field(default=None)

class UserDelete(BaseModel):
    id: str
    password: str

class UserData(TypedDict):
    name: str
    id: str
    tel: str
    password: str
    gender: Gender
    location: Location
    children: list[str]
    email: Optional[str]

# ChildSchoolUser Data

class ChildSchoolUserCreate(BaseModel):
    id: str                         # 유치원 고유 id
    password: str
    name: str                       # 시설명
    tel: str                        # 시설 연락처
    email: str                      # 시설 email

class ChildSchoolUserRead(BaseModel):
    id: str
    email: Optional[str] = Field(default=None)
    tel: Optional[str] = Field(default=None)\

class ChildSchoolUserUpdate(BaseModel):
    id: str     # id used to find user.
    # updatable data
    password: Optional[str]  = Field(default=None)
    name: Optional[str] = Field(default=None)
    tel: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)

class ChildSchoolUserDelete(BaseModel):
    id: str
    password: str

class ChildSchoolUserData(TypedDict):
    id: str
    password: str
    name: str
    tel: str
    email: str

class UserLogin(BaseModel):
    id: str
    password: str

# Facility Data

class ChildSchoolCreate(BaseModel):
    code: str                       # 유치원 고유 id
    name: str                       # 시설명
    representerName: str            # 대표자명
    tel: str                        # 시설 연락처
    location: Location              # 지역
    address: str                    # 주소
    establishType: EstablishType    # 설립유형
    establishAt: str                # 설립일자
    openingTime: str                # 운영 시간
    children: list[str]             # 자녀 목록

class ChildSchoolRead(BaseModel):
    code: str        # 유치원 고유 id

class ChildSchoolUpdate(BaseModel):
    code: str                                                       # 유치원 고유 id
    name: Optional[str] = Field(default=None)                       # 시설명
    representerName: Optional[str] = Field(default=None)            # 대표자명
    tel: Optional[str] = Field(default=None)                    # 시설 email
    openingTime: Optional[str] = Field(default=None)                # 운영 시간
    children: Optional[list[str]] = Field(default=None)

class ChildSchoolDelete(BaseModel):
    code: str        # 유치원 고유 id

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
    children: list[str]

class ArticleCreate(BaseModel):
    title: str
    content: str
    attachments: list[str]
    location: Location
    childSchoolId: Optional[str] = Field(default=None)
    uploadAt: Optional[str] = Field(default_factory=date.today)

class ArticleRead(BaseModel):
    id: str
    childSchoolId: Optional[str] = Field(default=None)

class ArticleUpdate(BaseModel):
    id: str
    title: Optional[str]
    content: Optional[str]
    attachments: Optional[list[str]]
    location: Optional[Location]
    childSchoolId: Optional[str] = Field(default=None)

class ArticleDelete(BaseModel):
    id: str
    childSchoolId: Optional[str] = Field(default=None)

class ArticleData(TypedDict):
    id: str
    title: str
    content: str
    attachments: list[str]
    location: str
    uploadAt: str
    childSchoolId: Optional[str]
