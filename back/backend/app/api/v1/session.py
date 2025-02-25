from fastapi import APIRouter, Depends
from backend.app.schemas.session import SaveSession
from backend.app.services.session_service import SessionService
from backend.app.common.jwt import DependsJwtUser

router = APIRouter()

@router.post('/saveSession', summary="保存课程")
async def save_sessions(sessions: SaveSession):
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