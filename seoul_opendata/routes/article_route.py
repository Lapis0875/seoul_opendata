from typing import Final
from fastapi import APIRouter
from seoul_opendata.firebase.controller import DB

__all__ = ("article_router",)

article_router: Final[APIRouter] = APIRouter(prefix="/articles")