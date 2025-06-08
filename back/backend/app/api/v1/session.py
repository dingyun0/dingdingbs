from fastapi import APIRouter, Depends, Query
from backend.app.schemas.session import SessionList
from backend.app.services.session_service import SessionService
from backend.app.common.jwt import DependsJwtUser

router = APIRouter()

@router.post('/saveSession', summary="保存课程")
async def save_sessions(sessions: SessionList):
    """
    保存课程
    """
    
    print("路由层接收到请求数据:", sessions.model_dump())
    return await SessionService.save_sessions(sessions) 

@router.get('/allSession',summary="获取成绩信息")
async def get_all_sessions():
    """
    获取所有成绩
    """
    return await SessionService.get_all_sessions()

@router.get('/options', summary="获取课程选项")
async def get_session_options():
    """
    获取课程表中所有不重复的学院、专业、年级选项
    """
    return await SessionService.get_session_options()

@router.get('/filtered-courses', summary="根据学院，专业，年级过滤课程")
async def get_filtered_courses(
    department: str = Query(..., description="学院"),
    major: str = Query(..., description="专业"),
    grade: str = Query(..., description="年级")
):
    """
    根据学院，专业，年级获取课程列表
    """
    return await SessionService.get_filtered_courses(department, major, grade)
    