"""
AI 服务 - 处理 AI 调用
"""

import httpx
from typing import Optional

from ..config import (
    get_settings, SYSTEM_PROMPT, build_user_prompt, 
    MOOD_KEYWORDS, DEFAULT_EXERCISES
)


def _parse_response(text: str) -> dict:
    """解析 AI 响应"""
    mood, exercise, advice = "麻木", "休息", text
    
    for line in text.split('\n'):
        if '【心情】' in line:
            m = line.split('】')[-1].strip().strip('：:')
            for w in MOOD_KEYWORDS:
                if w in m:
                    mood = w
                    break
            # 如果没匹配到预设词，直接用 AI 返回的
            if mood == "麻木" and m:
                mood = m[:4]  # 取前4个字
        elif '【运动】' in line:
            exercise = line.split('】')[-1].strip().strip('：:')
        elif '【建议】' in line:
            advice = line.split('】')[-1].strip().strip('：:')
    
    return {"mood": mood, "exercise": exercise, "advice": advice, "full": text}


async def call_ai(
    api_key: str, 
    model: str, 
    amount: float, 
    total_assets: float, 
    exercises: list[str]
) -> dict:
    """调用 AI 生成建议"""
    if not api_key:
        raise ValueError("请先配置 API 密钥")
    
    settings = get_settings()
    exercise_str = ', '.join(exercises) if exercises else '休息'
    user_prompt = build_user_prompt(amount, total_assets, exercise_str)
    
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
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": settings.API_TEMPERATURE
            },
            timeout=settings.API_TIMEOUT
        )
        
        if resp.status_code == 401:
            raise ValueError("API 密钥无效")
        resp.raise_for_status()
        
        data = resp.json()
        text = data['choices'][0]['message']['content'].strip()
        return _parse_response(text)


async def generate_prescription(
    amount: float,
    total_assets: float,
    api_key: str,
    model: str = "deepseek-ai/DeepSeek-V3",
    exercises: Optional[list[str]] = None
) -> dict:
    """生成韭菜处方
    
    Returns:
        包含 mood, exercise, advice, roi, full 的字典
    """
    if exercises is None:
        exercises = DEFAULT_EXERCISES.copy()
    
    # 计算收益率
    roi = round((amount / total_assets) * 100, 2) if total_assets > 0 else 0
    
    # 调用 AI
    result = await call_ai(api_key, model, amount, total_assets, exercises)
    
    return {
        "amount": amount,
        "total_assets": total_assets,
        "roi": roi,
        **result
    }
