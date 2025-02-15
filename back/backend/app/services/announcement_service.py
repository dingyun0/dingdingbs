from backend.app.dao.announcement_dao import AnnouncementDao
from backend.app.schemas.announcement import CreateAnnouncement, UpdateAnnouncement
from backend.app.common.exception import errors

class AnnouncementService:
    @staticmethod
    async def add_announcement(announcement: CreateAnnouncement):
        try:
            result = await AnnouncementDao.create(announcement)
            return result
        except Exception as e:
            raise errors.CustomError(msg=f"添加公告失败: {str(e)}")

    @staticmethod
    async def update_announcement(announcement: UpdateAnnouncement):
        try:
            result = await AnnouncementDao.update(announcement.id, announcement)
            return result
        except Exception as e:
            raise errors.CustomError(msg=f"更新公告失败: {str(e)}")

    @staticmethod
    async def delete_announcement(id: int):
        try:
            result = await AnnouncementDao.delete(id)
            return result
        except Exception as e:
            raise errors.CustomError(msg=f"删除公告失败: {str(e)}")

    @staticmethod
    async def get_announcement_list(page: int = 1, page_size: int = 10):
        """获取公告列表"""
        try:
            # 计算偏移量
            offset = (page - 1) * page_size
            
            # 获取总数
            total = await AnnouncementDao.get_count()
            
            # 获取分页数据
            announcements = await AnnouncementDao.get_page(offset, page_size)
            
            # 转换为列表格式
            result = []
            for announcement in announcements:
                result.append({
                    'id': announcement.id,
                    'title': announcement.title,
                    'content': announcement.content,
                    'publisher': announcement.publisher,
                    'type': announcement.type,
                    'status': announcement.status,
                    'publish_date': announcement.publish_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'update_date': announcement.update_date.strftime('%Y-%m-%d %H:%M:%S')
                })
            return {
                'list': result,
                'total': total
            }
        except Exception as e:
            raise errors.CustomError(msg=f"获取公告列表失败: {str(e)}")