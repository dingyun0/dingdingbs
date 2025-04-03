from fastapi import APIRouter
from backend.app.services.college_service import CollegeService
from backend.app.common.jwt import DependsJwtUser
from backend.app.schemas.college import CollegeCreate, CollegeUpdate, CollegeInDB
from typing import List

router = APIRouter()

@router.get('/get_college_list', summary="获取学院列表", response_model=List[CollegeInDB])
async def get_college_list(current_user = DependsJwtUser):
    """获取学院列表"""
    result = await CollegeService.get_college_list()
    return result

@router.post('/save_college', summary="添加学院信息", response_model=CollegeInDB)
async def save_college(college: CollegeCreate, current_user = DependsJwtUser):
    """添加学院信息"""
    result = await CollegeService.save_college(college.dict())
    return result

@router.put('/update_college', summary="更新学院信息", response_model=CollegeInDB)
async def update_college(college: CollegeUpdate, current_user = DependsJwtUser):
    """更新学院信息"""
    result = await CollegeService.update_college(college.dict())
    return result

@router.delete('/delete_college/{college_id}', summary="删除学院信息")
async def delete_college(college_id: int, current_user = DependsJwtUser):
    """删除学院信息"""
    await CollegeService.delete_college(college_id)
    return {"code": 200, "msg": "删除成功"}