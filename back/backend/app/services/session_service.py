from backend.app.models.session import Session
from backend.app.dao.session_dao import session_dao
from backend.app.schemas.session import SaveSession
from backend.app.common.exception.errors import CustomError
import logging
import json

class SessionService:
    @staticmethod
    async def save_sessions(sessions: SaveSession):
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
                        "department": session.department
                    } for session in sessions
                ]
            }
        except Exception as e:
            logging.error(f"获取课程失败: {str(e)}", exc_info=True)
            raise CustomError(msg=f"获取课程失败: {str(e)}", code=500)