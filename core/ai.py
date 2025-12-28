"""
AI 模块 - 处理 AI 调用
"""

import requests
from config import (
    SYSTEM_PROMPT, build_user_prompt, MOOD_KEYWORDS,
    API_URL, API_TIMEOUT, API_TEMPERATURE
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


def call_ai(api_key: str, model: str, amount: float, total_assets: float, exercises: list[str]) -> dict:
    """调用 AI 生成建议"""
    if not api_key:
        raise Exception("请先配置 API 密钥")
    
    exercise_str = ', '.join(exercises) if exercises else '休息'
    user_prompt = build_user_prompt(amount, total_assets, exercise_str)
    
    resp = requests.post(
        API_URL,
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
            "temperature": API_TEMPERATURE
        },
        timeout=API_TIMEOUT
    )
    
    if resp.status_code == 401:
        raise Exception("API 密钥无效")
    resp.raise_for_status()
    
    text = resp.json()['choices'][0]['message']['content'].strip()
    return _parse_response(text)
