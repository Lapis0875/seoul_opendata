from typing import Final
from fastapi import APIRouter
from seoul_opendata.firebase.controller import DB

from seoul_opendata.models.payloads import ChildCreate, ChildDelete, ChildRead, ChildUpdate

__all__ = ("child_router",)

child_router: Final[APIRouter] = APIRouter(prefix="/children")

@child_router.post("/")
def register_child(body: ChildCreate):
    """
    아이 정보를 등록합니다.

    Args:
        body (ChildData): 아이 데이터

    Returns:
        Child | Message: 생성된 아이 모델로 응답합니다. 만약 데이터가 잘못됬으면, 오류 메세지로 응답합니다.
    """
    return DB.child.create(body)

@child_router.post("/")
def get_child(body: ChildRead):
    """
    아이 정보를 반환합니다.

    Args:
        body (ChildRead): 반환할 아이 데이터

    Returns:
        Child | Message: 아이 모델로 응답합니다. 데이터가 잘못될 경우, 오류 메세지로 응답합니다.
    """
    return DB.child.read(body)

@child_router.put("/")
def update_child(body: ChildUpdate):
    """
    아이 정보를 수정합니다.

    Args:
        body (ChildRead): 수정할 아이 데이터

    Returns:
        Child | Message: 수정된 아이 모델로 응답합니다. 데이터가 잘못될 경우, 오류 메세지로 응답합니다.
    """
    return DB.child.update(body)

@child_router.delete("/")
def delete_child(body: ChildDelete):
    """
    아이 정보를 삭제합니다.

    Args:
        body (ChildRead): 삭제할 아이 데이터

    Returns:
        Child | Message: 삭제된 아이 모델로 응답합니다. 데이터가 잘못될 경우, 오류 메세지로 응답합니다.
    """
    return DB.child.delete(body)