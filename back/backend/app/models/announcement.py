from tortoise import fields
from tortoise.models import Model
from backend.app.utils.generate_string import get_uuid4_str


class Announcement(Model):
    id = fields.BigIntField(pk=True, index=True, description='主键id')
    uuid = fields.CharField(max_length=36, default=get_uuid4_str, unique=True, description='公告UID')
    title = fields.CharField(max_length=255, description='公告标题')
    content = fields.TextField(description='公告内容')
    publish_date = fields.DatetimeField(auto_now_add=True, description='发布时间')
    update_date = fields.DatetimeField(auto_now=True, description='更新时间')
    publisher = fields.CharField(max_length=255, description='发布者')
    type = fields.CharField(max_length=50, description='公告类型')  # 如：学校公告、奖学金公告等
    status = fields.CharField(max_length=50, default='active', description='公告状态')  # active/inactive

    class Meta:
        table = "announcements"
        table_description = "公告表"
        indexes = [("title", "type")]

    def __str__(self):
        return self.title
