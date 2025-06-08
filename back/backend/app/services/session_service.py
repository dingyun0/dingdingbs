from backend.app.models.session import Session
from backend.app.dao.session_dao import session_dao
from backend.app.schemas.session import SessionList, FilteredCoursesResponse, CourseItem
from backend.app.common.exception.errors import CustomError
import logging
import json
from typing import List

class SessionService:
    @staticmethod
    async def save_sessions(sessions: SessionList):
        try:
            print(f"Service层接收到 {len(sessions.sessions)} 条数据")
            count = await session_dao.save_sessions(sessions.sessions)
            return {
                "code": 200,
                "message": "保存成功",
                "data": {
                    "total": len(sessions.sessions),
                    "success": count
                }
            }
        except Exception as e:
            logging.error(f"保存课程失败: {str(e)}", exc_info=True)
            raise CustomError(msg=f"保存课程失败: {str(e)}", code=500)
        
    @staticmethod
    async def get_all_sessions():
        try:
            sessions = await Session.all()
            return {
                "code": 200,
                "message": "获取成功",
                "data": [
                    {
                        "id": session.id,
                        "course_id": session.course_id,
                        "course_name": session.course_name,
                        "credit": session.credit,
                        "hours": session.hours,
                        "nature": session.nature,
                        "college": session.college,
                        "major": session.major,
                        "grade": session.grade
                    } for session in sessions
                ]
            }
        except Exception as e:
            logging.error(f"获取课程失败: {str(e)}", exc_info=True)
            raise CustomError(msg=f"获取课程失败: {str(e)}", code=500)

    @staticmethod
    async def get_session_options():
        """获取所有不重复的学院、专业、年级选项"""
        try:
            # 使用 distinct 获取不重复的值
            colleges = await Session.all().distinct().values_list('college', flat=True)
            majors = await Session.all().distinct().values_list('major', flat=True)
            grades = await Session.all().distinct().values_list('grade', flat=True)
            
            return {
                "code": 200,
                "message": "获取成功",
                "data": {
                    "colleges": sorted(list(filter(None, colleges))),  # 过滤掉空值并排序
                    "majors": sorted(list(filter(None, majors))),
                    "grades": sorted(list(filter(None, grades)))
                }
            }
        except Exception as e:
            logging.error(f"获取课程选项失败: {str(e)}", exc_info=True)
            raise CustomError(msg=f"获取课程选项失败: {str(e)}", code=500)

    @staticmethod
    async def get_filtered_courses(department: str, major: str, grade: str) -> FilteredCoursesResponse:
        """根据条件筛选课程"""
        try:
            # 构建查询条件
            conditions = {
                "college": department,
                "major": major,
                "grade": grade
            }
            
            # 查询符合条件的课程
            sessions = await Session.filter(**conditions).values("course_id", "course_name")
            
            # 转换为响应格式
            course_items = [
                CourseItem(
                    course_id=session["course_id"],
                    course_name=session["course_name"]
                )
                for session in sessions
            ]
            
            return FilteredCoursesResponse(
                code=200,
                message="获取课程列表成功",
                data=course_items
            )
            
        except Exception as e:
            logging.error(f"获取课程列表失败: {str(e)}", exc_info=True)
            return FilteredCoursesResponse(
                code=500,
                message=f"获取课程列表失败: {str(e)}",
                data=[]
            )