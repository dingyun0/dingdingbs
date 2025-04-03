#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 只导入模块，不导入具体的类
from backend.app.models import user
from backend.app.models import score
from backend.app.models import announcement
from backend.app.models import session
from backend.app.models import comprehensive_test
from backend.app.models import student
from backend.app.models import teacher
from backend.app.models import activity
from backend.app.models import activity_review
from backend.app.models import college

# 新增model后，在list引入模块文件
models = [
    user,
    score,
    announcement,
    session,
    comprehensive_test,
    student,
    teacher,
    activity,
    activity_review,
    college
]

__all__ = ['User', 'Score', 'Announcement', 'Session', 'ComprehensiveTest', 'Student','Teacher','activity','activity_review','college']
