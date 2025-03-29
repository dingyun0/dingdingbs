from typing import List
from tortoise.transactions import atomic
import json

from backend.app.dao.base import DaoBase
from backend.app.models.session import Session
from backend.app.schemas.session import SessionBase

class SessionDao(DaoBase):
    """课程数据访问对象"""

    def __init__(self):
        super().__init__(Session)

    async def get_filtered_courses(self, department: str = None, major: str = None, grade: str = None):
        """
        获取筛选后的课程列表
        
        Args:
            department: 学院
            major: 专业
            grade: 年级
            
        Returns:
            课程列表
        """
        try:
            query = self.model.all()
            
            if department:
                query = query.filter(college=department)
            if major:
                query = query.filter(major=major)
            if grade:
                query = query.filter(grade=grade)
                
            return await query
            
        except Exception as e:
            print(f"获取课程列表失败: {str(e)}")
            raise

    @atomic()
    async def save_sessions(self, sessions: List[SessionBase]):
        """批量保存课程"""
        try:
            for session in sessions:
                session_dict = session.model_dump()
                print(f"正在处理课程: {session.course_id}")
                
                # 验证必填字段
                if not all([
                    session.course_id,
                    session.course_name,
                    session.credit,
                    session.hours,
                    session.nature,
                    session.college,
                    session.major,
                    session.grade
                ]):
                    raise ValueError("所有字段都是必填的")
                    
                existing = await self.model.filter(course_id=session.course_id).first()
                if existing:
                    print(f"更新已存在的课程: {session.course_id}")
                    await self.model.filter(course_id=session.course_id).update(**session_dict)
                else:
                    print(f"创建新课程: {session.course_id}")
                    await self.model.create(**session_dict)
            return True
        except Exception as e:
            print(f"DAO层错误: {str(e)}")
            print(f"错误类型: {type(e)}")
            import traceback
            print(f"错误堆栈: {traceback.format_exc()}")
            raise

# 创建全局实例
session_dao = SessionDao()