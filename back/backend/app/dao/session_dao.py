from typing import List
from tortoise.transactions import atomic
import json

from backend.app.dao.base import DaoBase
from backend.app.models.session import Session
from backend.app.schemas.session import SessionBase

class SessionDao(DaoBase):
    """课程数据访问对象"""

    @atomic()
    async def save_sessions(self, sessions: List[SessionBase]):
        """批量保存课程"""
        try:
            # print("DAO层接收到的数据:", json.dumps(
            #     [session.model_dump() for session in sessions], 
            #     ensure_ascii=False, 
            #     indent=2
            # ))
            for session in sessions:
                session_dict = session.model_dump()
                print("处理单条课程:", json.dumps(session_dict, ensure_ascii=False))
                existing = await self.model.filter(course_id=session.course_id).first()
                if existing:
                    await self.model.filter(course_id=session.course_id).update(**session_dict)
                else:
                    await self.model.create(**session_dict)
            return True
        except Exception as e:
            print("DAO层错误:", str(e))
            raise

# 创建全局实例
session_dao = SessionDao(Session)