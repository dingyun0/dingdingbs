from fastapi import APIRouter, Depends
from backend.app.schemas.comprehensive_test import SaveComprehensiveTest
from backend.app.services.comprehensive_test_service import ComprehensiveTestService
from backend.app.common.jwt import DependsJwtUser

router = APIRouter()

@router.post('/save', summary="保存综合测评")
async def save_tests(tests: SaveComprehensiveTest):
    """
    保存综合测评
    """
    print("路由层接收到请求数据:", tests.model_dump())
    return await ComprehensiveTestService.save_tests(tests)

@router.get('/all', summary="获取综合测评信息")
async def get_all_tests():
    """
    获取所有综合测评
    """
    return await ComprehensiveTestService.get_all_tests()

@router.get('/student/{sno}', summary="获取学生学业分信息")
async def get_student_test(sno: str):
    """
    获取指定学号的学生学业分信息
    """
    return await ComprehensiveTestService.get_test_by_sno(sno) 