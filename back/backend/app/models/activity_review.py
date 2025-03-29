#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class ActivityReview(Model):
    """活动审核表"""
    id = fields.IntField(pk=True, description="主键ID")
    activity_id = fields.IntField(description="活动ID")
    activity_title = fields.CharField(max_length=255, description="活动名称")
    teacher_id = fields.IntField(description="审核老师ID")
    student_sno = fields.CharField(max_length=20, description="申请学生学号")
    activity_category = fields.CharField(max_length=50, description='活动类型')  # 学业/文体/劳动/创新
    credits = fields.IntField(description='加分数', default=0)
    status = fields.CharField(max_length=20, description="审核状态", default="已申请")  # pending, approved, rejected
    apply_time = fields.DatetimeField(description="申请时间", auto_now_add=True)
    review_time = fields.DatetimeField(description="审核时间", null=True)
    review_comment = fields.TextField(description="审核意见", default="审核中")
    comment=fields.TextField(description="审核评论", null=True)
    
    # 外键关联
    # activity = fields.ForeignKeyField(
    #     'models.Activity', 
    #     related_name='reviews',
    #     description="关联的活动"
    # )
    # teacher = fields.ForeignKeyField(
    #     'models.Teacher',
    #     related_name='activity_reviews',
    #     description="审核老师"
    # )
    # student = fields.ForeignKeyField(
    #     'models.Student',
    #     related_name='activity_reviews',
    #     description="申请学生"
    # )

    class Meta:
        table = "activity_reviews"
        description = "活动审核表"

    def __str__(self):
        return f"{self.activity_title} - {self.student_sno} - {self.status}"

    @classmethod
    async def get_student_reviews(cls, student_sno: str):
        """获取学生的所有活动申请记录"""
        return await cls.filter(student_sno=student_sno).all()

    @classmethod
    async def get_teacher_reviews(cls, teacher_id: int):
        """获取老师需要审核的所有记录"""
        return await cls.filter(teacher_id=teacher_id).all()

    async def approve(self,  comment: str = None):
        """审核通过"""
        self.status = "approved"
        self.review_comment = comment
        self.review_time = datetime.now()
        await self.save()

    async def reject(self, comment: str):
        """审核拒绝"""
        self.status = "rejected"
        self.review_comment = comment
        self.review_time = datetime.now()
        await self.save()