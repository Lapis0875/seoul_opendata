from fastapi import FastAPI
from setup import set_keys
from seoul_opendata.firebase.controller import DB
from seoul_opendata.seoul_openapi import SeoulOpenData
from seoul_opendata.models.playloads import ChildSchoolCreate, ChildSchoolUpdate, UserCreate, UserLogin, UserRead, UserUpdate

set_keys()
app = FastAPI()
seoulOpenAPI = SeoulOpenData()

seoulOpenAPI.prefetch()
seoulOpenAPI.create()

@app.get("/")
def index():
    return {"message": "Hello World", "api-version": "20230528"}

@app.get("/echo/{text}")
def echo(text: str):
    return {"message": text}

@app.get("/childschool/all")
def get_all_childschools():
    return DB.childSchool.read_all()

@app.get("/childschool/{code}")
def get_childschool(code: str):
    childSchool = DB.childSchool.read({"code": code})
    return childSchool.dict() or {}

@app.post("/childschool")
def create_childschool(body: ChildSchoolCreate):
    childSchool = DB.childSchool.create(body)
    return childSchool.dict() or {}

@app.post("/childschool/{code}")
def update_childschool(code: str, body: ChildSchoolUpdate):
    childSchool = DB.childSchool.read({"code": code})   # check if exist
        
    return DB.childSchool.update(body).dict()      # login success & update success

@app.post("/users/signup")
def user_signup(body: UserCreate):
    user = DB.parentUser.create(body)
    return user.dict()

@app.post("/users/login")
def user_login(body: UserLogin):
    user = DB.parentUser.read({"id": body["id"]})
    if user.password == body["password"]:
        return user.dict()      # login success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

@app.post("/users/update")
def user_update(body: UserUpdate):
    query: UserRead = {"id": body["id"]}
    if "email" in body:
        query["email"] = body["email"]
        
    user = DB.parentUser.read(query)
    if "password" in body and user.password == body["password"]:
        return DB.parentUser.update(body).dict()      # login success & update success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}
