from fastapi import APIRouter, Depends
from backend.app.schemas.score import SaveScore
from backend.app.services.score_service import ScoreService
from backend.app.common.jwt import DependsJwtUser

router = APIRouter()

@router.post('/save', summary="保存成绩")
async def save_scores(scores: SaveScore):
    """
    保存成绩
    """
    print("路由层接收到请求数据:", scores.model_dump())
    return await ScoreService.save_scores(scores)

@router.get('/all',summary="获取成绩信息")
async def get_all_scores():
    """
    获取所有成绩
    """
    return await ScoreService.get_all_scores()