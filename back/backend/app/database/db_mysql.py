#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.core.conf import Settings
from backend.app.models import models

mysql_config = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': f'{Settings.DB_HOST}',
                'port': Settings.DB_PORT,
                'user': f'{Settings.DB_USER}',
                'password': f'{Settings.DB_PASSWORD}',
                'database': f'{Settings.DB_DATABASE}',
                'charset': f'{Settings.DB_ENCODING}',
                'echo': Settings.DB_ECHO,
            },
        },
    },
    'apps': {
        'ftm': {
            'models': [*models],
            'default_connection': 'default',
        },
    },
    'use_tz': False,
    'timezone': Settings.DB_TIMEZONE,
}
