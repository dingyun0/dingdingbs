from typing import List
from pydantic import BaseModel
from backend.app.schemas.base import SchemaBase

class SessionBase(SchemaBase):
    course_id: str
    course_name: str
    credit: str
    hours: str
    nature: str
    department: str

class SaveSession(BaseModel):
    sessions: List[SessionBase] 