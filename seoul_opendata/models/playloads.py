from typing import Optional, TypedDict

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

class UserRead(TypedDict):
    id: str
    email: Optional[str]
    phone: Optional[str]

class UserUpdate(TypedDict):
    id: str     # id used to find user.
    # updatable data
    password: Optional[str] 
    name: Optional[str]
    email: Optional[str]
    age: int

class UserDelete(TypedDict):
    id: str
    password: str
    phone: str

class UserData(TypedDict):
    name: str
    id: str
    phone: str
    email: Optional[str]
    password: str
    age: int
    gender: Gender

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
