from backend.app.models.score import Score
from backend.app.dao.score_dao import score_dao
from backend.app.dao.session_dao import session_dao
from backend.app.schemas.score import SaveScore, ScoreReview
from backend.app.common.exception.errors import CustomError
import logging
import json

class ScoreService:
    @staticmethod
    async def save_scores(scores: SaveScore):
        """保存成绩"""
        try:
            print(f"Service层接收到 {len(scores.scores)} 条数据")
            print("课程字段列表:", scores.course_fields)
            
            # 使用动态模型验证数据
            validated_scores = scores.get_validated_scores()
            print("验证后的数据:", json.dumps(
                [score.model_dump() for score in validated_scores],
                ensure_ascii=False,
                indent=2
            ))
            
            success = await score_dao.save_scores(validated_scores)
            return {
                "code": 200,
                "message": "保存成功",
                "data": {
                    "total": len(validated_scores),
                    "success": success
                }
            }
        except Exception as e:
            logging.error(f"保存成绩失败: {str(e)}", exc_info=True)
            raise CustomError(msg=f"保存成绩失败: {str(e)}", code=500)
        
    @staticmethod
    async def get_all_scores(department: str = None, major: str = None, grade: str = None):
        """
        获取成绩信息
        
        Args:
            department: 学院
            major: 专业
            grade: 年级
            
        Returns:
            成绩列表
        """
        try:
            # 使用全局实例而不是创建新的实例
            courses = await session_dao.get_filtered_courses(department, major, grade)
            print('获取到的课程是：',courses)
            
            if not courses:
                return {"code": 200, "message": "未找到符合条件的课程", "data": []}
            
            # 使用全局实例而不是创建新的实例
            scores = await score_dao.get_scores_by_courses(courses)
            
            if not scores:
                return {"code": 200, "message": "未找到成绩数据", "data": []}
            
            # 组织返回数据
            result = []
            for score in scores:
                score_dict = {
                    "sno": score.sno,
                    "name": score.name,
                    "department":score.department,
                    "major":score.major,
                    "grade":score.grade
                }
                
                # 动态添加课程成绩
                for course in courses:
                    score_dict[course.course_name] = getattr(score, course.course_name, "")
                
                result.append(score_dict)
            
            return {
                "code": 200,
                "message": "获取成功",
                "data": result
            }
        
        except Exception as e:
            print(f"获取成绩失败: {str(e)}")
            return {"code": 500, "message": f"获取成绩失败: {str(e)}"}
        
    @staticmethod
    async def get_inputted_college():
        """获取已录入成绩的学院信息"""
        try:
            colleges = await score_dao.get_inputted_college()
            return {
                "code": 200,
                "message": "获取成功",
                "data": colleges
            }
        except Exception as e:
            logging.error(f"获取已录入成绩的学院信息失败: {str(e)}", exc_info=True)
            return {"code": 500, "message": f"获取成绩失败: {str(e)}"}
    
    @staticmethod
    async def submit_score_review(data: ScoreReview):
        """提交成绩疑问申请"""
        try:
            success = await score_dao.save_score_review(data)
            print("提交成绩疑问申请成功:", success)
            if success:
                return {
                    "code": 200,
                    "message": "提交成功",
                    "data": data.model_dump()
                }
            return {
                "code": 500,
                "message": "提交失败",
                "data": None
            }
        except Exception as e:
            logging.error(f"提交成绩疑问申请失败: {str(e)}", exc_info=True)
            return {"code": 500, "message": f"提交失败: {str(e)}"}
        
    @staticmethod
    async def get_review_score_list(page: int = 1, page_size: int = 10, status: str = None):
        """获取成绩疑问申请列表"""
        try:
            reviews, total = await score_dao.get_review_score_list(page, page_size, status)
            # 将 Tortoise ORM 模型转换为字典
            review_list = []
            for review in reviews:
                review_dict = {
                    "id": review.id,
                    "student_sno": review.student_sno,
                    "student_name": review.student_name,
                    "teacher_id": review.teacher_id,
                    "question_type": review.question_type,
                    "content": review.content,
                    "status": review.status,
                    "apply_time": str(review.apply_time),
                    "review_time": str(review.review_time) if review.review_time else None,
                    "review_comment": review.review_comment
                }
                review_list.append(review_dict)
            
            return {
                "code": 200,
                "message": "获取成功",
                "data": {
                    "list": review_list,
                    "total": total,
                    "page": page,
                    "page_size": page_size
                }
            }
        except Exception as e:
            logging.error(f"获取成绩疑问申请列表失败: {str(e)}", exc_info=True)
            return {
                "code": 500,
                "message": f"获取失败: {str(e)}",
                "data": None
            }
    