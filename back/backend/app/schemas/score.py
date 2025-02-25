from typing import List
from pydantic import BaseModel, Field
from backend.app.schemas.base import SchemaBase

class ScoreBase(SchemaBase):
    name: str
    sno: str  
    class_name: str
    操作系统课程设计成绩: str | None = None
    无线网络技术成绩: str | None = None
    计算机网络课程设计: str | None = None
    操作系统: str | None = None
    人工智能与网络技术学科前沿: str | None = None
    信息安全原理及应用: str | None = None
    Linux操作系统: str | None = None
    Java程序设计: str | None = None

class SaveScore(SchemaBase):
    scores: List[ScoreBase]