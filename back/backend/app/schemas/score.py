from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, create_model
from backend.app.schemas.base import SchemaBase
from datetime import datetime

class ScoreBase(SchemaBase):
    name: str
    sno: str  
    department: str
    major: str
    grade: str
    # 用于存储动态课程成绩
    
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

class ScoreReview(SchemaBase):
    """成绩疑问申请"""
    student_sno: str = Field(..., description="学生学号")
    student_name: str = Field(..., description="学生姓名")
    teacher_id: int = Field(..., description="审核老师ID")
    question_type: str = Field(..., description="疑问类型")
    content: str = Field(..., description="疑问说明")
    status: str = Field(default="pending", description="审核状态")
    apply_time: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="申请时间")
    review_time: str | None = Field(default=None, description="审核时间")
    review_comment: str | None = Field(default=None, description="审核意见")
    
class ScoreReviewResult(BaseModel):
    """成绩疑问审核结果"""
    review_id: int = Field(..., description="成绩疑问ID")
    status: str = Field(..., description="审核状态：approved-通过，rejected-驳回")
    comment: str = Field(..., description="审核意见")

class ScoreCreate(SchemaBase):
    sno: str
    name: str
    department: str
    major: str
    grade: str
    scores: Dict[str, str]

class ScoreUpdate(SchemaBase):
    sno: str
    name: str
    department: str
    major: str
    grade: str
    scores: Dict[str, str]
    
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
