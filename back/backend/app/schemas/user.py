#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from email_validator import EmailNotValidError, validate_email
from pydantic import UUID4, ConfigDict, EmailStr, field_validator, BaseModel

from backend.app.schemas.base import SchemaBase


class Auth(SchemaBase):
    username: str
    password: str


class UserInfo(SchemaBase):
    username: str
    roles:str
    uuid:str
    joined_time:str
    last_login_time:str
    id:int
    password:str

class Auth2(Auth):
    captcha_code: str


class CreateUser(SchemaBase):
    username: str
    password: str
    confirmPassword: str

class UserInfo(SchemaBase):
    username: str
    uuid:str

class UpdateUser(SchemaBase):
    username: str
    email: str
    phone: str | None = None

    @field_validator('email')
    @classmethod
    def email_validate(cls, v: str):
        try:
            validate_email(v, check_deliverability=False).email
        except EmailNotValidError:
            raise ValueError('邮箱格式错误')
        return v


class GetUserInfo(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID4
    username: str
    email: EmailStr
    status: int
    is_superuser: bool
    avatar: str | None = None
    phone: str | None = None
    joined_time: datetime.datetime
    last_login_time: datetime.datetime | None = None


class ResetPassword(SchemaBase):
    code: str
    password1: str
    password2: str


class UpdateUserRole(SchemaBase):
    """更新用户角色请求体"""
    id: str
    roles: str
