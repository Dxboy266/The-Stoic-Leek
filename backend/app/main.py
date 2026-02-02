"""
韭菜的自我修养 v2.0 - FastAPI 后端入口
The Stoic Leek Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import (
    prescription_router,
    market_router,
    persistence_router,
    fund_router
)

# 创建应用
app = FastAPI(
    title="韭菜的自我修养 API (Local Mode)",
    description="""
## The Stoic Leek v2.0 Backend (Local Mode)

Local-First 架构支持后端：仅提供 AI 调用和市场数据代理，不保存用户数据。

### 功能模块
- 💊 **处方**: AI 生成运动处方和毒舌建议 (无状态)
- 📊 **市场**: 北向资金、热门板块、每日 AI 总结 (缓存)
- 💾 **持久化**: 本地 JSON 文件存储
    """,
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 配置
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(prescription_router)
app.include_router(market_router)
app.include_router(persistence_router)
app.include_router(fund_router)


# 根路由
@app.get("/")
async def root():
    """API 根路由"""
    return {
        "name": "韭菜的自我修养 API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "message": "市场涨跌皆虚妄，唯有酸痛最真实。"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "stoic-leek-backend"
    }
