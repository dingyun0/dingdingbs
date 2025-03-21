from datetime import datetime
from backend.app.dao.activity_dao import ActivityDAO
from backend.app.schemas.activity import ActivityApply, CreateActivity, UpdateActivity, ActivityInfo
from tortoise import timezone

class ActivityService:
    @staticmethod
    async def add_activity(activity: CreateActivity):
        """添加活动"""
        try:
            # 打印接收到的数据
            print("Received activity data:", activity)
            print("Activity type:", type(activity))
            
            # 调用DAO层创建活动
            result = await ActivityDAO.create(activity)
            return {"code": 200, "msg": "添加成功", "data": result}
        except Exception as e:
            print("Error details:", str(e))
            return {"code": 500, "msg": f"添加失败: {str(e)}", "data": None}

    @staticmethod
    async def update_activity(activity: UpdateActivity):
        """更新活动"""
        try:
            # 检查活动是否存在
            existing_activity = await ActivityDAO.get_by_id(activity.id)
            if not existing_activity:
                return {"code": 404, "msg": "活动不存在", "data": None}
            
            # 调用DAO层更新活动
            result = await ActivityDAO.update(activity)
            return {"code": 200, "msg": "更新成功", "data": result}
        except Exception as e:
            return {"code": 500, "msg": f"更新失败: {str(e)}", "data": None}

    @staticmethod
    async def delete_activity(activity_id: int):
        """删除活动"""
        try:
            # 检查活动是否存在
            existing_activity = await ActivityDAO.get_by_id(activity_id)
            if not existing_activity:
                return {"code": 404, "msg": "活动不存在", "data": None}
            
            # 调用DAO层删除活动
            await ActivityDAO.delete(activity_id)
            return {"code": 200, "msg": "删除成功", "data": None}
        except Exception as e:
            return {"code": 500, "msg": f"删除失败: {str(e)}", "data": None}

    @staticmethod
    async def get_activity_list():
        """获取活动列表"""
        try:
            # 调用DAO层获取活动列表
            activities = await ActivityDAO.get_all()
            total = await ActivityDAO.get_total()
            
            return {
                "code": 200,
                "msg": "获取成功",
                "data": {
                    "list": activities,
                    "total": total
                }
            }
        except Exception as e:
            return {"code": 500, "msg": f"获取失败: {str(e)}", "data": None}

    @staticmethod
    async def apply_activity(apply_data: ActivityApply):
        """申请活动"""
        try:
            # 检查活动是否存在
            activity = await ActivityDAO.get_by_id(apply_data.activity_id)
            if not activity:
                return {"code": 404, "msg": "活动不存在", "data": None}
            
            # 检查活动是否已过期 - 使用timezone.now()替代datetime.now()
            if activity.deadline < timezone.now():
                return {"code": 400, "msg": "活动已过截止日期", "data": None}
            
            # 检查名额是否已满
            if activity.quota <= 0:
                return {"code": 400, "msg": "活动名额已满", "data": None}
            
            # 检查是否重复申请
            existing_apply = await ActivityDAO.get_student_apply(
                apply_data.activity_id, 
                apply_data.student_sno
            )
            if existing_apply:
                return {"code": 400, "msg": "已经申请过该活动", "data": None}
            
            # 创建申请记录
            result = await ActivityDAO.create_apply(apply_data)
            
            # 更新活动名额
            await ActivityDAO.update_quota(apply_data.activity_id)
            
            return {"code": 200, "msg": "申请成功", "data": result}
        except Exception as e:
            print("申请活动失败:", str(e))
            return {"code": 500, "msg": f"申请失败: {str(e)}", "data": None}