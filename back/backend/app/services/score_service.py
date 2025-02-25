from backend.app.models.score import Score
from backend.app.dao.score_dao import score_dao
from backend.app.schemas.score import SaveScore
from backend.app.common.exception.errors import CustomError
import logging
import json

class ScoreService:
    @staticmethod
    async def save_scores(scores: SaveScore):
        try:
            print("Service层接收到数据:", json.dumps(scores.model_dump(), ensure_ascii=False, indent=2))
            await score_dao.save_scores(scores.scores)
            return {"message": "保存成功"}
        except Exception as e:
            logging.error(f"保存成绩失败: {str(e)}", exc_info=True)
            raise CustomError(msg=f"保存成绩失败: {str(e)}", code=500)
        
    @staticmethod
    async def get_all_scores():
        try:
            scores = await Score.all()
            return {
                "code": 200,
                "message": "获取成功",
                "data": [
                    {
                        "id": score.id,
                        "name": score.name,
                        "sno": score.sno,
                        "class_name": score.class_name,
                        "操作系统课程设计成绩": score.操作系统课程设计成绩,
                        "无线网络技术成绩": score.无线网络技术成绩,
                        "计算机网络课程设计": score.计算机网络课程设计,
                        "操作系统": score.操作系统,
                        "人工智能与网络技术学科前沿": score.人工智能与网络技术学科前沿,
                        "信息安全原理及应用": score.信息安全原理及应用,
                        "Linux操作系统": score.Linux操作系统,
                        "Java程序设计": score.Java程序设计
                    } for score in scores
                ]
            }
        except Exception as e:
            logging.error(f"获取成绩失败: {str(e)}", exc_info=True)
            raise CustomError(msg=f"获取成绩失败: {str(e)}", code=500)