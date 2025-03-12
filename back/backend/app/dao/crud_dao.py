#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tortoise import timezone
from tortoise.transactions import atomic

from backend.app.common import jwt
from backend.app.dao.base import DaoBase
from backend.app.models.user import User
from backend.app.schemas.user import CreateUser, UpdateUser
from backend.app.common.exception.errors import CustomError
from backend.app.models.student import Student


class UserDao(DaoBase[User, CreateUser, UpdateUser]):
    async def get_user_by_id(self, pk: int) -> User:
        print(f"正在查询用户ID: {pk}")
        return await self.get(pk)

    async def get_user_by_username(self, name: str) -> User:
        return await self.model.filter(username=name).first()
    
    async def get_all_user_info(self):
        return await self.model.all()

    @atomic()
    async def update_user_login_time(self, pk: int) -> int:
        return await self.model.filter(id=pk).update(last_login_time=timezone.now())

    async def check_email(self, email: str) -> bool:
        return await self.model.filter(email=email).exists()

    @atomic()
    async def register_user(self, user: CreateUser) -> User:
        user.password = await jwt.get_hash_password(user.password)
        user = await self.create(user)
        return user

    async def get_email_by_username(self, username: str) -> str:
        user = await self.model.filter(username=username).first()
        return user.email

    async def get_username_by_email(self, email: str) -> str:
        user = await self.model.filter(email=email).first()
        return user.username

    async def get_avatar_by_username(self, username: str) -> str:
        user = await self.get_user_by_username(username)
        return user.avatar

    @atomic()
    async def reset_password(self, username: str, password: str) -> int:
        new_password = await jwt.get_hash_password(password)
        return await self.model.filter(username=username).update(password=new_password)

    @atomic()
    async def update_userinfo(self, current_user: User, obj_in: UpdateUser) -> int:
        return await self.update(current_user.pk, obj_in)

    @atomic()
    async def update_avatar(self, current_user: User, avatar: str):
        return await self.update(current_user.pk, {'avatar': avatar})

    async def get_avatar_by_pk(self, pk: int):
        user = await self.get(pk)
        return user.avatar

    @atomic()
    async def delete_avatar(self, pk: int) -> int:
        return await self.model.filter(id=pk).update(avatar=None)

    async def get_user_super_status(self, pk: int) -> bool:
        user = await self.get(pk)
        return user.is_superuser

    async def get_user_active_status(self, pk: int) -> bool:
        user = await self.get(pk)
        return user.status

    @atomic()
    async def super_set(self, pk: int) -> int:
        super_status = await self.get_user_super_status(pk)
        return await self.model.filter(id=pk).update(is_superuser=False if super_status else True)

    @atomic()
    async def status_set(self, pk: int) -> int:
        status = await self.get_user_active_status(pk)
        return await self.model.filter(id=pk).update(status=False if status else True)

    @atomic()
    async def delete_user(self, pk: int) -> int:
        return await self.delete(pk)

    async def get_user_count(self) -> int:
        """获取用户总数"""
        return await self.model.all().count()
    
    async def get_user_page(self, offset: int, limit: int):
        """获取分页用户数据"""
        return await self.model.all().offset(offset).limit(limit)

    @staticmethod
    async def update_user_role(user_id: int, update_data: dict):
        """更新用户角色和相关信息"""
        try:
            return await User.filter(id=user_id).update(**update_data)
        except Exception as e:
            raise CustomError(f"更新用户角色失败: {str(e)}")
    
    @staticmethod
    async def get_user_by_sno(sno: str):
        """通过学号获取用户"""
        return await User.filter(sno=sno).first()

    @staticmethod
    @atomic()
    async def create_user_with_student(user_data: dict) -> User:
        """创建用户并关联学生信息"""
        try:
            # 创建用户
            hashed_password = await jwt.get_hash_password(user_data["password"])
            user = await User.create(
                username=user_data["username"],
                password=hashed_password,
                sno=user_data["sno"],
                roles="student"
            )
            
            # 创建学生信息
            await Student.create(
                sno=user_data["sno"],
                name=user_data["username"],
                department=user_data["department"],
                major=user_data["major"],
                grade=user_data["grade"],
                class_name=user_data["class_name"],
                user_id=user.id  # 直接存储用户ID
            )
            
            return user
        except Exception as e:
            print("创建用户失败:", str(e))
            raise CustomError(f"创建用户失败: {str(e)}")

UserDao: UserDao = UserDao(User)