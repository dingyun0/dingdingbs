from fastapi import APIRouter, Depends, Query
from backend.app.schemas.activity import ActivityApply, CreateActivity, UpdateActivity, ActivityInfo
from backend.app.services.activity_service import ActivityService
from backend.app.common.jwt import DependsJwtUser

router = APIRouter()

@router.post('/addActivity', summary="增加活动公告")
async def add_activity(activity: CreateActivity, current_user = DependsJwtUser):
    """
    保存活动公告
    """
    return await ActivityService.add_activity(activity)

@router.put('/updateActivity',summary="更新活动公告")
async def update_activity(activity: UpdateActivity, current_user = DependsJwtUser):
    """
    更新活动公告
    """
    return await ActivityService.update_activity(activity)

@router.delete('/delete/{id}', summary="删除选择活动公告")
async def delete_activity(id: int, current_user = DependsJwtUser):
    """
    删除活动公告
    """
    return await ActivityService.delete_activity(id)

@router.get('/activityList', summary="获取活动公告列表")
async def get_activity_list(current_user = DependsJwtUser):
    """
    获取活动公告列表
    """
    return await ActivityService.get_activity_list()
    


@router.post('/applyActivity', summary="存储申请活动信息")
async def apply_activity(apply_data: ActivityApply):
    """
    申请活动接口
    - activity_id: 活动ID
    - activity_title: 活动名称
    - teacher_id: 审核老师ID
    - student_sno: 申请学生学号
    """
    try:
        result = await ActivityService.apply_activity(apply_data)
        return result
    except Exception as e:
        print("申请活动接口错误:", str(e))
        return {"code": 500, "msg": f"申请失败: {str(e)}", "data": None}