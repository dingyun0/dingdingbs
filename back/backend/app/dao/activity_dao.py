from datetime import datetime
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


    @staticmethod
    async def get_review_activities(teacher_id: int):
        """获取教师需要审核的活动列表"""
        print('222222222',teacher_id)
        return await ActivityReview.filter(
            teacher_id=teacher_id,
            review_comment="审核中"
        ).order_by("-apply_time")

    @staticmethod
    async def get_review_by_id(review_id: int):
        """根据ID获取审核记录"""
        return await ActivityReview.get_or_none(id=review_id)


    @staticmethod
    async def update_review_status(review_id: int, review_comment: str, comment: str):
        """更新活动审核状态"""
        async with in_transaction():
            review = await ActivityReview.get(id=review_id)
            review.review_comment = "审核通过" if review_comment == "通过" else "审核未通过"
            review.comment = comment
            review.status='申请通过' if review_comment=='通过' else '申请未通过'
            review.review_time = datetime.now()
            await review.save()
            return review

        
    @staticmethod
    async def get_review_message(student_sno: str):
        """获取学生的活动审核情况"""
        return await ActivityReview.filter(
            student_sno=student_sno
        ).order_by("-apply_time")
