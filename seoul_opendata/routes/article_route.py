from typing import Final
from fastapi import APIRouter
from seoul_opendata.firebase.controller import DB
from seoul_opendata.models.payloads import ArticleCreate, ArticleDelete, ArticleRead, ArticleUpdate

__all__ = ("article_router",)

article_router: Final[APIRouter] = APIRouter(prefix="/articles")

@article_router.get("/")
def get_all_articles():
    """
    모든 Article을 반환합니다.

    Returns:
        dict[str, dict[str, Article]]: 
    """
    return DB.article.readAll()

@article_router.get("/events")
def get_all_event_articles():
    """
    모든 행사 관련 Article을 반환합니다.

    Returns:
        dict[str, Article]: 
    """
    return DB.article.readAllEventArticles()

@article_router.get("/{child_school_id}")
def get_all_child_school_articles(child_school_id: str):
    """
    특정 기관의 모든 Article을 반환합니다.

    Returns:
        dict[str, Article]: 
    """
    return DB.article.readAllChildSchoolArticles(child_school_id)

@article_router.post("/events")
def create_event_article(body: ArticleCreate):
    """
    단일 Article을 생성합니다. 특정 기관에 소속되지 않은, 이벤트 게시글을 반환합니다.

    Args:
        article_id (str): 게시글 id

    Returns:
        Article: 게시글 모델
    """
    return DB.article.createChildSchoolArticle(body)

@article_router.get("/events/{article_id}")
def get_event_article(article_id: str):
    """
    단일 Article을 반환합니다. 특정 기관에 소속되지 않은, 이벤트 게시글을 반환합니다.

    Args:
        article_id (str): 게시글 id

    Returns:
        Article: 게시글 모델
    """
    return DB.article.readChildSchoolArticle(ArticleRead(id=article_id, childSchoolId=None))

@article_router.put("/events/{article_id}")
def update_event_article(article_id: str, body: ArticleUpdate):
    """
    단일 Article을 수정합니다. 특정 기관에 소속되지 않은, 이벤트 게시글을 수정합니다.

    Args:
        article_id (str): 게시글 id

    Returns:
        Article: 게시글 모델
    """
    if (article_id != body.id):
        return {"message": "article_id is not matched.", "code": "INVALID_REQUEST"}
    return DB.article.updateEventArticle(body)

@article_router.delete("/events/{article_id}")
def delete_event_article(article_id: str, body: ArticleDelete):
    """
    단일 Article을 수정합니다. 특정 기관에 소속되지 않은, 이벤트 게시글을 수정합니다.

    Args:
        article_id (str): 게시글 id

    Returns:
        Article: 게시글 모델
    """
    if (article_id != body.id):
        return {"message": "article_id is not matched.", "code": "INVALID_REQUEST"}
    return DB.article.deleteEventArticle(body)

@article_router.get("/{child_school_id}")
def create_childschool_article(child_school_id: str, body: ArticleCreate):
    """
    단일 Article을 생성합니다. 특정 기관에 소속된 게시글을 반환합니다.

    Args:
        child_school_id (str): 이 게시글이 속한 유치원/어린이집 기관의 id
        article_id (str): 게시글 id

    Returns:
        Article: 게시글 모델
    """
    return DB.article.createChildSchoolArticle(body)

@article_router.get("/{child_school_id}/{article_id}")
def get_childschool_article(child_school_id: str, article_id: str):
    """
    단일 Article을 반환합니다. 특정 기관에 소속된 게시글을 반환합니다.

    Args:
        child_school_id (str): 이 게시글이 속한 유치원/어린이집 기관의 id
        article_id (str): 게시글 id

    Returns:
        Article: 게시글 모델
    """
    return DB.article.readChildSchoolArticle(ArticleRead(id=article_id, childSchoolId=child_school_id))

@article_router.put("/{child_school_id}/{article_id}")
def update_childschool_article(child_school_id: str, article_id: str, body: ArticleUpdate):
    """
    단일 Article을 수정합니다. 특정 기관에 소속된 게시글을 반환합니다.

    Args:
        child_school_id (str): 이 게시글이 속한 유치원/어린이집 기관의 id
        article_id (str): 게시글 id

    Returns:
        Article: 게시글 모델
    """
    if (article_id != body.id or child_school_id != body.childSchoolId):
        return {"message": "article_id or child_school_id is not matched.", "code": "INVALID_REQUEST"}
    return DB.article.updateChildSchoolArticle(body)

@article_router.delete("/{child_school_id}/{article_id}")
def delete_childschool_article(child_school_id: str, article_id: str, body: ArticleDelete):
    """
    단일 Article을 수정합니다. 특정 기관에 소속된 게시글을 반환합니다.

    Args:
        child_school_id (str): 이 게시글이 속한 유치원/어린이집 기관의 id
        article_id (str): 게시글 id

    Returns:
        Article: 게시글 모델
    """
    if (article_id != body.id or child_school_id != body.childSchoolId):
        return {"message": "article_id or child_school_id is not matched.", "code": "INVALID_REQUEST"}
    return DB.article.deleteChildSchoolArticle(body)