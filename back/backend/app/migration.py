#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('../../')

from backend.app.database.db_mysql import mysql_config  # noqa: E402
from backend.app.models import models  # noqa: E402

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'password': '123456',
                'database': 'dingdingbs',
                'charset': 'utf8mb4',
                'echo': False,
            }
        }
    },
    'apps': {
        'models': {  # 这是 app 名称
            'models': [
                'backend.app.models.user',  # 用户模型
                'aerich.models'     # aerich 需要的模型
            ],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}
