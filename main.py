from fastapi import FastAPI
from seoul_opendata.models import Child, ChildSchool, ParentUser
from setup import set_keys
from seoul_opendata.firebase.controller import DB
from seoul_opendata.seoul_openapi import SeoulOpenData
from seoul_opendata.models.payloads import ChildData, ChildRead, ChildSchoolCreate, ChildSchoolUpdate, ModelOrMessage, UserCreate, UserLogin, UserRead, UserUpdate, Message

set_keys()
app = FastAPI()
seoulOpenAPI = SeoulOpenData()

seoulOpenAPI.prefetch()
seoulOpenAPI.create()

# Sample Endpoints

@app.get("/")
def index():
    """
    index 요청입니다. 그냥 서버 상태 확인이에요.
    
    Returns:
        Message: 서버 상태에 대한 정보를 응답으로 보냅니다.
    """
    return {"message": "Server Online!", "api_version": "20230530", "code": "OK"}

@app.get("/echo/{text}")
def echo(text: str):
    """
    echo 요청입니다. URL 파라미터로 받은 문자열을 그대로 보내줍니다. 서버 상태 확인을 위해 존재합니다.

    Args:
        text (str): 아무 문자열입니다.

    Returns:
        Message: 경로에 받은 문자열을 그대로 포함한 응답을 보내줍니다.
    """
    return {"message": text, "code": "OK"}

# ChildSchool Endpoints

@app.get("/childschool/all")
def get_all_childschools():
    """
    모든 유치원 정보를 가져옵니다.

    Returns:
        dict[str, ChildSchool]: 유치원 고유 코드와 유치원 모델 데이터로 구성된 맵을 응답으로 보냅니다.
    """
    return DB.childSchool.read_all()

@app.get("/childschool/{code}")
def get_childschool(code: str):
    """
    특정 코드의 유치원 정보를 가져옵니다.

    Args:
        code (str): 가져올 유치원의 코드입니다.

    Returns:
        ChildSchool | Message: 유치원 모델의 데이터로 응답합니다. 만약 코드에 해당하는 유치원이 없으면, 오류를 안내하는 응답을 전달합니다.
    """
    childSchool = DB.childSchool.read({"code": code})
    return childSchool or {"message": "유치원 정보를 찾을 수 없습니다.", "code": "INVALID_SCHOOL_CODE"}

@app.post("/childschool")
def create_childschool(body: ChildSchoolCreate):
    """
    새 유치원 모델을 생성합니다.

    Args:
        body (ChildSchoolCreate): 유치원 모델의 정보입니다.

    Returns:
        ChildSchool: 생성된 유치원 모델의 데이터입니다.
    """
    childSchool = DB.childSchool.create(body)
    return childSchool.dict() or {}

@app.post("/childschool/{code}")
def update_childschool(code: str, body: ChildSchoolUpdate):
    """
    유치원 정보를 수정합니다.
    Args:
        code (str): 수정할 유치원 코드
        body (ChildSchoolUpdate): 수정할 유치원의 정보

    Returns:
        ChildSchool | Message: 수정된 유치원 모델의 데이터로 응답합니다. 만약 코드에 해당하는 유치원이 없으면, 오류를 안내하는 응답을 전달합니다. 
    """
    childSchool = DB.childSchool.read({"code": code})   # check if exist
    
    if childSchool is None:
        return {"message": "유치원 정보를 찾을 수 없습니다.", "code": "INVALID_SCHOOL_CODE"}
        
    return DB.childSchool.update(body)

# User Endpoints

@app.post("/users/signup")
def user_signup(body: UserCreate) -> ParentUser:
    """
    회원가입 엔드포인트입니다. 새 유저 데이터를 생성합니다.

    Args:
        body (UserCreate): 유저 생성 데이터

    Returns:
        ParentUser: 생성된 유저 모델의 데이터입니다.
    """
    user = DB.parentUser.create(body)
    return user

@app.post("/users/login")
def user_login(body: UserLogin):
    """
    로그인 엔드포인트입니다. 기존 유저 계정으로 로그인합니다.

    Args:
        body (UserLogin): 로그인 데이터

    Returns:
        ParentUser: 로그인에 성공한 경우, 유저 모델의 데이터를 응답으로 보냅니다.
    """
    user = DB.parentUser.read({"id": body["id"]})
    if user.password == body["password"]:
        return user      # login success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

@app.post("/users/update")
def user_update(body: UserUpdate):
    """
    기존 유저 정보를 수정합니다.

    Args:
        body (UserUpdate): 수정할 유저 정보 데이터

    Returns:
        ParentUser | Message: 수정된 유저 모델로 응답합니다. 수정 실패하면, 오류를 안내하는 메세지로 응답합니다.
    """
    query: UserRead = {"id": body["id"]}
    if "email" in body:
        query["email"] = body["email"]
        
    user = DB.parentUser.read(query)
    if "password" in body and user.password == body["password"]:
        return DB.parentUser.update(body)      # login success & update success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

# Child Endpoints

@app.post("/children/register")
def child_register(body: ChildData):
    """
    아이 정보를 등록합니다.

    Args:
        body (ChildData): 아이 데이터

    Returns:
        Child | Message: 생성된 아이 모델로 응답합니다. 만약 데이터가 잘못됬으면, 오류 메세지로 응답합니다.
    """
    child = DB.child.create(body)
    if child is None:
        return {"message": "fail to create child", "code": "INVALID_CHILD_DATA"}
    return child

@app.post("/children/update")
def child_update(body: ChildRead):
    """
    아이 정보를 수정합니다.

    Args:
        body (ChildRead): 수정할 아이 데이터

    Returns:
        Child | Message: 수정된 아이 모델로 응답합니다. 데이터가 잘못될 경우, 오류 메세지로 응답합니다.
    """
    child = DB.child.update(body)
    if child is None:
        return {"message": "fail to update child", "code": "INVALID_CHILD_DATA"}
    return child
