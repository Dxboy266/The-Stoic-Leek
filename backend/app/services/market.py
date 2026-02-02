"""
市场数据服务 - 使用 AkShare 获取金融数据（带缓存）
"""

import httpx
import akshare as ak
from datetime import datetime, date, timedelta
from typing import Optional
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from ..config import get_settings

logger = logging.getLogger(__name__)

# ========== 缓存机制 ==========
_cache = {
    "northbound": {"data": None, "last_update": None},
    "sectors": {"data": None, "last_update": None},
}
CACHE_DURATION = timedelta(minutes=15)  # 缓存15分钟


def _is_cache_valid(cache_key: str) -> bool:
    """检查缓存是否有效"""
    cache_entry = _cache.get(cache_key)
    if not cache_entry or not cache_entry["last_update"]:
        return False
    return datetime.now() - cache_entry["last_update"] < CACHE_DURATION


def _refresh_northbound_cache():
    """后台刷新北向资金缓存"""
    try:
        logger.info("开始刷新北向资金缓存...")
        df = ak.stock_hsgt_hist_em(symbol="北向资金")
        
        if not df.empty:
            row = df.iloc[-1]
            data = {
                "date": str(row.get('日期', date.today().isoformat())),
                "shanghai_net": float(row.get('沪股通净流入', row.get('当日净流入', 0))),
                "shenzhen_net": float(row.get('深股通净流入', 0)),
                "total_net": float(row.get('当日净流入', row.get('北向资金净流入', 0))),
                "unit": "亿元"
            }
            _cache["northbound"]["data"] = data
            _cache["northbound"]["last_update"] = datetime.now()
            logger.info(f"北向资金缓存刷新成功: {data['date']}")
        else:
            logger.warning("北向资金数据为空")
    except Exception as e:
        logger.error(f"刷新北向资金缓存失败: {e}")


def _refresh_sectors_cache():
    """后台刷新板块缓存"""
    try:
        logger.info("开始刷新板块缓存...")
        df = ak.stock_board_industry_spot_em()
        
        if not df.empty:
            change_col = '涨跌幅' if '涨跌幅' in df.columns else '涨幅'
            name_col = '板块名称' if '板块名称' in df.columns else '名称'
            
            df = df.sort_values(change_col, ascending=False).head(20)
            
            result = []
            for _, row in df.iterrows():
                result.append({
                    "name": str(row.get(name_col, '')),
                    "change_pct": float(row.get(change_col, 0)),
                    "leading_stocks": []
                })
            
            _cache["sectors"]["data"] = result
            _cache["sectors"]["last_update"] = datetime.now()
            logger.info(f"板块缓存刷新成功，共 {len(result)} 条")
        else:
            logger.warning("板块数据为空")
    except Exception as e:
        logger.error(f"刷新板块缓存失败: {e}")


# ========== 启动后台定时任务 ==========
scheduler = BackgroundScheduler()
scheduler.add_job(_refresh_northbound_cache, 'interval', minutes=15, id='refresh_northbound')
scheduler.add_job(_refresh_sectors_cache, 'interval', minutes=15, id='refresh_sectors')

# 立即执行一次
scheduler.add_job(_refresh_northbound_cache, id='init_northbound')
scheduler.add_job(_refresh_sectors_cache, id='init_sectors')

try:
    scheduler.start()
    logger.info("市场数据定时刷新任务已启动")
except Exception as e:
    logger.error(f"启动定时任务失败: {e}")


# ========== 北向资金 ==========
async def get_northbound_flow(target_date: Optional[str] = None) -> Optional[dict]:
    """
    获取北向资金流入数据（从缓存读取）
    
    Args:
        target_date: 目标日期，格式 YYYY-MM-DD，默认今天
    
    Returns:
        {
            "date": "2026-01-25",
            "shanghai_net": 50.32,  # 沪股通净流入（亿元）
            "shenzhen_net": 30.15,  # 深股通净流入（亿元）
            "total_net": 80.47,     # 总计净流入（亿元）
            "unit": "亿元"
        }
    """
    # 优先从缓存读取
    if _is_cache_valid("northbound") and _cache["northbound"]["data"]:
        logger.info("从缓存返回北向资金数据")
        return _cache["northbound"]["data"]
    
    # 缓存失效或不存在，手动触发刷新
    logger.warning("缓存失效，手动刷新北向资金")
    _refresh_northbound_cache()
    
    # 返回刚刷新的数据或 Mock 数据
    if _cache["northbound"]["data"]:
        return _cache["northbound"]["data"]
    else:
        return _mock_northbound_flow()


def _mock_northbound_flow() -> dict:
    """模拟北向资金数据（开发测试用）"""
    import random
    return {
        "date": date.today().isoformat(),
        "shanghai_net": round(random.uniform(-50, 80), 2),
        "shenzhen_net": round(random.uniform(-40, 60), 2),
        "total_net": round(random.uniform(-80, 120), 2),
        "unit": "亿元"
    }


# ========== 热门板块 ==========
async def get_hot_sectors(top_n: int = 10) -> list[dict]:
    """
    获取今日热门板块（从缓存读取）
    
    Args:
        top_n: 返回前 N 个板块
    
    Returns:
        [
            {"name": "半导体", "change_pct": 3.25, "leading_stocks": []},
            ...
        ]
    """
    # 优先从缓存读取
    if _is_cache_valid("sectors") and _cache["sectors"]["data"]:
        logger.info("从缓存返回板块数据")
        return _cache["sectors"]["data"][:top_n]
    
    # 缓存失效或不存在，手动触发刷新
    logger.warning("缓存失效，手动刷新板块")
    _refresh_sectors_cache()
    
    # 返回刚刷新的数据或 Mock 数据
    if _cache["sectors"]["data"]:
        return _cache["sectors"]["data"][:top_n]
    else:
        return _mock_hot_sectors(top_n)


def _mock_hot_sectors(top_n: int = 10) -> list[dict]:
    """模拟热门板块数据（开发测试用）"""
    import random
    sectors = [
        "半导体", "人工智能", "新能源车", "光伏", "白酒",
        "医药生物", "军工", "消费电子", "房地产", "银行",
        "券商", "保险", "煤炭", "有色金属", "化工"
    ]
    random.shuffle(sectors)
    
    return [
        {
            "name": sectors[i],
            "change_pct": round(random.uniform(-3, 5), 2),
            "leading_stocks": []
        }
        for i in range(min(top_n, len(sectors)))
    ]


# ========== AI 市场总结 ==========
async def generate_daily_summary(
    api_key: str,
    model: str = "deepseek-ai/DeepSeek-V3"
) -> dict:
    """
    生成每日市场 AI 总结
    
    Returns:
        {
            "date": "2026-01-25",
            "northbound_flow": {...},
            "hot_sectors": [...],
            "ai_summary": "今日市场...",
            "generated_at": "2026-01-25T15:30:00"
        }
    """
    settings = get_settings()
    
    # 获取数据
    northbound = await get_northbound_flow()
    hot_sectors = await get_hot_sectors(10)
    
    # 构建 AI prompt
    sector_text = "\n".join([
        f"- {s['name']}: {s['change_pct']:+.2f}%" 
        for s in hot_sectors[:5]
    ])
    
    prompt = f"""# 今日 A 股市场数据

## 北向资金
- 沪股通净流入: {northbound['shanghai_net'] if northbound else 'N/A'}亿元
- 深股通净流入: {northbound['shenzhen_net'] if northbound else 'N/A'}亿元
- 北向资金总计: {northbound['total_net'] if northbound else 'N/A'}亿元

## 热门板块 Top 5
{sector_text}

# 任务
请用毒舌韭菜哲学家的口吻，写一段 150 字以内的今日市场点评。要求：
1. 指出今日"聪明钱"的动向
2. 嘲讽散户可能犯的错误
3. 给出一个反讽式的"投资建议"（实际上是劝退）
"""

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                settings.API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "你是一位阅尽沧桑的韭菜哲学家，擅长用毒舌但不失幽默的方式点评市场。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if resp.status_code == 200:
                data = resp.json()
                ai_summary = data['choices'][0]['message']['content'].strip()
            else:
                ai_summary = "AI 抽风了，自己看数据吧。"
    except Exception as e:
        ai_summary = f"AI 罢工了: {str(e)[:50]}"
    
    return {
        "date": date.today().isoformat(),
        "northbound_flow": northbound,
        "hot_sectors": hot_sectors,
        "ai_summary": ai_summary,
        "generated_at": datetime.now().isoformat()
    }
