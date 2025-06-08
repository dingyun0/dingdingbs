from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CollegeBase(BaseModel):
    department: str
    major: str
    grade: str
    department_code: Optional[str] = None
    major_code: Optional[str] = None
    grade_code: Optional[str] = None

class CollegeCreate(CollegeBase):
    pass

class CollegeUpdate(CollegeBase):
    id: int

class CollegeInDB(CollegeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True