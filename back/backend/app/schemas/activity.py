from datetime import datetime
from pydantic import BaseModel, Field
from backend.app.schemas.base import SchemaBase

class ActivityBase(SchemaBase):
    title: str = Field(..., max_length=255, description="活动标题")
    content: str = Field(..., description="活动内容")
    publisher: str = Field(..., max_length=255, description="发布者")
    category: str = Field(..., description="活动类型（学业/文体/劳动/创新）")
    credits: int = Field(..., ge=0, description="加分数")
    deadline: datetime = Field(..., description="截止时间")
    quota: int = Field(..., ge=0, description="名额数量")
    status: str = Field(default="active", description="活动状态")

class CreateActivity(ActivityBase):
    pass

class UpdateActivity(ActivityBase):
    id: int

class ActivityInfo(ActivityBase):
    id: int
    uuid: str
    publish_date: datetime
    update_date: datetime

    class Config:
        from_attributes = True

class ActivityApply(BaseModel):
    """活动申请模型"""
    activity_id: int = Field(..., description="活动ID")
    activity_title: str = Field(..., description="活动名称")
    teacher_id: int = Field(..., description="审核老师ID")
    student_sno: str = Field(..., description="申请学生学号")

    class Config:
        from_attributes = True

class ReviewRequest(BaseModel):
    review_id: int
    review_comment: str
    comment: str
