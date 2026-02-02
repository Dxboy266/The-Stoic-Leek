"""
市场数据路由 - 北向资金、热门板块、每日总结
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..schemas import (
    NorthboundFlowData, 
    MarketHotSector, 
    DailyMarketSummary,
    MessageResponse
)
from ..services import (
    get_northbound_flow, 
    get_hot_sectors, 
    generate_daily_summary
)

router = APIRouter(prefix="/market", tags=["市场数据"])


@router.get("/northbound", response_model=Optional[NorthboundFlowData])
async def northbound_flow(
    date: Optional[str] = Query(None, description="日期，格式 YYYY-MM-DD")
):
    """
    获取北向资金数据
    
    返回沪股通、深股通净流入数据
    """
    data = await get_northbound_flow(date)
    
    if not data:
        raise HTTPException(
            status_code=404,
            detail="暂无数据"
        )
    
    return NorthboundFlowData(**data)


@router.get("/hot-sectors", response_model=list[MarketHotSector])
async def hot_sectors(
    top: int = Query(10, ge=1, le=30, description="返回前 N 个板块")
):
    """
    获取今日热门板块
    
    按涨跌幅排序的行业板块
    """
    data = await get_hot_sectors(top)
    return [MarketHotSector(**item) for item in data]


@router.get("/daily-summary", response_model=DailyMarketSummary)
async def daily_summary(
    api_key: str = Query(..., description="AI API 密钥"),
    model: str = Query("deepseek-ai/DeepSeek-V3", description="AI 模型")
):
    """
    获取每日市场 AI 总结
    
    包含北向资金、热门板块和 AI 点评
    """
    try:
        data = await generate_daily_summary(api_key, model)
        return DailyMarketSummary(**data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"生成失败: {str(e)}"
        )


@router.get("/health")
async def market_health():
    """
    检查市场数据服务健康状态
    """
    try:
        # 尝试获取数据
        northbound = await get_northbound_flow()
        sectors = await get_hot_sectors(3)
        
        return {
            "status": "healthy",
            "northbound_available": northbound is not None,
            "sectors_count": len(sectors),
            "message": "市场数据服务正常"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "message": "部分功能可能不可用"
        }
