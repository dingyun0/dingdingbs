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

@router.get('/all', summary="获取成绩信息")
async def get_all_scores(
    department: str = None,
    major: str = None,
    grade: str = None
):
    """
    获取成绩信息
    
    Args:
        department: 学院
        major: 专业
        grade: 年级
        
    Returns:
        成绩列表
    """
    return await ScoreService.get_all_scores(department, major, grade)

@router.get('/recorded-classes', summary="获取已录入成绩的班级信息")
async def get_recorded_classes():
    """
    获取已录入成绩的班级信息，包括学院、专业、年级、班级和已录入人数
    """
    return await ScoreService.get_recorded_classes()

