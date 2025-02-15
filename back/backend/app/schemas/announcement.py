from pydantic import BaseModel
from backend.app.schemas.base import SchemaBase


class AnnouncementBase(SchemaBase):
    """公告基础模型"""
    title: str
    content: str
    publisher: str
    type: str
    status: str = "active"


class CreateAnnouncement(AnnouncementBase):
    """创建公告请求体"""
    pass


class UpdateAnnouncement(AnnouncementBase):
    """更新公告请求体"""
    id: int


class AnnouncementInfo(AnnouncementBase):
    """公告信息响应体"""
    id: int
    uuid: str
    publish_date: str
    update_date: str

    class Config:
        from_attributes = True
