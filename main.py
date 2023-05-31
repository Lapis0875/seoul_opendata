from pydantic import ValidationError
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from seoul_opendata.routes import user_router, child_school_router, child_router
from seoul_opendata.firebase.controller import DBException
from seoul_opendata.seoul_openapi import SeoulOpenData

app = FastAPI()
seoulOpenAPI = SeoulOpenData()

seoulOpenAPI.prefetch()
seoulOpenAPI.create()

# Sample Endpoints

@app.exception_handler(DBException)
async def handle_db_exception(request: Request, exc: DBException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(exc.message)
    )

@app.exception_handler(ValidationError)
async def handle_type_exception(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            "message": "Type Validation Failed.",
            "code": "TYPE_VALIDATION_FAILED",
            "details": exc.errors()
        })
    )


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

app.include_router(user_router)
app.include_router(child_school_router)
app.include_router(child_router)
