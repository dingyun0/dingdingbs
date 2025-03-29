from backend.app.models.score import Score
from backend.app.dao.score_dao import score_dao
from backend.app.dao.session_dao import session_dao
from backend.app.schemas.score import SaveScore
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
                    "class_name": score.class_name
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