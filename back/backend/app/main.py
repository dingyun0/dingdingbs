from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from backend.app.core.conf import Settings
from backend.app.api.routers import v1
from backend.app.common.exception import exception_handler

app = FastAPI(
    title=Settings.TITLE,
    version=Settings.VERSION,
    description=Settings.DESCRIPTION,
    docs_url=Settings.DOCS_URL,
    redoc_url=Settings.REDOCS_URL,
)

# 注册数据库连接
register_tortoise(
    app,
    config={
        'connections': {
            'default': {
                'engine': 'tortoise.backends.mysql',
                'credentials': {
                    'host': Settings.DB_HOST,
                    'port': Settings.DB_PORT,
                    'user': Settings.DB_USER,
                    'password': Settings.DB_PASSWORD,
                    'database': Settings.DB_DATABASE,
                    'charset': Settings.DB_ENCODING,
                    'echo': Settings.DB_ECHO,
                }
            }
        },
        'apps': {
            'models': {
                'models': [
                    'backend.app.models.user',
                    'backend.app.models.score', 
                    'backend.app.models.announcement',
                    'backend.app.models.session',
                    'aerich.models'
                ],
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'timezone': Settings.DB_TIMEZONE
    },
    generate_schemas=True
)

# 注册路由
app.include_router(v1)

# 注册异常处理
exception_handler.register_exception(app) 