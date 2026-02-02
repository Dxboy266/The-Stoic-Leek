"""
Routers 模块
"""

from .prescription import router as prescription_router
from .market import router as market_router
from .persistence import router as persistence_router
from .fund import router as fund_router

__all__ = [
    "prescription_router",
    "market_router",
    "persistence_router",
    "fund_router",
]
