#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from distutils import errors
from typing import Any

from asgiref.sync import sync_to_async
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from typing_extensions import Annotated

from backend.app.common.exception.errors import AuthorizationError, TokenError
from backend.app.core.conf import Settings
from backend.app.dao.crud_dao import UserDao
from backend.app.models.user import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl=Settings.TOKEN_URL_SWAGGER)


@sync_to_async
def get_hash_password(password: str) -> str:
    """
    使用hash算法加密密码

    :param password: 密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


@sync_to_async
def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    密码校验

    :param plain_password: 要验证的密码
    :param hashed_password: 要比较的hash密码
    :return: 比较密码之后的结果
    """
    return pwd_context.verify(plain_password, hashed_password)


@sync_to_async
def create_access_token(data: int | Any, expires_delta: timedelta | None = None) -> str:
    """
    生成加密 token
    """
    try:
        # 1. 确保data是字符串格式
        if isinstance(data, int):
            data = str(data)
            
        # 2. 设置token过期时间
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=Settings.TOKEN_EXPIRE_MINUTES)
            
        # 构建payload
        to_encode = {
            'exp': expire,
            'sub': data,
            'iat': datetime.utcnow()
        }
        
        print("Token payload:", to_encode)  # 添加日志
        
        # 生成token
        encoded_jwt = jwt.encode(
            to_encode,
            Settings.TOKEN_SECRET_KEY,
            algorithm=Settings.TOKEN_ALGORITHM
        )
        
        return encoded_jwt
    except Exception as e:
        print("Token生成错误:", str(e))
        raise errors.AuthorizationError(msg=f"Token生成失败: {str(e)}")


async def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    """通过token获取当前用户"""
    try:
        print("接收到的token:", token)  # 添加token日志
    
        
        # 解密token
        payload = jwt.decode(token, Settings.TOKEN_SECRET_KEY, algorithms=[Settings.TOKEN_ALGORITHM])
        user_id = payload.get('sub')
        
        print("解析出的user_id:", user_id)  # 添加user_id日志
        
        if not user_id:
            raise TokenError("无效的token")
            
        user = await UserDao.get_user_by_id(user_id)
        print("查询到的用户:", user)  # 添加用户日志
        
        if not user:
            raise TokenError("用户不存在")
            
        return user
    except jwt.JWTError as e:
        print("Token验证错误:", str(e))
        # 修改这里的错误抛出方式
        raise TokenError(message=str(e))  # 确保使用正确的参数名
    except Exception as e:
        print("其他错误:", str(e))
        raise TokenError(message=str(e))


@sync_to_async
def superuser_verify(user: User):
    """
    验证当前用户是否为超级用户

    :param user:
    :return:
    """
    is_superuser = user.is_superuser
    if not is_superuser:
        raise AuthorizationError
    return is_superuser


# 用户依赖注入
CurrentUser = Annotated[User, Depends(get_current_user)]
# 权限依赖注入
DependsJwtUser = Depends(get_current_user)


