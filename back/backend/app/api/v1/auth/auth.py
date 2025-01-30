#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.common.jwt import DependsJwtUser
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.token import Token
from backend.app.schemas.user import Auth, Auth2
from backend.app.services.user_service import UserService
from backend.app.dao.crud_dao import UserDao
from backend.app.common.exception import errors
from backend.app.common.response.response_code import CustomCode
from backend.app.common.redis import redis_client

router = APIRouter()




@router.post('/login', summary='用户登录')
async def login(obj: Auth, request: Request):
    try:
        # 验证验证码
        # redis_code = await redis_client.get(f'captcha:{obj.uuid}')
        # if not redis_code:
        #     raise errors.ForbiddenError(msg='验证码失效，请重新获取')
        # if redis_code.lower() != obj.code.lower():
        #     raise errors.CustomError(error=CustomCode.CAPTCHA_ERROR)
            
        # 验证用户名密码
        token, user = await UserService.login_json(obj)
        
        # 更新登录时间
        await UserDao.update_user_login_time(user.pk)
        
        return await response_base.success(
            data={
                'token': token,
                'user': user
            }
        )
    except Exception as e:
        raise errors.AuthorizationError(msg=str(e))




@router.post('/logout', summary='登出', dependencies=[DependsJwtUser])
async def user_logout():
    return await response_base.response_200()
