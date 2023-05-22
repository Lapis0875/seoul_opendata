from typing import Callable
from fastapi import FastAPI, routing


def register_routes(app: FastAPI):
    pass

RouteRegister = Callable[[FastAPI], None]       # type(register_routes)
