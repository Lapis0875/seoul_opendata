from typing import Final
from fastapi import APIRouter
from seoul_opendata.firebase.controller import DB

from seoul_opendata.models.payloads import ChildSchoolUserCreate, ChildSchoolUserDelete, ChildSchoolUserRead, ChildSchoolUserUpdate, UserCreate, UserDelete, UserLogin, UserRead, UserUpdate
from seoul_opendata.models import ParentUser, ChildSchoolUser

__all__ = ("user_router",)

user_router: Final[APIRouter] = APIRouter(prefix="/users")


@user_router.post("/signup")
def user_signup(body: UserCreate) -> ParentUser:
    """
    회원가입 엔드포인트입니다. 새 부모 유저 데이터를 생성합니다.

    Args:
        body (UserCreate): 부모 유저 생성 데이터

    Returns:
        ParentUser: 생성된 부모 유저 모델의 데이터입니다.
    """
    return DB.parentUser.create(body)

@user_router.post("/login")
def user_login(body: UserLogin):
    """
    로그인 엔드포인트입니다. 기존 부모 유저 계정으로 로그인합니다.

    Args:
        body (UserLogin): 로그인 데이터

    Returns:
        ParentUser: 로그인에 성공한 경우, 부모 유저 모델의 데이터를 응답으로 보냅니다.
    """
    user = DB.parentUser.read(UserRead(id=body.id))
    if user.password == body.password:
        return user      # login success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

@user_router.put("/")
def user_update(body: UserUpdate):
    """
    기존 부모 유저 정보를 수정합니다.

    Args:
        body (UserUpdate): 수정할 부모 유저 정보 데이터

    Returns:
        ParentUser | Message: 수정된 부모 유저 모델로 응답합니다. 수정 실패하면, 오류를 안내하는 메세지로 응답합니다.
    """
    query: UserRead = UserRead(id=body.id)
        
    user = DB.parentUser.read(query)
    if user.password == body.password:
        return DB.parentUser.update(body)      # login success & update success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

@user_router.delete("/")
def user_delete(body: UserDelete):
    """
    기존 부모 유저 정보를 삭제합니다. 회원 탈퇴 엔드포인트로 사용합니다.

    Args:
        body (UserDelete): 삭제할 부모 유저의 인증 정보 데이터

    Returns:
        ParentUser | Message: 삭제된 부모 유저 모델로 응답합니다. 삭제에 실패하면, 오류를 안내하는 메세지로 응답합니다.
    """
    query: UserRead = UserRead(id=body.id)
        
    user = DB.parentUser.read(query)
    if user.password == body.password:
        return DB.parentUser.delete(body)      # login success & update success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

# Child School User Endpoints

@user_router.post("/childschool/signup")
def childschool_user_signup(body: ChildSchoolUserCreate) -> ChildSchoolUser:
    """
    유치원/어린이집 기관 계정의 회원가입 엔드포인트입니다. 새 기관 유저 데이터를 생성합니다.

    Args:
        body (ChildSchoolUserCreate): 기관 유저 생성 데이터

    Returns:
        ChildSchoolUser: 생성된 기관 유저 모델의 데이터입니다.
    """
    return DB.childSchoolUser.create(body)

@user_router.post("/childschool/login")
def childschool_user_login(body: UserLogin):
    """
    유치원/어린이집 기관 계정의 로그인 엔드포인트입니다. 기존 기관 유저 데이터를 생성합니다.

    Args:
        body (ChildSchoolUserCreate): 유저 생성 데이터

    Returns:
        ChildSchoolUser: 로그인된 기관 유저 모델의 데이터입니다.
    """
    user = DB.childSchoolUser.read(ChildSchoolUserRead(id=body.id))
    if user.password == body.password:
        return user      # login success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

@user_router.put("/childschool")
def childschool_user_update(body: ChildSchoolUserUpdate):
    """
    기존 기관 유저 정보를 수정합니다.

    Args:
        body (ChildSchoolUserUpdate): 수정할 기관 유저 정보 데이터

    Returns:
        ChildSchoolUser | Message: 수정된 기관 유저 모델로 응답합니다. 수정 실패하면, 오류를 안내하는 메세지로 응답합니다.
    """
    query = ChildSchoolUserRead(id=body.id)
        
    user = DB.childSchoolUser.read(query)
    if user.password == body.password:
        return DB.childSchoolUser.update(body)      # login success & update success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

@user_router.delete("/childschool/")
def childschool_user_delete(body: ChildSchoolUserDelete):
    """
    기존 기관 유저 정보를 삭제합니다. 회원 탈퇴 엔드포인트로 사용합니다.

    Args:
        body (UserDelete): 삭제할 기관 유저의 인증 정보 데이터

    Returns:
        ChildSchoolUser | Message: 삭제된 기관 유저 모델로 응답합니다. 삭제에 실패하면, 오류를 안내하는 메세지로 응답합니다.
    """
    query = ChildSchoolUserRead(id=body.id)
        
    user = DB.childSchoolUser.read(query)
    if user.password == body.password:
        return DB.childSchoolUser.delete(body)      # login success & update success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

