#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 只导入模块，不导入具体的类
from backend.app.models import user
from backend.app.models import score
from backend.app.models import announcement
from backend.app.models import session
from backend.app.models import comprehensive_test

# 新增model后，在list引入模块文件
models = [
    user,
    score,
    announcement,
    session,
    comprehensive_test

]

__all__ = ['User', 'Score', 'Announcement','Session','ComprehensiveTest']
