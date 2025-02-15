#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request, Response, UploadFile
# from backend.app.models.user import User


from backend.app.models.announcement import Announcement
from backend.app.common.jwt import CurrentUser, DependsJwtUser, get_current_user
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.response.response_schema import response_base

from backend.app.services.user_service import UserService
from backend.app.services.announcement_service import AnnouncementService
from backend.app.schemas.announcement import CreateAnnouncement, UpdateAnnouncement

router = APIRouter()


@router.post("/add")
async def add_announcement(announcement: CreateAnnouncement):
    """添加公告"""
    result = await AnnouncementService.add_announcement(announcement)
    return await response_base.success(data=result, msg="添加公告成功")

@router.put("/update")
async def update_announcement(announcement: UpdateAnnouncement):
    """更新公告"""
    result = await AnnouncementService.update_announcement(announcement)
    return await response_base.success(data=result, msg="更新公告成功")

@router.delete("/delete/{id}")
async def delete_announcement(id: int):
    """删除公告"""
    result = await AnnouncementService.delete_announcement(id)
    return await response_base.success(data=result, msg="删除公告成功")

@router.get("/list")
async def get_announcement_list(page: int = 1, page_size: int = 10):
    """获取公告列表"""
    result = await AnnouncementService.get_announcement_list(page, page_size)
    return await response_base.success(data=result)


