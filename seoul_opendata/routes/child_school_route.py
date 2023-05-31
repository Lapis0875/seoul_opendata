from typing import Final
from fastapi import APIRouter

from seoul_opendata.firebase.controller import DB
from seoul_opendata.models.payloads import ChildSchoolCreate, ChildSchoolRead, ChildSchoolUpdate

__all__ = ("child_school_router",)

child_school_router: Final[APIRouter] = APIRouter(prefix="/childschools")

@child_school_router.get("/all")
def get_all_childschools():
    """
    모든 유치원 정보를 가져옵니다.

    Returns:
        dict[str, ChildSchool]: 유치원 고유 코드와 유치원 모델 데이터로 구성된 맵을 응답으로 보냅니다.
    """
    return DB.childSchool.readAll()

@child_school_router.get("/{code}")
def get_childschool(code: str):
    """
    특정 코드의 유치원 정보를 가져옵니다.

    Args:
        code (str): 가져올 유치원의 코드입니다.

    Returns:
        ChildSchool | Message: 유치원 모델의 데이터로 응답합니다. 만약 코드에 해당하는 유치원이 없으면, 오류를 안내하는 응답을 전달합니다.
    """
    return DB.childSchool.read(ChildSchoolRead(code=code))

@child_school_router.post("/")
def create_childschool(body: ChildSchoolCreate):
    """
    새 유치원 모델을 생성합니다.

    Args:
        body (ChildSchoolCreate): 유치원 모델의 정보입니다.

    Returns:
        ChildSchool: 생성된 유치원 모델의 데이터입니다.
    """
    return DB.childSchool.create(body)

@child_school_router.put("/")
def update_childschool(body: ChildSchoolUpdate):
    """
    유치원 정보를 수정합니다.
    Args:
        code (str): 수정할 유치원 코드
        body (ChildSchoolUpdate): 수정할 유치원의 정보

    Returns:
        ChildSchool | Message: 수정된 유치원 모델의 데이터로 응답합니다. 만약 코드에 해당하는 유치원이 없으면, 오류를 안내하는 응답을 전달합니다. 
    """
        
    return DB.childSchool.update(body)