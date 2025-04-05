#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request, Response, UploadFile
# from backend.app.models.user import User
from fastapi import APIRouter, Depends, UploadFile, File
from backend.app.   services.user_service import UserService
from backend.app.models.user import User
import os
import aiofiles
import uuid


from backend.app.models.user import User
from backend.app.common.jwt import CurrentUser, DependsJwtUser, get_current_user
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.user import CreateUser,UserInfo,Auth,GetUserInfo, ResetPassword, UpdateUser, UpdateUserRole, UpdateTeacherRole
from backend.app.services.user_service import UserService
from backend.app.common.exception.errors import CustomError
from backend.app.models.teacher import Teacher
from typing import Dict
from backend.app.schemas.user import PasswordResetRequest

router = APIRouter()


@router.post("/register", summary="用户注册")
async def register(user_data: CreateUser):
    """
    用户注册接口
    - username: 用户名
    - password: 密码
    - confirmPassword: 确认密码
    - sno: 学号
    - department: 学院
    - major: 专业
    - grade: 年级
    - class_name: 班级
    """
    return await UserService.register(user_data)

@router.get('/getInfo', summary='获取用户信息')
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    try:
        print("开始获取用户信息, token用户:", current_user)
        user_info = await UserService.get_user_info(current_user)
        print("获取到的用户信息:", user_info)
        return await response_base.success(data=user_info)
    except Exception as e:
        print("获取用户信息错误:", str(e))
        return await response_base.fail(msg=str(e))


@router.get('/getAllInfo', summary='获取所有用户信息')
async def get_all_user_info(page: int = 1, page_size: int = 10):
    """
    获取所有用户信息（分页）
    :param page: 页码，默认1
    :param page_size: 每页数量，默认10
    """
    print(f"接收到的分页参数 - page: {page}, page_size: {page_size}")
    data = await UserService.get_all_user_info(page, page_size)
    return await response_base.success(data=data)

@router.get('/getAllStudentInfo',summary="获取所有学生信息")
async def get_all_student_info(page: int = 1, page_size: int = 10):
    """
    获取所有学生信息（分页）
    :param page: 页码，默认1
    :param page_size: 每页数量，默认10
    """
    print(f"接收到的分页参数 - page: {page}, page_size: {page_size}")
    data=await UserService.get_all_student_info(page,page_size)
    return await response_base.success(data=data)

@router.get('/getAllTeacherInfo',summary="获取所有老师信息")
async def get_all_teacher_info(page: int = 1, page_size: int = 10):
    """
    获取所有老师信息（分页）
    :param page: 页码，默认1
    :param page_size: 每页数量，默认10
    """
    print(f"接收到的分页参数 - page: {page}, page_size: {page_size}")
    data=await UserService.get_all_teacher_info(page,page_size)
    return await response_base.success(data=data)

@router.get('/getRoutes', summary='获取用户路由权限')
async def get_user_routes(current_user: User = Depends(get_current_user)):
    """获取当前用户的路由权限"""
    try:
        # 根据用户角色返回对应的路由权限
        routes = {
            'admin': [
                "0", "1", "12", "13","14", "5","51","52","53","7","13","131","151","171"
            ],
            'teacher': ["0","3","31","32","33","34","7","16","161","162","151"],
            'student': ["0", "8","81","82","7","9","91","92","11",'111',"112","151"]        }
        
        # 获取用户角色
        user_role = current_user.roles  # 假设用户模型中有role字段
        
        return await response_base.success(
            data={
                'routes': routes.get(user_role, [])  # 如果角色不存在返回空列表
            }
        )
    except Exception as e:
        print("获取路由权限错误:", str(e))
        return await response_base.fail(msg=str(e))


@router.get('/get_all_teachers_name', summary="获取所有教师姓名列表")
async def get_all_teachers_name(current_user: User = Depends(get_current_user)):
    """获取所有教师姓名列表"""
    try:
       
        teachers = await Teacher.all().values('id', 'name')
        return await response_base.success(data=teachers)
    except Exception as e:
        print(f"获取教师姓名列表失败: {str(e)}")
        return await response_base.fail(msg=f"获取教师姓名列表失败: {str(e)}")

@router.put("/update")
async def update_user_role(user_data: UpdateUserRole):
    """更新用户角色"""
    print("1111",user_data)
    count = await UserService.update_user_role(user_data.id, user_data.roles)
    return await response_base.success(data=count, msg="更新角色成功")

@router.put("/updateTeacherRole")
async def update_teacher_role(teacher_data: UpdateTeacherRole):
    """更新教师角色和信息"""
    try:
        result = await UserService.update_user_with_role_change(
            user_id=teacher_data.id,
            roles=teacher_data.roles,
            teacher_data={
                "department": teacher_data.department,
                "major": teacher_data.major,
                "title": teacher_data.title,
                "name":teacher_data.name
            }
        )
        return await response_base.success(data=result, msg="更新成功")
    except Exception as e:
        return await response_base.fail(msg=f"更新失败: {str(e)}")

@router.post('/password/reset/code', summary='获取密码重置验证码', description='可以通过用户名或者邮箱重置密码')
async def password_reset_captcha(username_or_email: str, response: Response):
    await UserService.get_pwd_rest_captcha(username_or_email=username_or_email, response=response)
    return await response_base.success(msg='验证码发送成功')


@router.post('/password/reset', summary='密码重置请求')
async def password_reset(obj: ResetPassword, request: Request, response: Response):
    await UserService.pwd_reset(obj=obj, request=request, response=response)
    return await response_base.success(msg='密码重置成功')


@router.get('/password/reset/done', summary='重置密码完成')
async def password_reset_done():
    return await response_base.success(msg='重置密码完成')


@router.get('/{username}', summary='查看用户信息', dependencies=[DependsJwtUser])
async def get_user_info(username: str):
    current_user = await UserService.get_user_info(username)
    return await response_base.success(data=current_user, exclude={'password'})


@router.put('/{username}', summary='更新用户信息')
async def update_userinfo(username: str, obj: UpdateUser, current_user: CurrentUser):
    count = await UserService.update(username=username, current_user=current_user, obj=obj)
    if count > 0:
        return await response_base.success(msg='更新用户信息成功')
    return await response_base.fail()


@router.put('/{username}/avatar', summary='更新头像')
async def update_avatar(username: str, avatar: UploadFile, current_user: CurrentUser):
    count = await UserService.update_avatar(username=username, current_user=current_user, avatar=avatar)
    if count > 0:
        return await response_base.success(msg='更新头像成功')
    return await response_base.fail()


@router.delete('/{username}/avatar', summary='删除头像文件')
async def delete_avatar(username: str, current_user: CurrentUser):
    count = await UserService.delete_avatar(username=username, current_user=current_user)
    if count > 0:
        return await response_base.success(msg='删除用户头像成功')
    return await response_base.fail()


@router.get('', summary='获取所有用户', dependencies=[DependsJwtUser, DependsPagination])
async def get_all_users():
    data = await UserService.get_user_list()
    page_data = await paging_data(data, GetUserInfo)
    return await response_base.success(data=page_data)


@router.post('/{pk}/super', summary='修改用户超级权限', dependencies=[DependsJwtUser])
async def super_set(pk: int):
    count = await UserService.update_permission(pk)
    if count > 0:
        return await response_base.success(msg='修改超级权限成功')
    return await response_base.fail()


@router.post('/{pk}/action', summary='修改用户状态', dependencies=[DependsJwtUser])
async def status_set(pk: int):
    count = await UserService.update_status(pk)
    if count > 0:
        return await response_base.success(msg='修改用户状态成功')
    return await response_base.fail()


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    try:
        count = await UserService.delete_user(user_id)
        if count == 0:
            return await response_base.fail(msg="用户不存在")
        return await response_base.success(msg="删除成功")
    except Exception as e:
        return await response_base.fail(msg=f"删除失败: {str(e)}")


@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    上传用户头像
    """
    try:
        # 检查文件类型
        if not file.content_type in ["image/jpeg", "image/png"]:
            return {"code": 400, "message": "只支持 JPG/PNG 格式的图片"}

        # 读取文件内容
        content = await file.read()
        
        # 检查文件大小（限制为2MB）
        if len(content) > 2 * 1024 * 1024:
            return {"code": 400, "message": "文件大小不能超过2MB"}

        # 生成文件名
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        
        # 确保上传目录存在
        upload_dir = "static/avatars"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_dir, filename)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
            
        # 更新用户头像信息
        avatar_url = f"/static/avatars/{filename}"
        await UserService.update_avatar(current_user.id, avatar_url)
        
        return {
            "code": 200,
            "message": "头像上传成功",
            "data": {
                "url": avatar_url
            }
        }
    except Exception as e:
        return {"code": 500, "message": f"头像上传失败: {str(e)}"} 
@router.post("/password/reset")
async def reset_password(
    password_data: PasswordResetRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """
    重置用户密码
    """
    try:
        await UserService.reset_password(
            user_id=current_user.id,
            old_password=password_data.old,
            new_password=password_data.new
        )
        return {"code": 200, "message": "密码修改成功"}
    except ValueError as e:
        return {"code": 500, "message": f"头像上传失败: {str(e)}"} 
    except Exception as e:
        return {"code": 500, "message": f"头像上传失败: {str(e)}"} 







