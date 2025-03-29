from fastapi import APIRouter, Depends, Query
from backend.app.schemas.activity import ActivityApply, CreateActivity, ReviewRequest, UpdateActivity, ActivityInfo
from backend.app.services.activity_service import ActivityService
from backend.app.common.jwt import DependsJwtUser
from backend.app.models.teacher import Teacher  # 添加这行

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

@router.get('/getReviewActivity', summary="获取要审核的活动列表")
async def review_activity(current_user = DependsJwtUser):
    """
    获取教师需要审核的活动列表
    """
    try:
        # 从Teacher表中获取教师ID
        teacher = await Teacher.get_or_none(user_id=current_user.id)
        print('111111111',teacher.id)
        if not teacher:
            return {"code": 400, "msg": "未找到教师信息", "data": None}
            
        return await ActivityService.get_review_activities(teacher.id)
    except Exception as e:
        print("获取审核列表失败:", str(e))
        return {"code": 500, "msg": f"获取失败: {str(e)}", "data": None}


@router.post('/handleReviewActivity', summary='审核学生活动')
async def handle_review_activity(review_data: ReviewRequest, current_user = DependsJwtUser):
    """
    审核学生活动申请
    - review_id: 审核记录ID
    - status: 审核结果（通过/不通过）
    - comment: 审核意见
    """
    try:
        # 验证教师身份
        teacher = await Teacher.get_or_none(user_id=current_user.id)
        if not teacher:
            return {"code": 400, "msg": "未找到教师信息", "data": None}
            
        return await ActivityService.handle_review(
            review_id=review_data.review_id,
            review_comment=review_data.review_comment,
            comment=review_data.comment
        )
    except Exception as e:
        print("审核活动失败:", str(e))
        return {"code": 500, "msg": f"审核失败: {str(e)}", "data": None}
    
@router.get('/getReviewMessage', summary='获取当前学号的审核情况')
async def get_review_message(student_sno: str):
    """
    获取学生的活动审核情况
    - student_sno: 学生学号
    """
    try:
        return await ActivityService.get_review_message(student_sno)
    except Exception as e:
        print("获取审核消息失败:", str(e))
        return {"code": 500, "msg": f"获取失败: {str(e)}", "data": None}
    

@router.get('/activity-scores', summary="根据学号和活动类型获取活动学分")
async def activity_scores(student_sno: str, activity_category: str = None):
    """
    获取学生的活动分数
    
    Args:
        student_sno: 学生学号
        activity_category: 活动类型（可选，不传则获取所有类型）
        
    Returns:
        活动分数列表，包含活动ID、标题和学分
    """
    try:
        return await ActivityService.activity_scores(student_sno, activity_category)
    except Exception as e:
        print("获取活动分数失败:", str(e))
        return {"code": 500, "msg": f"获取失败: {str(e)}", "data": None}