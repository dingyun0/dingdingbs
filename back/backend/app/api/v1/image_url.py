#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, UploadFile
# from backend.app.models.user import User
from fastapi import APIRouter,  UploadFile, File


import os
import aiofiles
import uuid


router = APIRouter()


@router.post("/upload", summary="上传文件")
async def upload_file(
    file: UploadFile = File(...),
):
    """
    上传文件接口
    - 支持JPG和PNG格式
    - 文件大小限制为5MB
    - 返回文件URL供前端使用
    """
    try:
        # 检查文件类型
        if not file.content_type in ["image/jpeg", "image/png"]:
            return {"code": 400, "message": "只支持 JPG/PNG 格式的图片"}

        # 读取文件内容
        content = await file.read()
        
        # 检查文件大小（限制为5MB）
        if len(content) > 5 * 1024 * 1024:
            return {"code": 400, "message": "文件大小不能超过5MB"}

        # 生成文件名
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        
        # 确保上传目录存在
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_dir, filename)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
            
        # 返回文件URL
        file_url = f"/static/uploads/{filename}"
        
        return {
            "code": 200,
            "message": "文件上传成功",
            "data": {
                "url": file_url,
                "filename": filename
            }
        }
    except Exception as e:
        print(f"文件上传失败: {str(e)}")
        return {"code": 500, "message": f"文件上传失败: {str(e)}"}

