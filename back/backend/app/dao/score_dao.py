from typing import List, Dict
from tortoise.transactions import atomic
import json
import logging
from datetime import datetime

from backend.app.dao.base import DaoBase
from backend.app.models.score import Score
from backend.app.models.score_review import ReviewScore
from backend.app.schemas.score import ScoreBase, ScoreReview, ScoreReviewResult, ScoreCreate, ScoreUpdate


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

    @atomic()
    async def save_score_review_result(self, data: ScoreReviewResult) -> bool:
        """保存成绩疑问审核结果"""
        try:
            # 获取当前时间作为审核时间
            current_time = datetime.now()
            
            # 更新审核状态和意见
            update_data = {
                "status": data.status,
                "review_comment": data.comment,
                "review_time": current_time
            }
            
            # 更新成绩疑问记录
            await ReviewScore.filter(id=data.review_id).update(**update_data)
            
            # 如果审核通过，这里可以添加其他逻辑，比如更新相关成绩等
            if data.status == "approved":
                # 获取成绩疑问记录
                review = await ReviewScore.get(id=data.review_id)
                if review:
                    # TODO: 根据需要添加成绩更新逻辑
                    pass
            
            return True
        except Exception as e:
            logging.error(f"保存成绩疑问审核结果失败: {str(e)}", exc_info=True)
            return False

    async def get_review_by_id(self, review_id: int):
        """获取单个成绩疑问记录"""
        try:
            review = await ReviewScore.get_or_none(id=review_id)
            return review
        except Exception as e:
            logging.error(f"获取成绩疑问记录失败: {str(e)}", exc_info=True)
            raise
        
    async def get_score_review_result(self, student_sno: str):
        """获取成绩疑问审核结果"""
        try:
            # 获取学生的所有成绩疑问记录，按申请时间倒序排序
            results = await ReviewScore.filter(student_sno=student_sno).order_by('-apply_time')
            
            # 转换为列表格式
            review_list = []
            for result in results:
                review_dict = {
                    "id": result.id,
                    "student_sno": result.student_sno,
                    "student_name": result.student_name,
                    "question_type": result.question_type,
                    "content": result.content,
                    "status": result.status,
                    "apply_time": str(result.apply_time),
                    "review_time": str(result.review_time) if result.review_time else None,
                    "review_comment": result.review_comment
                }
                review_list.append(review_dict)
            
            return review_list
        except Exception as e:
            logging.error(f"获取成绩疑问审核结果失败: {str(e)}", exc_info=True)
            raise

    async def get_college_scores(self, department: str, major: str, grade: str, courses):
        """获取学院成绩信息"""
        try:
            # 获取指定学院专业年级的所有学生成绩
            scores = await self.model.filter(
                department=department,
                major=major,
                grade=grade
            ).all()
            
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
            logging.error(f"获取学院成绩信息失败: {str(e)}", exc_info=True)
            raise

    async def update_score(self, score_data: Dict) -> bool:
        """更新成绩记录"""
        try:
            print(score_data,'22222222222')
            await self.model.filter(sno=score_data["sno"]).update(**score_data)
            return True
        except Exception as e:
            print(f"更新成绩失败: {str(e)}")
            return False

    async def add_score(self, score_data: Dict) -> bool:
        """添加成绩记录"""
        try:
            await self.model.create(**score_data)
            return True
        except Exception as e:
            print(f"添加成绩失败: {str(e)}")
            return False

# 创建全局实例
score_dao = ScoreDao()