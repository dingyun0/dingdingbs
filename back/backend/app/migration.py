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
        'models': {
            'models': [
                'backend.app.models.announcement',
                'backend.app.models.user',
                'backend.app.models.score',
                'backend.app.models.session',
                'backend.app.models.comprehensive_test',
                'backend.app.models.student',
                'backend.app.models.teacher',
                'aerich.models'
            ],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}
