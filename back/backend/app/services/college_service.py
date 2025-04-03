from backend.app.models.college import College
from backend.app.dao.college_dao import CollegeDAO
from backend.app.common.exception.errors import CustomError
import logging
from typing import List
from backend.app.schemas.college import CollegeInDB

class CollegeService:
    @staticmethod
    async def get_college_list() -> List[CollegeInDB]:
        """获取学院列表"""
        try:
            colleges = await CollegeDAO.get_college_list()
            return [CollegeInDB.model_validate(college) for college in colleges]
        except Exception as e:
            logging.error(f"获取学院列表失败: {str(e)}")
            raise CustomError(message="获取学院列表失败")

    @staticmethod
    async def save_college(college_data: dict) -> CollegeInDB:
        """保存学院信息"""
        try:
            college = await CollegeDAO.save_college(college_data)
            return CollegeInDB.model_validate(college)
        except Exception as e:
            logging.error(f"保存学院信息失败: {str(e)}")
            raise CustomError(message="保存学院信息失败")

    @staticmethod
    async def update_college(college_data: dict) -> CollegeInDB:
        """更新学院信息"""
        try:
            college = await CollegeDAO.update_college(college_data)
            return CollegeInDB.model_validate(college)
        except Exception as e:
            logging.error(f"更新学院信息失败: {str(e)}")
            raise CustomError(message="更新学院信息失败")

    @staticmethod
    async def delete_college(college_id: int) -> None:
        """删除学院信息"""
        try:
            await CollegeDAO.delete_college(college_id)
        except Exception as e:
            logging.error(f"删除学院信息失败: {str(e)}")
            raise CustomError(message="删除学院信息失败")