from fastapi import APIRouter, Depends
from backend.app.schemas.score import SaveScore, ScoreReview, ScoreReviewResult, ScoreCreate, ScoreUpdate
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

@router.get('/inputted-college', summary="获取已录入成绩的学院信息")
async def get_inputted_college():
    """
    获取已录入成绩的学院信息
    """
    return await ScoreService.get_inputted_college()

@router.post('/review_score', summary="提交成绩疑问申请")
async def submit_score_review(data: ScoreReview):
    """
    提交成绩疑问申请
    
    Args:
        data: 成绩疑问申请数据
        
    Returns:
        提交结果
    """
    return await ScoreService.submit_score_review(data)

@router.get('/get_review_score_list', summary="获取成绩疑问申请列表")
async def get_review_score_list(
    page: int = 1,
    page_size: int = 10,
    status: str = None
):
    """
    获取成绩疑问申请列表
    
    Args:
        page: 页码
        page_size: 每页数量
        status: 状态筛选（可选）
        
    Returns:
        成绩疑问申请列表和总数
    """
    return await ScoreService.get_review_score_list(page, page_size, status)

@router.post('/submit_score_review_result', summary="提交成绩疑问审核结果")
async def submit_score_review_result(data: ScoreReviewResult):
    """
    提交成绩疑问审核结果
    """
    return await ScoreService.submit_score_review_result(data)

@router.get('/get_score_review_result', summary="获取成绩疑问审核结果")
async def get_score_review_result(
    student_sno: str,
):
    """
    获取成绩疑问审核结果
    """
    return await ScoreService.get_score_review_result(student_sno)

@router.get('/get_college_scores', summary="获取学院成绩信息")
async def get_college_scores(
    department: str,
    major: str,
    grade: str
):
    """
    获取学院成绩信息
    """
    return await ScoreService.get_college_scores(department, major, grade)

@router.post('/update_score', summary="修改成绩")
async def update_score(score_data: ScoreUpdate, current_user = DependsJwtUser):
    """
    修改学生成绩
    """
    try:
        result = await ScoreService.update_score(score_data)
        return result
    except Exception as e:
        return {"code": 500, "msg": f"修改失败: {str(e)}", "data": None}

@router.post('/add_score', summary="添加成绩")
async def add_score(score_data: ScoreCreate, current_user = DependsJwtUser):
    """
    添加学生成绩
    """
    try:
        result = await ScoreService.add_score(score_data)
        return result
    except Exception as e:
        return {"code": 500, "msg": f"添加失败: {str(e)}", "data": None}