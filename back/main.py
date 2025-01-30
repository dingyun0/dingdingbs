#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn
from path import Path

from backend.app.common.log import log
from backend.app.core.conf import Settings
from backend.app.core.registrar import register_app

app = register_app()

if __name__ == '__main__':
    try:
        log.info(
            """\n
 /$$$$$$$$                   /$$      /$$$$$$  /$$$$$$$  /$$$$$$
| $$_____/                  | $$     /$$__  $$| $$__  $$|_  $$_/
| $$    /$$$$$$   /$$$$$$$ /$$$$$$  | $$  | $$| $$  | $$  | $$
| $$$$$|____  $$ /$$_____/|_  $$_/  | $$$$$$$$| $$$$$$$/  | $$
| $$__/ /$$$$$$$|  $$$$$$   | $$    | $$__  $$| $$____/   | $$
| $$   /$$__  $$ |____  $$  | $$ /$$| $$  | $$| $$        | $$
| $$  |  $$$$$$$ /$$$$$$$/  |  $$$$/| $$  | $$| $$       /$$$$$$
|__/   |_______/|_______/    |___/  |__/  |__/|__/      |______/

            """
        )
        uvicorn.run(
            app=f'{Path(__file__).stem}:app',
            host=Settings.UVICORN_HOST,
            port=Settings.UVICORN_PORT,
            reload=Settings.UVICORN_RELOAD,
        )
    except Exception as e:
        log.error(f'❌ FastAPI start filed: {e}')
