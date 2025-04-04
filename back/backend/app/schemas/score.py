from typing import List, Dict, Any
from pydantic import BaseModel, Field, create_model
from backend.app.schemas.base import SchemaBase

class ScoreBase(SchemaBase):
    name: str
    sno: str  
    department: str
    major: str
    grade: str
    
    @classmethod
    def create_dynamic_model(cls, course_fields: List[str]):
        """
        动态创建包含指定课程字段的模型
        
        Args:
            course_fields: 课程字段列表
            
        Returns:
            动态创建的模型类
        """
        field_definitions = {
            "name": (str, ...),
            "sno": (str, ...),
            "department": (str, ...),
            "major": (str, ...),
            "grade": (str, ...),
        }
        
        # 添加动态课程字段
        for field in course_fields:
            field_definitions[field] = (str | None, None)
            
        return create_model(
            "DynamicScoreBase",
            **field_definitions,
            __base__=SchemaBase
        )

class SaveScore(SchemaBase):
    scores: List[Dict[str, Any]]  # 改为接收任意字典列表
    course_fields: List[str]  # 添加课程字段列表
    
    def get_validated_scores(self):
        """
        验证并返回符合动态模型的成绩列表
        """
        DynamicModel = ScoreBase.create_dynamic_model(self.course_fields)
        return [DynamicModel(**score) for score in self.scores]

class InputtedCollege(SchemaBase):
    """已录入成绩的学院信息"""
    department: str
    major: str
    grade: str
    