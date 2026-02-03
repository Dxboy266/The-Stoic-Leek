"""
AI 配置路由 - 测试连接和管理 AI 提供商
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI

router = APIRouter(prefix="/ai", tags=["AI 配置"])


class AITestRequest(BaseModel):
    """测试 AI 连接请求"""
    baseUrl: str
    apiKey: str
    model: str


class AITestResponse(BaseModel):
    """测试 AI 连接响应"""
    success: bool
    message: str


@router.post("/test", response_model=AITestResponse)
async def test_ai_connection(request: AITestRequest):
    """
    测试 AI 提供商连接
    
    发送一个简单的测试消息验证 API Key 是否有效
    """
    if not request.apiKey:
        raise HTTPException(status_code=400, detail="请提供 API Key")
    
    if not request.baseUrl:
        raise HTTPException(status_code=400, detail="请提供 API Base URL")
    
    if not request.model:
        raise HTTPException(status_code=400, detail="请提供模型名称")
    
    try:
        client = OpenAI(
            api_key=request.apiKey,
            base_url=request.baseUrl,
            timeout=10.0  # 10秒超时
        )
        
        # 发送一个简单的测试请求
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "user", "content": "Hi, respond with just 'OK' to confirm you're working."}
            ],
            max_tokens=10
        )
        
        if response.choices and len(response.choices) > 0:
            return AITestResponse(
                success=True,
                message="连接成功！AI 响应正常。"
            )
        else:
            return AITestResponse(
                success=False,
                message="AI 返回了空响应"
            )
            
    except Exception as e:
        error_message = str(e)
        
        # 友好的错误提示
        if "401" in error_message or "Unauthorized" in error_message:
            return AITestResponse(
                success=False,
                message="API Key 无效或已过期"
            )
        elif "404" in error_message:
            return AITestResponse(
                success=False,
                message=f"模型 '{request.model}' 不存在或不可用"
            )
        elif "timeout" in error_message.lower():
            return AITestResponse(
                success=False,
                message="连接超时，请检查网络"
            )
        elif "connection" in error_message.lower():
            return AITestResponse(
                success=False,
                message="无法连接到 API 服务器，请检查 URL"
            )
        else:
            return AITestResponse(
                success=False,
                message=f"连接失败: {error_message[:100]}"
            )
