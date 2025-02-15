from typing import List
from tortoise.transactions import atomic

from backend.app.dao.base import DaoBase
from backend.app.models.announcement import Announcement
from backend.app.schemas.announcement import CreateAnnouncement, UpdateAnnouncement


class AnnouncementDao(DaoBase):
    """公告数据访问对象"""

    @atomic()
    async def create(self, announcement: CreateAnnouncement) -> Announcement:
        """创建公告"""
        return await self.model.create(**announcement.model_dump())

    @atomic()
    async def update(self, id: int, announcement: UpdateAnnouncement) -> int:
        """更新公告"""
        # 先检查公告是否存在
        exists = await self.model.filter(id=id).exists()
        if not exists:
            return 0
            
        # 执行更新
        count = await self.model.filter(id=id).update(**announcement.model_dump(exclude={'id'}))
        return count

    @atomic()
    async def delete(self, id: int) -> int:
        """删除公告"""
        count = await self.model.filter(id=id).delete()
        return count

    async def get_all(self) -> List[Announcement]:
        """获取所有公告"""
        return await self.model.all().order_by('-publish_date')

    async def get_by_id(self, id: int) -> Announcement:
        """根据ID获取公告"""
        return await self.model.get_or_none(id=id)

    async def get_by_type(self, type: str) -> List[Announcement]:
        """根据类型获取公告"""
        return await self.model.filter(type=type).order_by('-publish_date')

    async def get_count(self) -> int:
        """获取总数"""
        return await self.model.all().count()

    async def get_page(self, offset: int, limit: int):
        """获取分页数据"""
        return await self.model.all().offset(offset).limit(limit)


# 创建全局实例
AnnouncementDao = AnnouncementDao(Announcement)