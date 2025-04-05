from typing import List
from tortoise.transactions import atomic
import json
import logging

from backend.app.dao.base import DaoBase
from backend.app.models.score import Score
from backend.app.models.score_review import ReviewScore
from backend.app.schemas.score import ScoreBase, ScoreReview


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

    async def get_inputted_college(self):
        """获取已录入成绩的学院信息"""
        try:
            # 获取所有成绩记录
            scores = await self.model.all()
            
            # 使用集合来存储唯一的组合
            unique_combinations = set()
            result = []
            
            # 遍历所有成绩记录，提取唯一的学院-专业-年级组合
            for score in scores:
                if score.department and score.major and score.grade:
                    combination = (score.department, score.major, score.grade)
                    if combination not in unique_combinations:
                        unique_combinations.add(combination)
                        result.append({
                            "department": score.department,
                            "major": score.major,
                            "grade": score.grade
                        })
            
            return result
        except Exception as e:
            print(f"获取已录入成绩的学院信息失败: {str(e)}")
            raise

    @atomic()
    async def save_score_review(self, data: ScoreReview) -> bool:
        """保存成绩疑问申请"""
        try:
            review_data = {
                "student_sno": data.student_sno,
                "student_name": data.student_name,
                "teacher_id": data.teacher_id,
                "question_type": data.question_type,
                "content": data.content,
                "status": data.status,
                "apply_time": data.apply_time,
                "review_time": data.review_time
            }
            await ReviewScore.create(**review_data)
            return True
        except Exception as e:
            logging.error(f"保存成绩疑问申请失败: {str(e)}", exc_info=True)
            return False

    async def get_review_score_list(self, page: int = 1, page_size: int = 10, status: str = None):
        """获取成绩疑问申请列表"""
        try:
            # 构建查询条件
            query = ReviewScore.all()
            if status:
                query = query.filter(status=status)
            
            # 获取总数
            total = await query.count()
            
            # 分页查询
            offset = (page - 1) * page_size
            reviews = await query.offset(offset).limit(page_size).order_by('-apply_time')
            
            return reviews, total
        except Exception as e:
            logging.error(f"获取成绩疑问申请列表失败: {str(e)}", exc_info=True)
            raise


# 创建全局实例
score_dao = ScoreDao()