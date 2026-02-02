"""
数据模型 - Pydantic Schemas
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ========== 认证相关 ==========
class UserCreate(BaseModel):
    """用户注册"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """用户登录"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """用户信息响应"""
    id: str
    email: str


class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ========== 盈亏记录相关 ==========
class ProfitLossInput(BaseModel):
    """盈亏输入"""
    amount: float = Field(..., description="今日盈亏金额")
    total_assets: float = Field(..., gt=0, description="本金")


class AIAdviceResponse(BaseModel):
    """AI 建议响应"""
    mood: str
    exercise: str
    advice: str
    roi: float
    full: Optional[str] = None


class GeneratePrescriptionRequest(BaseModel):
    """生成处方请求"""
    amount: float
    total_assets: float
    api_key: str
    model: str = "deepseek-ai/DeepSeek-V3"
    exercises: list[str] = []


class GeneratePrescriptionResponse(BaseModel):
    """生成处方响应"""
    amount: float
    total_assets: float
    roi: float
    mood: str
    exercise: str
    advice: str
    full: str


# ========== 用户设置 ==========
class UserSettings(BaseModel):
    """用户设置"""
    api_key: Optional[str] = ""
    exercises: list[str] = []
    model: str = "deepseek-ai/DeepSeek-V3"
    model_name: str = "DeepSeek-V3 (免费)"
    total_assets: Optional[float] = None


class UserSettingsUpdate(BaseModel):
    """更新用户设置"""
    api_key: Optional[str] = None
    exercises: Optional[list[str]] = None
    model: Optional[str] = None
    model_name: Optional[str] = None
    total_assets: Optional[float] = None


# ========== 市场数据相关 ==========
class NorthboundFlowData(BaseModel):
    """北向资金数据"""
    date: str
    shanghai_net: float  # 沪股通净流入
    shenzhen_net: float  # 深股通净流入
    total_net: float  # 总计净流入
    unit: str = "亿元"


class MarketHotSector(BaseModel):
    """热门板块"""
    name: str
    change_pct: float
    leading_stocks: list[str] = []


class DailyMarketSummary(BaseModel):
    """每日市场总结"""
    date: str
    northbound_flow: Optional[NorthboundFlowData] = None
    hot_sectors: list[MarketHotSector] = []
    ai_summary: str = ""
    generated_at: Optional[datetime] = None


# ========== 通用响应 ==========
class MessageResponse(BaseModel):
    """通用消息响应"""
    success: bool
    message: str
    data: Optional[dict] = None
