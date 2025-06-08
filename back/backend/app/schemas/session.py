from typing import List, Optional
from pydantic import BaseModel, Field
from backend.app.schemas.base import SchemaBase

class SessionBase(SchemaBase):
    course_id: str
    course_name: str
    credit: str
    hours: str
    nature: str
    college: str
    major: str
    grade: str

class SessionList(BaseModel):
    sessions: List[SessionBase]

class FilteredCoursesRequest(BaseModel):
    department: str
    major: str
    grade: str

class CourseItem(BaseModel):
    course_id: str
    course_name: str

class FilteredCoursesResponse(BaseModel):
    code: int = 200
    message: str = "Success"
    data: List[CourseItem] 