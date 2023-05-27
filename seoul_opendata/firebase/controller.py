from abc import ABCMeta, abstractmethod
from typing import Any, Final, cast
from firebase_admin import db
from firebase_admin.credentials import Certificate
import firebase_admin
from seoul_opendata.models.location import Location

from seoul_opendata.models.playloads import UserCreate, UserData, UserDelete, UserRead, UserUpdate
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


class FirebaseController:
    """
    Middleware to abstract Firebase Database access.
    All operations we need to do with Firebase Database should be implemetned here.
    """
    root: Final[db.Reference]
    parentUser: Final[ParentUserRepository]
    
    def __init__(self) -> None:
        self.root = db.reference("/")
        self.parentUser = ParentUserRepository(self.root.child("users/parent"))
    
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
