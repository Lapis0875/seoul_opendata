from abc import ABCMeta, abstractmethod
from datetime import date
from turtle import st
from typing import Any, Final, Type, cast
from firebase_admin import db, initialize_app
from firebase_admin.credentials import Certificate
from pydantic import BaseModel
from seoul_opendata.models import Article, Child, ChildSchool, Location, EstablishType, ParentUser, Gender, ChildSchoolUser, article, child

from seoul_opendata.models.payloads import ArticleCreate, ArticleData, ArticleDelete, ArticleRead, ArticleUpdate, ChildCreate, ChildData, ChildDelete, ChildRead, ChildSchoolCreate, ChildSchoolData, ChildSchoolDelete, ChildSchoolRead, ChildSchoolUpdate, ChildSchoolUserCreate, ChildSchoolUserData, ChildSchoolUserDelete, ChildSchoolUserRead, ChildSchoolUserUpdate, ChildUpdate, Message, UserCreate, UserData, UserDelete, UserRead, UserUpdate
from seoul_opendata.utils.dateutils import str2date, yyyy_mm_dd2date

CRED_OBJ: Final[Certificate] = Certificate("firebase_cert.json")

initialize_app(CRED_OBJ, {"databaseURL": "https://project-seoulmom-default-rtdb.firebaseio.com/"})

class DBException(Exception):
    """Base class of exception occurred in controller layer."""
    message: Message
    
class EntryNotExist(DBException):
    entryType: Type[BaseModel]
    key: str
    
    def __init__(self, entryType: Type[BaseModel], key: str) -> None:
        super().__init__({
            "message": f"Entry of type {entryType.__name__} with key {key} does not exist.",
            "code": "ENTRY_NOT_EXISTS"
        })
        self.entryType = entryType
        self.key = key

class EntryAlreadyExist(DBException):
    entryType: Type[BaseModel]
    key: str
    
    def __init__(self, entryType: Type[BaseModel], key: str) -> None:
        super().__init__({
            "message": f"Entry of type {entryType.__name__} with key {key} already exists.",
            "code": "ENTRY_ALREADY_EXISTS"
        })
        self.entryType = entryType
        self.key = key


class CRUDRepository(metaclass=ABCMeta):
    """Repository base class supporting CRUD operations."""
    repo: Final[db.Reference]
    controller: "FirebaseController"
    
    def __init__(self, repo: db.Reference, controller: "FirebaseController") -> None:
        super().__init__()
        self.repo = repo
        self.controller = controller
    
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
    
    @property
    def childRepo(self) -> "ChildRepository":
        return self.controller.child
    
    def create(self, payload: UserCreate) -> ParentUser:
        prev: dict | None = self.repo.child(payload.id).get()   # type: ignore
        if prev is not None:
            raise EntryAlreadyExist(ParentUser, payload.id)
        
        user = ParentUser(
            id=payload.id,
            name=payload.name,
            email=payload.email,
            tel=payload.tel,
            children=[],
            location=payload.location,
            gender=payload.gender,
            password=payload.password
        )
        self.repo.child(user.id).update(user.dict())
        return user
    
    def read(self, payload: UserRead) -> ParentUser:
        assert self.childRepo is not None       # Type assertion. Always True if initialized properly.
        
        data: UserData | None = self.repo.child(payload.id).get()  # type: ignore
        if data is None:
            raise EntryNotExist(ParentUser, payload.id)
        
        data["children"] = [self.childRepo.read(ChildRead(id=cid)) for cid in data["children"]]   # type: ignore
        
        return ParentUser(**data)   # type: ignore since resolved from above.

    def update(self, payload: UserUpdate) -> ParentUser | None:
        node: db.Reference = self.repo.child(payload.id)
        data: dict | None = node.get()  # type: ignore
        if data is None:
            raise EntryNotExist(ParentUser, payload.id)
        
        user = ParentUser(**data)
        if payload.name is not None:
            user.name = payload.name
        if payload.password is not None:
            user.password = payload.password
        if payload.email is not None:
            user.email = payload.email
        if payload.location is not None:
            user.location = payload.location
        if payload.gender is not None:
            user.gender = payload.gender
        node.update(user.dict())    # update firebase data.
        return user
    
    def delete(self, payload: UserDelete) -> ParentUser:
        node: db.Reference = self.repo.child(payload.id)
        data: dict | None = node.get()  # type: ignore
        if data is None:
            raise EntryNotExist(ParentUser, payload.id)
    
        user = ParentUser(**data)
        node.delete()
        return user


class ChildSchoolRepository(CRUDRepository):
    """CRUD Repository for ChildSchool."""
    
    @property
    def childRepo(self) -> "ChildRepository":
        return self.controller.child
    
    def create(self, payload: ChildSchoolCreate) -> ChildSchool:
        assert self.childRepo is not None
        
        prev: dict | None = self.repo.child(payload.code).get()   # type: ignore
        if prev is not None:
            raise EntryAlreadyExist(ChildSchoolCreate, payload.code)
        
        childSchool = ChildSchool(
            code=payload.code,
            name=payload.name,
            representerName=payload.representerName,
            address=payload.address,
            tel=payload.tel,
            location=payload.location,
            establishType=payload.establishType,
            openingTime=payload.openingTime,
            articles=[],
            children=[cast(Child, self.childRepo.read(ChildRead(id=cid))) for cid in payload.children]
        )
        
        self.repo.child(childSchool.code).update(childSchool.dict())
        return childSchool
    
    def readAll(self) -> dict[str, ChildSchool]:
        assert self.childRepo is not None       # Type assertion. Always True if initialized properly.
        
        data: dict[str, ChildSchoolData] = self.repo.get()  # type: ignore
        res: dict[str, ChildSchool] = {}
        
        if data is None:
            return {}
        
        for code, entry in data.items():
            entry["children"] = [self.childRepo.read(ChildRead(id=cid)) for cid in entry["children"]]   # type: ignore
            res[code] = ChildSchool(**entry)
    
        return res
    
    def read(self, payload: ChildSchoolRead) -> ChildSchool:
        assert self.childRepo is not None       # Type assertion. Always True if initialized properly.
        data: ChildSchoolData | None = cast(ChildSchoolData | None, self.repo.child(payload.code).get())
        if data is None:
            raise EntryNotExist(ChildSchool, payload.code)
        
        data["children"] = [self.childRepo.read(ChildRead(id=cid)) for cid in data["children"]]   # type: ignore
        
        return ChildSchool(**data)

    def update(self, payload: ChildSchoolUpdate) -> ChildSchool:
        node: db.Reference = self.repo.child(payload.code)
        childSchool = ChildSchool(**cast(ChildSchoolData, node.get()))
        
        if payload.name is not None:
            childSchool.name = payload.name
        if payload.representerName is not None:
            childSchool.representerName = payload.representerName
        if payload.tel is not None:
            childSchool.tel = payload.tel
        if payload.openingTime is not None:
            childSchool.openingTime = payload.openingTime
        if payload.children is not None:
            childSchool.children = [
                cast(Child, self.childRepo.read(ChildRead(id=cid)))
                for cid
                in payload.children
            ]
        
        
        node.update(childSchool.dict())    # update firebase data.
        return childSchool
    
    def delete(self, payload: ChildSchoolDelete) -> ChildSchool:
        node: db.Reference = self.repo.child(payload.code)
        data: ChildSchoolData | None = node.get()  # type: ignore
        
        if data is None:
            raise EntryNotExist(ChildSchool, payload.code)
        
        data["children"] = [self.childRepo.read(ChildRead(id=cid)) for cid in data["children"]]   # type: ignore
        
        childSchool = ChildSchool(**data)
        node.delete()
        return childSchool


class ChildSchoolNotExist(DBException):
    def __init__(self, code: str) -> None:
        super().__init__({
            "message": f"ChildSchool with code {code} does not exist.",
            "code": "INVALID_CHILD_SCHOOL_CODE"
        })


class ChildSchoolUserRepository(CRUDRepository):
    """CRUD Repository for ChildSchoolUser."""
    @property
    def childSchoolRepo(self) -> ChildSchoolRepository:
        return self.controller.childSchool
    
    def create(self, payload: ChildSchoolUserCreate) -> ChildSchoolUser:
        childSchool: ChildSchool | None = self.childSchoolRepo.read(ChildSchoolRead(code=payload.id))
        
        if childSchool is None:
            raise ChildSchoolNotExist(payload.id)
            
        user = ChildSchoolUser(
            id=payload.id,
            name=payload.name,
            email=payload.email,
            tel=payload.tel,
            password=payload.password,
            childSchool=childSchool
        )
        self.repo.child(user.id).update(user.dict())
        return user
    
    def read(self, payload: ChildSchoolUserRead) -> ChildSchoolUser:
        data: ChildSchoolUserData | None = cast(ChildSchoolUserData | None, self.repo.child(payload.id).get())
        if data is None:
            raise EntryNotExist(ChildSchoolUser, payload.id)
        
        return ChildSchoolUser(
            childSchool=cast(ChildSchool, self.childSchoolRepo.read(ChildSchoolRead(code=payload.id))),
            **data
        )

    def update(self, payload: ChildSchoolUserUpdate) -> ChildSchoolUser:
        node: db.Reference = self.repo.child(payload.id)
        data: ChildSchoolUserData | None = cast(ChildSchoolUserData | None, node.get())
        
        if data is None:
            raise EntryNotExist(ChildSchoolUser, payload.id)
        user: ChildSchoolUser = ChildSchoolUser(
            childSchool=cast(ChildSchool, self.childSchoolRepo.read(ChildSchoolRead(code=payload.id))),
            **data
        )
        
        # update model.
        if payload.password is not None:
            user.password = payload.password
        if payload.name is not None:
            user.name = payload.name
        if payload.tel is not None:
            user.tel = payload.tel
        if payload.email is not None:
            user.email = payload.email
        
        node.update(user.dict())    # update firebase data.
        return user
    
    def delete(self, payload: ChildSchoolUserDelete) -> ChildSchoolUser:
        node: db.Reference = self.repo.child(payload.id)
        data: ChildSchoolUserData | None = node.get()  # type: ignore
        
        if data is None:
            raise EntryNotExist(ChildSchoolUser, payload.id)
        
        user = ChildSchoolUser(
            childSchool=cast(ChildSchool, self.childSchoolRepo.read(ChildSchoolRead(code=payload.id))),
            **data
        )
        node.delete()
        return user


class ChildRepository(CRUDRepository):
    """CRUD Repository for Child."""
    
    @property
    def parentUserRepo(self) -> ParentUserRepository:
        return self.controller.parentUser
    
    @property
    def childSchoolRepo(self) -> ChildSchoolRepository:
        return self.controller.childSchool
    
    def create(self, payload: ChildCreate) -> Child:
        parent: ParentUser | None = self.parentUserRepo.read(UserRead(id=payload.parentId))
        if parent is None:
            raise EntryNotExist(ParentUser, payload.parentId)
        
        childSchool: ChildSchool | None = None
        if payload.schoolCode is not None:
            childSchool = self.childSchoolRepo.read(ChildSchoolRead(code=payload.schoolCode))
        
        child = Child(
            name=payload.name,
            age=payload.age,
            parent=parent,
            school=childSchool
        )
        child.parent.children.append(child)
        self.repo.child(child.id).update(child.dict())
        return child
    
    def read(self, payload: ChildRead) -> Child:
        data: ChildData | None = cast(ChildData | None, self.repo.child(payload.id).get())
        
        if data is None:
            raise EntryNotExist(Child, payload.id)
        
        parent: ParentUser = cast(ParentUser, self.parentUserRepo.read(UserRead(id=data["parentId"])))
        school: ChildSchool | None = None
        if (schoolCode := data["schoolCode"]) is not None:
            school = cast(ChildSchool, self.childSchoolRepo.read(ChildSchoolRead(code=schoolCode)))
        
        return Child(
            name=data["name"],
            age=data["age"],
            parent=parent,
            school=school
        )

    def update(self, payload: ChildUpdate) -> Child:
        node: db.Reference = self.repo.child(payload.id)
        data: ChildData | None = cast(ChildData | None, node.get())
        if data is None:
            raise EntryNotExist(Child, payload.id)
        
        parent: ParentUser = cast(ParentUser, self.parentUserRepo.read(UserRead(id=data["parentId"])))
        school: ChildSchool | None = None
        if (schoolCode := data["schoolCode"]) is not None:
            school = cast(ChildSchool, self.childSchoolRepo.read(ChildSchoolRead(code=schoolCode)))
        
        child = Child(
            name=data["name"],
            age=data["age"],
            parent=parent,
            school=school
        )
        
        # update user model.
        if payload.name is not None:
            child.name = payload.name
        if payload.age is not None:
            child.age = payload.age
        if payload.schoolCode is not None:
            child.school = self.childSchoolRepo.read(ChildSchoolRead(code=payload.schoolCode))
        
        node.update(child.dict())    # update firebase data.
        return child
    
    def delete(self, payload: ChildDelete) -> Child:
        node: db.Reference = self.repo.child(payload.id)
        data: ChildData | None = node.get() # type: ignore
        if data is None:
            raise EntryNotExist(Child, payload.id)
        
        parent: ParentUser = cast(ParentUser, self.parentUserRepo.read(UserRead(id=data["parentId"])))
        school: ChildSchool | None = None
        if (schoolCode := data["schoolCode"]) is not None:
            school = cast(ChildSchool, self.childSchoolRepo.read(ChildSchoolRead(code=schoolCode)))
        
        child = Child(
            name=data["name"],
            age=data["age"],
            parent=parent,
            school=school
        )
        node.delete()
        return child

class ArticleRepository(CRUDRepository):
    """CRUD Repository for Article"""
    
    @property
    def childSchoolRepo(self) -> ChildSchoolRepository:
        return self.controller.childSchool
    
    def createEventArticle(self, payload: ArticleCreate) -> Article:
        # event article
        if payload.uploadAt is not None:
            article = Article(
                title=payload.title,
                content=payload.content,
                attachments=payload.attachments,
                location=Location(payload.location),
                uploadAt=yyyy_mm_dd2date(payload.uploadAt),
                childSchool=None
            )
        else:
            article = Article(
                title=payload.title,
                content=payload.content,
                attachments=payload.attachments,
                location=Location(payload.location),
                childSchool=None
            )
            
        self.repo.child(f"events/{article.id}").update(article.dict())
        return article
    
    def createChildSchoolArticle(self, payload: ArticleCreate) -> Article:
        # child school article
        childSchoolId: str = cast(str, payload.childSchoolId)
        childSchool: ChildSchool | None = self.childSchoolRepo.read(ChildSchoolRead(code=childSchoolId))
        if childSchool is None:
            raise EntryNotExist(ChildSchool, childSchoolId)
        
        if payload.uploadAt is not None:
            article = Article(
                title=payload.title,
                content=payload.content,
                attachments=payload.attachments,
                location=Location(payload.location),
                uploadAt=yyyy_mm_dd2date(payload.uploadAt),
                childSchool=childSchool
            )
        else:
            article = Article(
                title=payload.title,
                content=payload.content,
                attachments=payload.attachments,
                location=Location(payload.location),
                childSchool=childSchool
            )
        
        self.repo.child(f"{childSchoolId}/{article.id}").update(article.dict())
        return article
    
    def create(self, payload: ArticleCreate) -> Article:
        childSchoolId: str | None = payload.childSchoolId
        if childSchoolId is None:
            return self.createEventArticle(payload)
        else:
            return self.createChildSchoolArticle(payload)
    
    def readAll(self) -> dict[str, dict[str, Article]]:
        data: dict[str, dict[str, ArticleData]] | None = cast(dict[str, dict[str, ArticleData]] | None, self.repo.get())
        res: dict[str, dict[str, Article]] = {}
        
        if data is None:
            return {}
        
        for childSchool, articles in data.items():
            res[childSchool] = {}
            for articleId, articleData in articles.items():
                childSchoolId = articleData["childSchoolId"]
                if childSchoolId is None:
                    res[childSchool][articleId] = Article(
                        title=articleData["title"],
                        content=articleData["content"],
                        attachments=articleData["attachments"],
                        location=Location(articleData["location"]),
                        uploadAt=str2date(articleData["uploadAt"]),
                        childSchool=None
                    )
                else:
                    res[childSchool][articleId] = Article(
                        title=articleData["title"],
                        content=articleData["content"],
                        attachments=articleData["attachments"],
                        location=Location(articleData["location"]),
                        uploadAt=str2date(articleData["uploadAt"]),
                        childSchool=self.childSchoolRepo.read(ChildSchoolRead(code=childSchoolId))
                    )
    
        return res
    
    def readAllEventArticles(self) -> dict[str, Article]:
        data: dict[str, ArticleData] | None = cast(dict[str, ArticleData] | None, self.repo.child("events").get())
        res: dict[str, Article] = {}
        
        if data is None:
            return {}
        
        for articleId, articleData in data.items():
            res[articleId] = Article(
                title=articleData["title"],
                content=articleData["content"],
                attachments=articleData["attachments"],
                location=Location(articleData["location"]),
                uploadAt=str2date(articleData["uploadAt"]),
                childSchool=None
            )
    
        return res
    
    def readAllChildSchoolArticles(self, childSchoolId: str) -> dict[str, Article]:
        data: dict[str, ArticleData] | None = cast(dict[str, ArticleData] | None, self.repo.child(childSchoolId).get())
        res: dict[str, Article] = {}
        
        if data is None:
            return {}

        childSchool = self.childSchoolRepo.read(ChildSchoolRead(code=childSchoolId))
        
        for articleId, articleData in data.items():
            res[articleId] = Article(
                title=articleData["title"],
                content=articleData["content"],
                attachments=articleData["attachments"],
                location=Location(articleData["location"]),
                uploadAt=str2date(articleData["uploadAt"]),
                childSchool=childSchool
            )
    
        return res
    
    def readEventArticle(self, payload: ArticleRead) -> Article:
        data: ArticleData | None = cast(ArticleData | None, self.repo.child(f"events/{payload.id}").get())
        
        if data is None:
            raise EntryNotExist(Article, payload.id)
        
        return Article(
            title=data["title"],
            content=data["content"],
            attachments=data["attachments"],
            location=Location(data["location"]),
            uploadAt=str2date(data["uploadAt"]),
            childSchool=None
        )
    
    def readChildSchoolArticle(self, payload: ArticleRead) -> Article:
        childSchoolId: str = cast(str, payload.childSchoolId)
        data: ArticleData | None = cast(ArticleData | None, self.repo.child(f"{childSchoolId}/{payload.id}").get())
        
        if data is None:
            raise EntryNotExist(Article, payload.id)
        
        childSchool = self.childSchoolRepo.read(ChildSchoolRead(code=childSchoolId))
        return Article(
            title=data["title"],
            content=data["content"],
            attachments=data["attachments"],
            location=Location(data["location"]),
            uploadAt=str2date(data["uploadAt"]),
            childSchool=childSchool
        )
        
    
    def read(self, payload: ArticleRead) -> Article:
        if payload.childSchoolId is None:
            return self.readEventArticle(payload)
        else:
            return self.readChildSchoolArticle(payload)
    
    def updateEventArticle(self, payload: ArticleUpdate) -> Article:
        node: db.Reference = self.repo.child(f"events/{payload.id}")
        data: ArticleData | None = cast(ArticleData | None, node.get())
        
        if data is None:
            raise EntryNotExist(Article, payload.id)
        
        article = Article(
            title=data["title"],
            content=data["content"],
            attachments=data["attachments"],
            location=Location(data["location"]),
            uploadAt=str2date(data["uploadAt"]),
            childSchool=None
        )
        node.update(article.dict())
        return article
        

    def updateChildSchoolArticle(self, payload: ArticleUpdate) -> Article:
        childSchoolId: str = cast(str, payload.childSchoolId)
        node: db.Reference = self.repo.child(f"{childSchoolId}/{payload.id}")
        data: ArticleData | None = cast(ArticleData | None, node.get())
        
        if data is None:
            raise EntryNotExist(Article, payload.id)
        
        article = Article(
            title=data["title"],
            content=data["content"],
            attachments=data["attachments"],
            location=Location(data["location"]),
            uploadAt=str2date(data["uploadAt"]),
            childSchool=self.childSchoolRepo.read(ChildSchoolRead(code=childSchoolId))
        )
        
        node.update(article.dict())    # update firebase data.
        return article

    def update(self, payload: ArticleUpdate) -> Article:
        if payload.childSchoolId is None:
            return self.updateEventArticle(payload)
        else:
            return self.updateChildSchoolArticle(payload)
    
    def deleteEventArticle(self, payload: ArticleDelete) -> Article:
        node: db.Reference = self.repo.child(f"events/{payload.id}")
        data: ArticleData | None = cast(ArticleData | None, node.get())
        
        if data is None:
            raise EntryNotExist(Article, payload.id)
        
        article = Article(
            title=data["title"],
            content=data["content"],
            attachments=data["attachments"],
            location=Location(data["location"]),
            uploadAt=str2date(data["uploadAt"]),
            childSchool=None
        )
        node.delete()
        return article
    
    def deleteChildSchoolArticle(self, payload: ArticleDelete) -> Article:
        childSchoolId: str = cast(str, payload.childSchoolId)
        node: db.Reference = self.repo.child(f"{childSchoolId}/{payload.id}")
        data: ArticleData | None = cast(ArticleData | None, node.get())
        
        if data is None:
            raise EntryNotExist(Article, payload.id)
        
        article = Article(
            title=data["title"],
            content=data["content"],
            attachments=data["attachments"],
            location=Location(data["location"]),
            uploadAt=str2date(data["uploadAt"]),
            childSchool=self.childSchoolRepo.read(ChildSchoolRead(code=childSchoolId))
        )
        node.delete()
        return article
        
    
    def delete(self, payload: ArticleDelete) -> Article:
        if payload.childSchoolId is None:
            return self.deleteEventArticle(payload)
        else:
            return self.deleteChildSchoolArticle(payload)
        
class FirebaseController:
    """
    Middleware to abstract Firebase Database access.
    All operations we need to do with Firebase Database should be implemetned here.
    """
    root: Final[db.Reference]
    parentUser: Final[ParentUserRepository]
    childSchool: Final[ChildSchoolRepository]
    child: Final[ChildRepository]
    article: Final[ArticleRepository]
    childSchoolUser: Final[ChildSchoolUserRepository]
    
    def __init__(self) -> None:
        self.root = db.reference("/")
        self.parentUser = ParentUserRepository(self.root.child("users/parent"), self)
        self.childSchool = ChildSchoolRepository(self.root.child("childschool"), self)
        self.childSchoolUser = ChildSchoolUserRepository(self.root.child("users/childschool"), self)
        self.child = ChildRepository(self.root.child("children"), self)
        self.article = ArticleRepository(self.root.child("articles"), self)
    
    def debug(self):
        self.debug_user_feature()
        self.debug_childschool_feature()
    
    def debug_user_feature(self):
        self.parentUser.create(UserCreate(
            id="lapis0875",
            password="1234",
            name="김민준",
            tel="010-1234-5678",
            email="lapis0875@gmail.com",
            gender=Gender.Male,
            location=Location.GangBuk
        ))
        self.parentUser.read(UserRead(id="lapis0875"))
        self.parentUser.update(UserUpdate(id="lapis0875", password="5678"))
        self.parentUser.delete(UserDelete(id="lapis0875", password="5678"))
    
    def debug_childschool_feature(self):
        self.childSchool.create(ChildSchoolCreate(
            code="1ecec08c-f932-b044-e053-0a32095ab044",
            name="유성유치원",
            representerName="유성유치원",
            location=Location.YongSan,
            address="서울특별시 용산구 회나무로13가길 16",
            establishType=EstablishType.PRIVATE,
            establishAt="19650927",
            openingTime="08:40~18:00",
            tel="02-792-8691",
            children=[]
        ))
        self.childSchool.read(ChildSchoolRead(code="1ecec08c-f932-b044-e053-0a32095ab044"))
        self.childSchool.update(ChildSchoolUpdate(code="1ecec08c-f932-b044-e053-0a32095ab044", openingTime="09:00~20:00"))
        self.childSchool.delete(ChildSchoolDelete(code="1ecec08c-f932-b044-e053-0a32095ab044"))

DB: Final[FirebaseController] = FirebaseController()
