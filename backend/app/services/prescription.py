"""
韭菜处方生成服务 - 100% AI 驱动
"""

import httpx
from datetime import datetime
from typing import Optional

from ..config import get_settings, SYSTEM_PROMPT, build_user_prompt, DEFAULT_EXERCISES


async def generate_prescription(
    amount: float,
    total_assets: float,
    api_key: str,
    model: str = "deepseek-ai/DeepSeek-V3",
    exercises: Optional[list[str]] = None
) -> dict:
    """
    调用 AI 生成个性化运动处方和毒舌建议
    
    Args:
        amount: 今日盈亏（元）
        total_assets: 本金（元）
        api_key: SiliconFlow API Key
        model: AI 模型
        exercises: 可选动作池，默认使用内置
    
    Returns:
        {
            "amount": 500.0,
            "total_assets": 10000.0,
            "roi": 5.0,
            "mood": "膨胀",
            "exercise": "深蹲×30，波比跳×15，平板支撑2分钟",
            "advice": "赚了5个点就开始膨胀？...",
            "full": "完整AI回复"
        }
    """
    settings = get_settings()
    
    # 参数校验
    if total_assets <= 0:
        raise ValueError("本金必须大于 0")
    
    if not api_key or api_key.strip() == "":
        raise ValueError("请在设置页配置 API Key")
    
    # 计算 ROI
    roi = (amount / total_assets) * 100
    
    # 构建动作池字符串
    exercise_pool = exercises if exercises else DEFAULT_EXERCISES
    exercise_str = "、".join(exercise_pool)
    
    # 构建用户 Prompt
    user_prompt = build_user_prompt(amount, total_assets, exercise_str)
    
    # 调用 AI
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
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": settings.API_TEMPERATURE,
                    "max_tokens": 500
                },
                timeout=settings.API_TIMEOUT
            )
            
            if resp.status_code != 200:
                error_detail = resp.json().get("error", {}).get("message", "未知错误")
                raise Exception(f"AI 调用失败 ({resp.status_code}): {error_detail}")
            
            data = resp.json()
            full_text = data['choices'][0]['message']['content'].strip()
    
    except httpx.RequestError as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except KeyError as e:
        raise Exception(f"AI 响应格式异常: {str(e)}")
    except Exception as e:
        raise Exception(f"AI 调用异常: {str(e)}")
    
    # 解析 AI 回复（按行解析）
    lines = [l.strip() for l in full_text.split('\n') if l.strip()]
    
    mood = ""
    exercise = ""
    advice = ""
    
    for line in lines:
        if line.startswith("【心情】") or line.startswith("心情："):
            mood = line.split("】")[-1].split("：")[-1].strip()
        elif line.startswith("【运动】") or line.startswith("运动："):
            exercise = line.split("】")[-1].split("：")[-1].strip()
        elif line.startswith("【建议】") or line.startswith("建议："):
            advice = line.split("】")[-1].split("：")[-1].strip()
    
    # 如果解析失败，使用默认值
    if not mood:
        mood = "上头" if roi > 0 else "麻木"
    if not exercise:
        exercise = "深蹲×20" if abs(roi) < 3 else "波比跳×20，深蹲×50"
    if not advice:
        advice = full_text[:100]  # 截取前100字
    
    return {
        "amount": amount,
        "total_assets": total_assets,
        "roi": round(roi, 2),
        "mood": mood,
        "exercise": exercise,
        "advice": advice,
        "full": full_text,
        "generated_at": datetime.now().isoformat()
    }
