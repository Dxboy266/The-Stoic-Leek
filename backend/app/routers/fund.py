"""
基金数据路由 - 获取基金实时估值
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

from ..services.fund import fetch_fund_realtime, batch_fetch_funds


router = APIRouter(prefix="/fund", tags=["基金数据"])


class FundRealtimeData(BaseModel):
    """基金实时数据"""
    code: str
    name: str
    gsz: float        # 实时估值
    gszzl: float      # 涨跌幅%
    dwjz: float       # 昨日净值
    gztime: str       # 估值时间
    jzrq: str         # 净值日期


@router.get("/{code}", response_model=Optional[FundRealtimeData])
async def get_fund_realtime(code: str):
    """
    获取单个基金的实时估值数据
    
    - **code**: 6位基金代码，如 110022
    """
    if not code or len(code) != 6:
        raise HTTPException(status_code=400, detail="请输入6位基金代码")
    
    data = await fetch_fund_realtime(code)
    
    if not data:
        raise HTTPException(status_code=404, detail="基金代码无效或暂无数据")
    
    return FundRealtimeData(**data)


@router.get("/batch/query")
async def get_funds_batch(
    codes: str = Query(..., description="基金代码，逗号分隔，如 110022,519069")
):
    """
    批量获取多个基金的实时估值数据
    """
    code_list = [c.strip() for c in codes.split(",") if c.strip()]
    
    if not code_list:
        raise HTTPException(status_code=400, detail="请提供基金代码")
    
    if len(code_list) > 20:
        raise HTTPException(status_code=400, detail="最多支持20个基金")
    
    results = await batch_fetch_funds(code_list)
    
    return [FundRealtimeData(**item) for item in results]
