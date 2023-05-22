from fastapi import FastAPI
from seoul_opendata.firebase.controller import FirebaseController

from seoul_opendata.models.playloads import UserCreate, UserLogin, UserUpdate

app = FastAPI()
db = FirebaseController()

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/echo/{text}")
async def echo(text: str):
    return {"message": text}

@app.get("/facilities/{facility_id}")
async def get_facility(facility_id: int):
    return {"facility_id": facility_id}

@app.post("/users/signup")
async def user_signup(body: UserCreate):
    user = db.parentUser.create(body)
    return user.dict()

@app.post("/users/login")
async def user_login(body: UserLogin):
    user = db.parentUser.read({"id": body["id"], "email": None, "phone": None})
    if user.password == body["password"]:
        return user.dict()      # login success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}

@app.post("/users/update")
async def user_update(body: UserUpdate):
    user = db.parentUser.read({"id": body["id"], "email": body["email"], "phone": None})
    if user.password == body["password"]:
        return db.parentUser.update(body).dict()      # login success & update success
    else:
        return {"message": "login failed", "code": "INVALID_PASSWORD"}
