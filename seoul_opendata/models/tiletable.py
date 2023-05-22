from datetime import time
from pydantic import BaseModel


class Schedule(BaseModel):
    """시간표 상의 한개 과목 모델."""
    name: str
    start: time
    end: time

class Timetable(BaseModel):
    """시간표 모델."""
    table: list[list[Schedule]]
    