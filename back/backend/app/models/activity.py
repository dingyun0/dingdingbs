from tortoise import fields
from tortoise.models import Model
from backend.app.utils.generate_string import get_uuid4_str

class Activity(Model):
    id = fields.BigIntField(pk=True, index=True, description='主键id')
    uuid = fields.CharField(max_length=36, default=get_uuid4_str, unique=True, description='活动UID')
    title = fields.CharField(max_length=255, description='活动标题')
    content = fields.TextField(description='活动内容')
    publish_date = fields.DatetimeField(auto_now_add=True, description='发布时间')
    update_date = fields.DatetimeField(auto_now=True, description='更新时间')
    publisher = fields.CharField(max_length=255, description='发布者')
    category = fields.CharField(max_length=50, description='活动类型')  # 学业/文体/劳动/创新
    credits = fields.IntField(description='加分数', default=0)
    deadline = fields.DatetimeField(description='截止时间')
    quota = fields.IntField(description='名额数量')
    status = fields.CharField(max_length=50, default='active', description='活动状态')  # active/inactive

    class Meta:
        table = "activities"
        table_description = "活动表"
        indexes = [("title", "category")]

    def __str__(self):
        return self.title