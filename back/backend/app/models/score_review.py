#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class ReviewScore(Model):
    """成绩疑问申请表"""
    id = fields.IntField(pk=True, description="ID")
    student_sno = fields.CharField(max_length=20, description="学生学号")
    student_name = fields.CharField(max_length=50, description="学生姓名")
    teacher_id = fields.IntField(description="审核老师ID")
    question_type = fields.CharField(max_length=20, description="疑问类型")  # academic/moral/sports/other
    content = fields.TextField(description="疑问说明")
    status = fields.CharField(max_length=20, description="状态", default="pending")  # pending/approved/rejected
    apply_time = fields.DatetimeField(description="申请时间", auto_now_add=True)
    review_time = fields.DatetimeField(description="审核时间", null=True)
    review_comment = fields.TextField(description="审核意见", null=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

  

    class Meta:
        table = "score_review"
        description = "成绩疑问申请表"
    
    def __str__(self):
        return f"{self.student_name} - {self.semester} - {self.status}"

    @classmethod
    async def get_student_questions(cls, student_sno: str):
        """获取学生的所有疑问申请记录"""
        return await cls.filter(student_sno=student_sno).all()

    @classmethod
    async def get_teacher_questions(cls, teacher_id: int):
        """获取老师需要审核的所有记录"""
        return await cls.filter(teacher_id=teacher_id).all()

    async def approve(self, comment: str = None):
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
