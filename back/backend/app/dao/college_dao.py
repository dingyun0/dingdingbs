from backend.app.models.college import College
from typing import List, Optional
import logging

class CollegeDAO:
    @staticmethod
    async def get_college_list() -> List[College]:
        """获取学院列表"""
        try:
            return await College.all()
        except Exception as e:
            logging.error(f"获取学院列表失败: {str(e)}")
            raise e

    @staticmethod
    async def save_college(college_data: dict) -> College:
        """保存学院信息"""
        try:
            return await College.create(**college_data)
        except Exception as e:
            logging.error(f"保存学院信息失败: {str(e)}")
            raise e

    @staticmethod
    async def update_college(college_data: dict) -> College:
        """更新学院信息"""
        try:
            college_id = college_data.pop("id")
            college = await College.get(id=college_id)
            await college.update_from_dict(college_data)
            await college.save()
            return college
        except Exception as e:
            logging.error(f"更新学院信息失败: {str(e)}")
            raise e

    @staticmethod
    async def delete_college(college_id: int) -> None:
        """删除学院信息"""
        try:
            college = await College.get(id=college_id)
            await college.delete()
        except Exception as e:
            logging.error(f"删除学院信息失败: {str(e)}")
            raise e
