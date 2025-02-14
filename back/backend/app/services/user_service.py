#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from hashlib import sha256

from email_validator import EmailNotValidError, validate_email
from fast_captcha import text_captcha
from fastapi import HTTPException, Request, Response, UploadFile
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.common import jwt
from backend.app.common.exception import errors
from backend.app.common.jwt import superuser_verify
from backend.app.common.log import log
from backend.app.common.redis import redis_client
from backend.app.common.response.response_code import CustomCode
from backend.app.core.conf import Settings
from backend.app.core.path_conf import AvatarPath
from backend.app.dao.crud_dao import UserDao  # 导入单例实例
from backend.app.models.user import User
from backend.app.schemas.user import (Auth, Auth2, CreateUser, ResetPassword,
                                      UpdateUser)
from backend.app.utils import re_verify
from backend.app.utils.format_string import cut_path
from backend.app.utils.generate_string import get_current_timestamp
from backend.app.utils.send_email import send_verification_code_email


class UserService:
    @staticmethod
    async def login_swagger(form_data: OAuth2PasswordRequestForm):
        user = await UserService.user_verify(form_data.username, form_data.password)
        await UserDao.update_user_login_time(user.pk)
        access_token = await jwt.create_access_token(user.pk)
        return access_token, user

    @staticmethod
    async def user_verify(username: str, password: str):
        print("正在验证用户:", username)
        user = await UserDao.get_user_by_username(username)
        if not user:
            raise errors.NotFoundError(msg='用户名不存在')
        elif not await jwt.password_verify(password, user.password):
            raise errors.AuthorizationError(msg='密码错误')
        return user


    @staticmethod
    async def login_json(obj: Auth):
        """用户登录"""
        user = await UserService.user_verify(obj.username, obj.password)
        if not user:
            raise errors.AuthorizationError(msg='用户名或密码错误')
        
        # 生成token
        access_token = await jwt.create_access_token(user.pk)
        return access_token, user
    
    @staticmethod
    async def get_all_user_info(page: int = 1, page_size: int = 10):
        """获取所有用户信息（分页）"""
        try:
            # 计算偏移量
            offset = (page - 1) * page_size
            print(f"分页参数 - 页码: {page}, 每页条数: {page_size}, 偏移量: {offset}")
            
            # 获取总数
            total = await UserDao.get_user_count()
            print(f"总记录数: {total}")
            
            # 使用 UserDao 获取分页后的用户
            users = await UserDao.get_user_page(offset, page_size)
            
            # 将用户对象转换为字典列表
            user_list = []
            for user in users:
                user_dict = {
                    'id': str(user.id),
                    'username': str(user.username),
                    'roles': str(user.roles),
                    'joined_time': user.joined_time.strftime('%Y-%m-%d %H:%M:%S') if user.joined_time else None,
                    'last_login_time': user.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if user.last_login_time else None,
                    'uuid': str(user.uuid)
                }
                user_list.append(user_dict)
            
            result = {
                'list': user_list,
                'total': total,
                'page': page,
                'page_size': page_size
            }
            print(f"返回的分页数据: {result}")
            return result
        
        except Exception as e:
            print("获取所有用户信息错误:", str(e))
            raise errors.CustomError(msg=f'获取用户信息失败: {str(e)}')

    @staticmethod
    async def login_captcha(*, obj: Auth2, request: Request):
        user = await UserService.user_verify(obj.username, obj.password)
        try:
            redis_code = await redis_client.get(obj.uuid)
            if not redis_code:
                raise errors.ForbiddenError(msg='验证码失效，请重新获取')
            if redis_code.lower() != obj.captcha_code.lower():
                raise errors.CustomError(error=CustomCode.CAPTCHA_ERROR)
        except AttributeError:
            raise errors.ForbiddenError(msg='验证码失效，请重新获取')
        
        await UserDao.update_user_login_time(user.pk)
        access_token = await jwt.create_access_token(user.pk)
        return access_token, user

    @staticmethod
    async def register(obj: CreateUser):
        """用户注册"""
        try:
            # 验证验证码
            # redis_code = await redis_client.get(f'captcha:{obj.uuid}')
            # if not redis_code:
            #     raise errors.ForbiddenError(msg='验证码失效，请重新获取')
            # if redis_code.lower() != obj.code.lower():
            #     raise errors.CustomError(error=CustomCode.CAPTCHA_ERROR)
            
            # 验证用户名是否已存在
            username = await UserDao.get_user_by_username(name=obj.username)
            if username:
                raise errors.ForbiddenError(msg='该用户名已被注册')
            
            # 验证两次密码是否一致
            # if obj.password != obj.confirmPassword:
            #     raise errors.ForbiddenError(msg='两次输入的密码不一致')
            
            # 注册用户
            await UserDao.register_user(obj)
            
        except Exception as e:
            raise errors.ForbiddenError(msg=str(e))

    @staticmethod
    async def get_pwd_rest_captcha(*, username_or_email: str, response: Response):
        code = text_captcha()
        if await UserDao.get_user_by_username(username_or_email):
            try:
                response.delete_cookie(key='fastapi_reset_pwd_code')
                response.delete_cookie(key='fastapi_reset_pwd_username')
                response.set_cookie(
                    key='fastapi_reset_pwd_code',
                    value=sha256(code.encode('utf-8')).hexdigest(),
                    max_age=Settings.COOKIES_MAX_AGE,
                )
                response.set_cookie(
                    key='fastapi_reset_pwd_username', value=username_or_email, max_age=Settings.COOKIES_MAX_AGE
                )
            except Exception as e:
                log.exception('无法发送验证码 {}', e)
                raise e
            current_user_email = await UserDao.get_email_by_username(username_or_email)
            await send_verification_code_email(current_user_email, code)
        else:
            try:
                validate_email(username_or_email, check_deliverability=False)
            except EmailNotValidError:
                raise HTTPException(status_code=404, detail='用户名不存在')
            email_result = await UserDao.check_email(username_or_email)
            if not email_result:
                raise HTTPException(status_code=404, detail='邮箱不存在')
            try:
                response.delete_cookie(key='fastapi_reset_pwd_code')
                response.delete_cookie(key='fastapi_reset_pwd_username')
                response.set_cookie(
                    key='fastapi_reset_pwd_code',
                    value=sha256(code.encode('utf-8')).hexdigest(),
                    max_age=Settings.COOKIES_MAX_AGE,
                )
                username = await UserDao.get_username_by_email(username_or_email)
                response.set_cookie(key='fastapi_reset_pwd_username',
                                    value=username, max_age=Settings.COOKIES_MAX_AGE)
            except Exception as e:
                log.exception('无法发送验证码 {}', e)
                raise e
            await send_verification_code_email(username_or_email, code)

    @staticmethod
    async def pwd_reset(*, obj: ResetPassword, request: Request, response: Response):
        pwd1 = obj.password1
        pwd2 = obj.password2
        cookie_reset_pwd_code = request.cookies.get('fastapi_reset_pwd_code')
        cookie_reset_pwd_username = request.cookies.get(
            'fastapi_reset_pwd_username')
        if pwd1 != pwd2:
            raise errors.ForbiddenError(msg='两次密码输入不一致')
        if cookie_reset_pwd_username is None or cookie_reset_pwd_code is None:
            raise errors.NotFoundError(msg='验证码已失效，请重新获取')
        if cookie_reset_pwd_code != sha256(obj.code.encode('utf-8')).hexdigest():
            raise errors.ForbiddenError(msg='验证码错误')
        await UserDao.reset_password(cookie_reset_pwd_username, obj.password2)
        response.delete_cookie(key='fastapi_reset_pwd_code')
        response.delete_cookie(key='fastapi_reset_pwd_username')

    @staticmethod
    async def get_user_info(user: User):
        """获取用户信息"""
        try:
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            
            # 返回用户信息(排除敏感字段)
            user_info = {
                'id': user.id,
                'username': user.username,
                'roles': user.roles,
                'joined_time': user.joined_time.strftime('%Y-%m-%d %H:%M:%S') if user.joined_time else None,
                'last_login_time': user.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if user.last_login_time else None
            }
            print("返回的用户信息:", user_info)
            return user_info
        except Exception as e:
            print("获取用户信息错误:", str(e))
            raise errors.AuthorizationError(msg=f'获取用户信息失败: {str(e)}')

    @staticmethod
    async def update(*, username: str, current_user: User, obj: UpdateUser):
        await superuser_verify(current_user)
        input_user = await UserDao.get_user_by_username(username)
        if not input_user:
            raise errors.NotFoundError(msg='用户不存在')
        if input_user.username != obj.username:
            username = await UserDao.get_user_by_username(obj.username)
            if username:
                raise errors.ForbiddenError(msg='该用户名已存在')
        if input_user.email != obj.email:
            _email = await UserDao.check_email(obj.email)
            if _email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
        if obj.phone is not None:
            if not re_verify.is_phone(obj.phone):
                raise errors.ForbiddenError(msg='手机号码输入有误')
        count = await UserDao.update_userinfo(input_user, obj)
        return count

    @staticmethod
    async def update_avatar(*, username: str, current_user: User, avatar: UploadFile):
        await superuser_verify(current_user)
        input_user = await UserDao.get_user_by_username(username)
        if not input_user:
            raise errors.NotFoundError(msg='用户不存在')
        input_user_avatar = input_user.avatar
        if avatar is not None:
            if input_user_avatar is not None:
                try:
                    os.remove(AvatarPath + input_user_avatar)
                except Exception as e:
                    log.error('用户 {} 更新头像时，原头像文件 {} 删除失败\n{}',
                              username, input_user_avatar, e)
            new_file = avatar.file.read()
            if 'image' not in avatar.content_type:
                raise errors.ForbiddenError(msg='图片格式错误，请重新选择图片')
            file_name = str(get_current_timestamp()) + '_' + avatar.filename
            if not os.path.exists(AvatarPath):
                os.makedirs(AvatarPath)
            with open(AvatarPath + f'{file_name}', 'wb') as f:
                f.write(new_file)
        else:
            file_name = input_user_avatar
        count = await UserDao.update_avatar(input_user, file_name)
        return count

    @staticmethod
    async def delete_avatar(*, username: str, current_user: User):
        await superuser_verify(current_user)
        input_user = await UserDao.get_user_by_username(username)
        if not input_user:
            raise errors.NotFoundError(msg='用户不存在')
        input_user_avatar = input_user.avatar
        if input_user_avatar is not None:
            try:
                os.remove(AvatarPath + input_user_avatar)
            except Exception as e:
                log.error('用户 {} 删除头像文件 {} 失败\n{}',
                          input_user.username, input_user_avatar, e)
        else:
            raise errors.NotFoundError(msg='用户没有头像文件，请上传头像文件后再执行此操作')
        count = await UserDao.delete_avatar(input_user.id)
        return count

    # @staticmethod
    # async def get_user_list():
    #     data = await UserDao.get_all()
    #     return data.order_by('-id')

    @staticmethod
    async def update_permission(pk: int):
        user = await UserDao.get_user_by_id(pk)
        if user:
            await superuser_verify(user)
            count = await UserDao.super_set(pk)
            return count
        else:
            raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def update_status(pk: int):
        user = await UserDao.get_user_by_id(pk)
        if user:
            await superuser_verify(user)
            count = await UserDao.status_set(pk)
            return count
        else:
            raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def delete(*, username: str, current_user: User):
        await superuser_verify(current_user)
        input_user = await UserDao.get_user_by_username(username)
        if not input_user:
            raise errors.NotFoundError(msg='用户不存在')
        input_user_avatar = input_user.avatar
        try:
            if input_user_avatar is not None:
                os.remove(AvatarPath + input_user_avatar)
        except Exception as e:
            log.error(f'删除用户 {input_user.username}  \
                    头像文件:{input_user_avatar} 失败\n{e}')
        finally:
            count = await UserDao.delete_user(input_user.id)
            return count

    @staticmethod
    async def get_user_routes(current_user: User):
        """根据用户角色返回对应的路由配置"""
        roles = current_user.roles  # 假设用户模型中有role字段
        print("当前用户角色:", roles)
        
        # 基础路由配置
        base_routes = {
            "personal": {
                "path": "/personal",
                "component": "Layout",
                "redirect": "/personal/info",
                "name": "Personal",
                "meta": {"title": "个人中心", "icon": "user"},
                "children": [
                    {
                        "path": "password",
                        "component": "personal/password",
                        "name": "Password",
                        "meta": {"title": "修改密码"}
                    },
                    {
                        "path": "info",
                        "component": "personal/info", 
                        "name": "PersonalInfo",
                        "meta": {"title": "个人信息"}
                    }
                ]
            }
        }
        
        # 学生特有路由
        student_routes = {
            "notice": {
                "path": "/notice",
                "component": "Layout",
                "name": "Notice",
                "meta": {"title": "公告管理", "icon": "message"},
                "children": [
                    {
                        "path": "school",
                        "component": "notice/school",
                        "name": "SchoolNotice",
                        "meta": {"title": "学校公告"}
                    },
                    {
                        "path": "scholarship",
                        "component": "notice/scholarship",
                        "name": "ScholarshipNotice", 
                        "meta": {"title": "奖学金公告"}
                    }
                ]
            },
            "activity": {
                "path": "/activity",
                "component": "Layout",
                "name": "Activity",
                "meta": {"title": "活动管理", "icon": "calendar"},
                "children": [
                    {
                        "path": "list",
                        "component": "activity/list",
                        "name": "ActivityList",
                        "meta": {"title": "活动列表"}
                    },
                    {
                        "path": "apply",
                        "component": "activity/apply",
                        "name": "ActivityApply",
                        "meta": {"title": "活动申请"}
                    }
                ]
            },
            "score": {
                "path": "/score",
                "component": "Layout",
                "name": "Score",
                "meta": {"title": "成绩管理", "icon": "chart"},
                "children": [
                    {
                        "path": "view",
                        "component": "score/view",
                        "name": "ScoreView",
                        "meta": {"title": "查看成绩"}
                    },
                    {
                        "path": "modify",
                        "component": "score/modify",
                        "name": "ScoreModify",
                        "meta": {"title": "申请修改"}
                    }
                ]
            }
        }
        
        # 教师特有路由
        teacher_routes = {
            "activity": {
                "path": "/activity",
                "component": "Layout",
                "name": "Activity",
                "meta": {"title": "活动管理", "icon": "calendar"},
                "children": [
                    {
                        "path": "review",
                        "component": "activity/review",
                        "name": "ActivityReview",
                        "meta": {"title": "活动审核"}
                    }
                ]
            },
            "score": {
                "path": "/score",
                "component": "Layout",
                "name": "Score",
                "meta": {"title": "成绩管理", "icon": "chart"},
                "children": [
                    {
                        "path": "import",
                        "component": "score/import",
                        "name": "ScoreImport",
                        "meta": {"title": "导入成绩"}
                    },
                    {
                        "path": "export",
                        "component": "score/export",
                        "name": "ScoreExport",
                        "meta": {"title": "导出成绩"}
                    },
                    {
                        "path": "review",
                        "component": "score/review",
                        "name": "ScoreReview",
                        "meta": {"title": "成绩审核"}
                    }
                ]
            }
        }
        
        # 管理员特有路由
        admin_routes = {
            "activity": {
                "path": "/activity",
                "component": "Layout",
                "name": "Activity",
                "meta": {"title": "活动管理", "icon": "calendar"},
                "children": [
                    {
                        "path": "publish",
                        "component": "activity/publish",
                        "name": "ActivityPublish",
                        "meta": {"title": "发布活动"}
                    }
                ]
            },
            "user": {
                "path": "/user",
                "component": "Layout",
                "name": "User",
                "meta": {"title": "用户管理", "icon": "user"},
                "children": [
                    {
                        "path": "teacher",
                        "component": "user/teacher",
                        "name": "TeacherManage",
                        "meta": {"title": "教师管理"}
                    },
                    {
                        "path": "student",
                        "component": "user/student",
                        "name": "StudentManage",
                        "meta": {"title": "学生管理"}
                    }
                ]
            },
            "notice": {
                "path": "/notice",
                "component": "Layout",
                "name": "Notice",
                "meta": {"title": "公告管理", "icon": "message"},
                "children": [
                    {
                        "path": "school/publish",
                        "component": "notice/school-publish",
                        "name": "SchoolNoticePublish",
                        "meta": {"title": "发布学校公告"}
                    },
                    {
                        "path": "scholarship/publish",
                        "component": "notice/scholarship-publish",
                        "name": "ScholarshipNoticePublish",
                        "meta": {"title": "发布奖学金公告"}
                    }
                ]
            }
        }
        
        # 根据角色返回对应路由
        routes = [base_routes]
        if roles == "student":
            routes.extend([student_routes])
        elif roles == "teacher":
            routes.extend([teacher_routes])
        elif roles == "admin":
            routes.extend([admin_routes])
        
        return routes
                        
    @staticmethod
    async def update_user(user_id: int, user_data: dict):
        """更新用户信息"""
        try:
            user = await UserDao.get_user_by_id(user_id)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            
            count = await UserDao.update(user_id, user_data)
            return count
        except Exception as e:
            print("更新用户信息错误:", str(e))
            raise errors.CustomError(msg=f'更新用户信息失败: {str(e)}')

    @staticmethod
    async def get_user_detail(user_id: int):
        """获取用户详情"""
        try:
            user = await UserDao.get_user_by_id(user_id)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            
            return {
                'id': str(user.id),
                'username': str(user.username),
                'roles': str(user.roles),
                'joined_time': user.joined_time.strftime('%Y-%m-%d %H:%M:%S') if user.joined_time else None,
                'last_login_time': user.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if user.last_login_time else None
            }
        except Exception as e:
            print("获取用户详情错误:", str(e))
            raise errors.CustomError(msg=f'获取用户详情失败: {str(e)}')

    @staticmethod
    async def update_user_role(user_id: int, roles: str):
        """更新用户角色"""
        try:
            # 验证角色是否合法
            valid_roles = ["admin", "teacher", "student"]
            if roles not in valid_roles:
                raise errors.ValidationError(msg=f"无效的角色值: {roles}")
            
            # 检查用户是否存在
            user = await UserDao.get_user_by_id(user_id)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            
            # 更新角色
            count = await UserDao.update_user_role(user_id, roles)
            print("222",count)
            if count == 0:
                raise errors.UpdateError(msg='更新角色失败')
            
            return count
        except Exception as e:
            print("更新用户角色错误:", str(e))
            raise errors.CustomError(msg=f'更新用户角色失败: {str(e)}')

    @staticmethod
    async def delete_user(user_id: int) -> int:
        """删除用户"""
        try:
            # 检查用户是否存在
            user = await UserDao.get_user_by_id(user_id)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            
            # 删除用户
            count = await UserDao.delete_user(user_id)
            if count == 0:
                raise errors.DeleteError(msg='删除用户失败')
            
            return count
        except Exception as e:
            print("删除用户错误:", str(e))
            raise errors.CustomError(msg=f'删除用户失败: {str(e)}')
                        
