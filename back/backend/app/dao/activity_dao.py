from tortoise.transactions import in_transaction
from backend.app.models.activity_review import ActivityReview
from backend.app.models.activity import Activity
from backend.app.schemas.activity import ActivityApply, ActivityInfo

class ActivityDAO:
    @staticmethod
    async def create(activity_info: ActivityInfo):
        """创建活动"""
        async with in_transaction():
            return await Activity.create(**activity_info.model_dump())

    @staticmethod
    async def get_by_id(activity_id: int):
        """根据ID获取活动"""
        return await Activity.get_or_none(id=activity_id)

    @staticmethod
    async def update(activity_info: ActivityInfo):
        """更新活动"""
        async with in_transaction():
            activity_dict = activity_info.model_dump()
            activity_id = activity_dict.pop("id")
            await Activity.filter(id=activity_id).update(**activity_dict)
            return await Activity.get(id=activity_id)

    @staticmethod
    async def delete(activity_id: int):
        """删除活动"""
        async with in_transaction():
            return await Activity.filter(id=activity_id).delete()

    @staticmethod
    async def get_all():
        """获取所有活动"""
        return await Activity.all().order_by("-publish_date")

    @staticmethod
    async def get_total():
        """获取活动总数"""
        return await Activity.all().count()

    @staticmethod
    async def get_student_apply(activity_id: int, student_sno: str):
        """检查学生是否已经申请过该活动"""
        return await ActivityReview.get_or_none(
            activity_id=activity_id,
            student_sno=student_sno
    )

    @staticmethod
    async def create_apply(apply_data: ActivityApply):
        """创建活动申请记录"""
        async with in_transaction():
            review = await ActivityReview.create(
                activity_id=apply_data.activity_id,
                activity_title=apply_data.activity_title,
                teacher_id=apply_data.teacher_id,
                student_sno=apply_data.student_sno,
                status="审核中"
            )
            return review

    @staticmethod
    async def update_quota(activity_id: int):
        """更新活动名额"""
        async with in_transaction():
            activity = await Activity.get(id=activity_id)
            activity.quota -= 1
            await activity.save()
            return activity