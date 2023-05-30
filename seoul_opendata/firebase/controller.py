from abc import ABCMeta, abstractmethod
from typing import Any, Final, cast
from firebase_admin import db
from firebase_admin.credentials import Certificate
import firebase_admin
from seoul_opendata.models.child import Child
from seoul_opendata.models.establish_type import EstablishType
from seoul_opendata.models.facility import ChildSchool
from seoul_opendata.models.location import Location

from seoul_opendata.models.payloads import ChildData, ChildObject, ChildRead, ChildSchoolCreate, ChildSchoolData, ChildSchoolDelete, ChildSchoolRead, ChildSchoolUpdate, UserCreate, UserData, UserDelete, UserRead, UserUpdate
from seoul_opendata.models.user import Gender, ParentUser

CRED_OBJ: Final[Certificate] = Certificate("firebase_cert.json")

firebase_admin.initialize_app(CRED_OBJ, {"databaseURL": "https://project-seoulmom-default-rtdb.firebaseio.com/"})

class CRUDRepository(metaclass=ABCMeta):
    """Repository base class supporting CRUD operations."""
    repo: Final[db.Reference]
    
    def __init__(self, repo: db.Reference) -> None:
        super().__init__()
        self.repo = repo
    
    @abstractmethod
    def create(self, payload: dict[str, Any]) -> Any:
        """Create new element in this repository."""
    
    @abstractmethod
    def read(self, payload: dict[str, Any]) -> Any:
        """Create new element in this repository."""
    
    @abstractmethod
    def update(self, payload: dict[str, Any]) -> Any:
        """Create new element in this repository."""
    
    @abstractmethod
    def delete(self, payload: dict[str, Any]) -> Any:
        """Create new element in this repository."""
    
class ParentUserRepository(CRUDRepository):
    """CRUD Repository for ParentUser."""
    
    def create(self, payload: UserCreate) -> ParentUser:
        user = ParentUser(**payload)
        self.repo.child(user.id).update(user.dict())
        return user
    
    def read(self, payload: UserRead) -> ParentUser:
        return ParentUser(**cast(UserData, self.repo.child(payload["id"]).get()))

    def update(self, payload: UserUpdate) -> ParentUser:
        node: db.Reference = self.repo.child(payload["id"])
        user = ParentUser(**cast(UserData, node.get()))
        for key in payload:
            if payload[key] is not None:
                setattr(user, key, payload[key])    # update user model.
        node.update(user.dict())    # update firebase data.
        return user
    
    def delete(self, payload: UserDelete) -> ParentUser:
        node: db.Reference = self.repo.child(payload["id"])
        user = ParentUser(**cast(UserData, node.get()))
        node.delete()
        return user


class ChildSchoolRepository(CRUDRepository):
    """CRUD Repository for ChildSchool."""
    
    def create(self, payload: ChildSchoolCreate) -> ChildSchool:
        # print(f"ChildSchoolRepository.create : code={payload['code']}")
        childSchool = ChildSchool(**payload)
        self.repo.child(childSchool.code).update(childSchool.dict())
        return childSchool
    
    def read_all(self) -> dict[str, ChildSchool]:
        data: dict[str, ChildSchool] = {}
        
        if data is None:
            return {}
        query_result: dict[str, ChildSchoolData] = cast(dict[str, ChildSchoolData], self.repo.get())
        
        for code, entry in query_result.items():
            data[code] = ChildSchool(**entry)
    
        return data
    
    def read(self, payload: ChildSchoolRead) -> ChildSchool | None:
        data: dict | None = cast(dict | None, self.repo.child(payload["code"]).get())
        return None if data is None else ChildSchool(**cast(ChildSchoolData, data))

    def update(self, payload: ChildSchoolUpdate) -> ChildSchool:
        node: db.Reference = self.repo.child(payload["code"])
        childSchool = ChildSchool(**cast(ChildSchoolData, node.get()))
        for key in payload:
            if payload[key] is not None:
                setattr(childSchool, key, payload[key])    # update user model.
        node.update(childSchool.dict())    # update firebase data.
        return childSchool
    
    def delete(self, payload: ChildSchoolDelete) -> ChildSchool:
        node: db.Reference = self.repo.child(payload["code"])
        childSchool = ChildSchool(**cast(ChildSchoolData, node.get()))
        node.delete()
        return childSchool


class ChildRepository(CRUDRepository):
    """CRUD Repository for Child."""
    parentUserRepo: Final[ParentUserRepository]
    childSchoolRepo: Final[ChildSchoolRepository]
    
    def __init__(self, repo: db.Reference, parentUserRepo: ParentUserRepository, childSchoolRepos: ChildSchoolRepository) -> None:
        self.parentUserRepo = parentUserRepo
        self.childSchoolRepo = childSchoolRepos
        super().__init__(repo)
    
    def create(self, payload: ChildData) -> Child | None:
        parent: ParentUser | None = self.parentUserRepo.read({"id": payload["parent_id"]})
        if parent is None:
            return None
        
        obj: ChildObject = {
            "name": payload["name"],
            "age": payload["age"],
            "parent": parent,
            "school": None if payload["school_code"] is None else self.childSchoolRepo.read({"code": payload["school_code"]}),
        }
        child = Child(**obj)
        child.parent.children.append(child)
        self.repo.child(child.uuid).update(child.dict())
        return child
    
    def read(self, payload: ChildRead) -> Child | None:
        return Child(**cast(ChildObject, self.repo.child(payload["uuid"]).get()))

    def update(self, payload: ChildRead) -> Child | None:
        node: db.Reference = self.repo.child(payload["uuid"])
        data: dict | None = cast(dict | None, node.get())
        if data is None:
            return None
        
        child = Child(**cast(ChildObject, data))
        for key in payload:
            if payload[key] is not None:
                setattr(child, key, payload[key])    # update user model.
        node.update(child.dict())    # update firebase data.
        return child
    
    def delete(self, payload: ChildSchoolDelete) -> ChildSchool:
        node: db.Reference = self.repo.child(payload["code"])
        childSchool = ChildSchool(**cast(ChildSchoolData, node.get()))
        node.delete()
        return childSchool


class FirebaseController:
    """
    Middleware to abstract Firebase Database access.
    All operations we need to do with Firebase Database should be implemetned here.
    """
    root: Final[db.Reference]
    parentUser: Final[ParentUserRepository]
    childSchool: Final[ChildSchoolRepository]
    child: Final[ChildRepository]
    
    def __init__(self) -> None:
        self.root = db.reference("/")
        self.parentUser = ParentUserRepository(self.root.child("users/parent"))
        self.childSchool = ChildSchoolRepository(self.root.child("childschool"))
        self.child = ChildRepository(self.root.child("children"), self.parentUser, self.childSchool)
    
    def debug_user_feature(self):
        self.parentUser.create({
            "id": "lapis0875",
            "password": "1234",
            "name": "김민준",
            "phone": "010-1234-5678",
            "email": "lapis0875@gmail.com",
            "age": 21,
            "gender": Gender.Male,
            "location": Location.GangBuk
        })
        self.parentUser.read({"id": "lapis0875"})
        self.parentUser.update({"id": "lapis0875", "password": "5678"})
        self.parentUser.delete({"id": "lapis0875", "password": "5678"})
    
    def debug_childschool_feature(self):
        self.childSchool.create({
            "code": "1ecec08c-f932-b044-e053-0a32095ab044",
            "name": "유성유치원",
            "representerName": "유성유치원",
            "location": Location.YongSan,
            "address": "서울특별시 용산구 회나무로13가길 16",
            "establishType": EstablishType.PRIVATE,
            "establishAt": "19650927",
            "openingTime": "08:40~18:00",
            "tel": "02-792-8691",
        })
        self.childSchool.read({"code": "1ecec08c-f932-b044-e053-0a32095ab044"})
        self.childSchool.update({"code": "1ecec08c-f932-b044-e053-0a32095ab044", "openingTime": "09:00~20:00"})
        self.childSchool.delete({"code": "1ecec08c-f932-b044-e053-0a32095ab044"})

DB: Final[FirebaseController] = FirebaseController()
