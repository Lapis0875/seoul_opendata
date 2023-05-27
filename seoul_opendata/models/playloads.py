from typing import Optional, Required, TypedDict
from seoul_opendata.models.location import Location

from seoul_opendata.models.user import Gender
# User Data

class UserCreate(TypedDict):
    id: str
    password: str
    name: str
    phone: str
    email: Optional[str]
    age: int
    gender: Gender
    location: Location

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

class FacilityCreate(TypedDict):
    pass

class FacilityRead(TypedDict):
    pass

class FacilityUpdate(TypedDict):
    pass

class FacilityDelete(TypedDict):
    pass

class FacilityData(TypedDict):
    pass
