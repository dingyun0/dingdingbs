#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tortoise import Model, fields

from backend.app.utils.generate_string import get_uuid4_str


class User(Model):
    """
    用户类
    """

    id = fields.BigIntField(pk=True, index=True, description='主键id')
    uuid = fields.CharField(max_length=36, default=get_uuid4_str, unique=True, description='用户UID')
    username = fields.CharField(max_length=32, unique=True, description='用户名')
    password = fields.CharField(max_length=255, description='密码')
    roles = fields.CharField(max_length=255, default="student", description='角色')
    sno = fields.CharField(max_length=50, null=True, unique=True, description='学号')
    joined_time = fields.DatetimeField(auto_now_add=True, description='注册时间')
    last_login_time = fields.DatetimeField(null=True, description='上次登录时间')

    def __str__(self):
        """定义模型的字符串表示"""
        return f"User(id={self.id}, username='{self.username}')"

    def __repr__(self):
        return (
            f"User("
            f"id={self.id}, "
            f"username='{self.username}', "
            f"roles={self.roles}, "
            f"joined_time='{self.joined_time}', "
            f"last_login_time='{self.last_login_time}'"
            f")"
        )
    class Meta:
        table = 'user'
        table_description = "用户表"

