#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.models import user, announcement

# 新增model后，在list引入文件，而不是model类
models = [
    user,
    announcement,
]
