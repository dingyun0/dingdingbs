from typing import List, Optional
from pydantic import BaseModel
from backend.app.schemas.base import SchemaBase

class ComprehensiveTestBase(SchemaBase):
    sno: str
    name: str
    class_name: str
    操作系统课程设计成绩: Optional[str] = None
    无线网络技术成绩: Optional[str] = None
    计算机网络课程设计: Optional[str] = None
    操作系统: Optional[str] = None
    人工智能与网络技术学科前沿: Optional[str] = None
    信息安全原理及应用: Optional[str] = None
    Linux操作系统: Optional[str] = None
    Java程序设计: Optional[str] = None
    credit_gpa: float
    year_gpa: float
    comprehensive_score: float

class SaveComprehensiveTest(BaseModel):
    tests: List[ComprehensiveTestBase]