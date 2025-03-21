#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.user import router as user_router
from backend.app.api.v1.announcement import router as announcement_router
from backend.app.api.v1.score import router as score_router
from backend.app.api.v1.session import router as session_router
from backend.app.api.v1.comprehensive_test import router as comprehensive_test_router
from backend.app.api.v1.activity import router as activity_router
from backend.app.core.conf import Settings

v1 = APIRouter(prefix=Settings.API_V1_STR)

v1.include_router(auth_router, prefix='/auth', tags=['认证'])
v1.include_router(user_router, prefix='/users', tags=['用户'])
v1.include_router(announcement_router, prefix='/announcement', tags=['公告'])
v1.include_router(score_router, prefix='/scores', tags=['成绩'])
v1.include_router(session_router, prefix='/sessions', tags=['课程'])
v1.include_router(comprehensive_test_router, prefix='/comprehensive-tests', tags=['综合测评'])
v1.include_router(activity_router,prefix='/activity',tags=['活动公告'])
