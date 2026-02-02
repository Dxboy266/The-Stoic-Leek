"""
本地持久化路由 - 将数据保存到本地 JSON 文件
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Dict, Any, Optional

router = APIRouter(prefix="/persistence", tags=["本地存储"])

# 数据文件路径 (在后端运行目录下)
DATA_FILE = "stoic_leek_data.json"

class SaveDataRequest(BaseModel):
    data: Dict[str, Any]

@router.get("/load")
async def load_data():
    """从本地 JSON 文件加载数据"""
    if not os.path.exists(DATA_FILE):
        return {"data": None, "message": "暂无本地存档"}
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"data": data, "message": "加载成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取文件失败: {str(e)}")

@router.post("/save")
async def save_data(request: SaveDataRequest):
    """保存数据到本地 JSON 文件"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(request.data, f, indent=2, ensure_ascii=False)
        return {"status": "success", "message": "存档已保存到本地文件"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件失败: {str(e)}")
