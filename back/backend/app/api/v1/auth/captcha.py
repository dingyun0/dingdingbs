#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fast_captcha import img_captcha
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_limiter.depends import RateLimiter
from starlette.concurrency import run_in_threadpool
from starlette.responses import StreamingResponse

from backend.app.common.redis import redis_client
from backend.app.core.conf import Settings
from backend.app.utils.generate_string import get_uuid4_str

router = APIRouter()


@router.get('/captcha', summary='获取验证码', dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def get_captcha(request: Request):
    try:
        img, code = await run_in_threadpool(img_captcha)
        print("1111",img,code)
        uuid = get_uuid4_str()
        print("uuid",uuid)
        
        # 存储验证码
        await redis_client.set(f'captcha:{uuid}', code, Settings.CAPTCHA_EXPIRATION_TIME)
        
        # 转换为base64
        import base64
        img_bytes = img.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode()
    
        
        return {
                "captchaEnabled": True,
                "img": img_base64,
                "uuid": uuid
            }
    except Exception as e:
        print(f"生成验证码错误: {str(e)}")
        return {
            "code": 500,
            "msg": str(e),
            "data": None
        }
