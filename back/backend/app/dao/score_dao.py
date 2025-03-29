from typing import List
from tortoise.transactions import atomic
import json

from backend.app.dao.base import DaoBase
from backend.app.models.score import Score
from backend.app.schemas.score import ScoreBase


class ScoreDao(DaoBase):
    """成绩数据访问对象"""
    
    def __init__(self):
        super().__init__(Score)

    @atomic()
    async def save_scores(self, scores: List[ScoreBase]):
        """批量保存成绩"""
        try:
            print("DAO层接收到的数据:", json.dumps(
                [score.model_dump() for score in scores], 
                ensure_ascii=False, 
                indent=2
            ))
            for score in scores:
                score_dict = score.model_dump()
                print("处理单条成绩:", json.dumps(score_dict, ensure_ascii=False))
                existing = await self.model.filter(sno=score.sno).first()
                if existing:
                    await self.model.filter(sno=score.sno).update(**score_dict)
                else:
                    await self.model.create(**score_dict)
            return True
        except Exception as e:
            print("DAO层错误:", str(e))
            raise

    async def get_scores_by_courses(self, courses):
        """
        根据课程列表获取成绩
        
        Args:
            courses: 课程列表
            
        Returns:
            成绩列表
        """
        try:
            # 获取所有学生的成绩记录
            scores = await self.model.all()
            
            # 过滤出有对应课程成绩的学生
            filtered_scores = []
            for score in scores:
                has_course_score = False
                for course in courses:
                    if hasattr(score, course.course_name) and getattr(score, course.course_name):
                        has_course_score = True
                        break
                if has_course_score:
                    filtered_scores.append(score)
            
            return filtered_scores
        except Exception as e:
            print(f"获取成绩失败: {str(e)}")
            raise




# 创建全局实例
score_dao = ScoreDao()