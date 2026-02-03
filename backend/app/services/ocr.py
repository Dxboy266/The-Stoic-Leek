"""
OCR 服务 - 使用 AI 视觉模型识别截图
替代 PaddleOCR，使用 OpenAI 兼容接口（如 SiliconFlow/DeepSeek/Qwen-VL）
"""

import os
import json
import base64
import re
from typing import List, Optional
from pydantic import BaseModel
from openai import OpenAI

class FundFromOCR(BaseModel):
    """从截图识别出的基金信息"""
    name: str
    code: Optional[str] = None
    amount: Optional[float] = None
    shares: Optional[float] = None


def clean_fund_name_for_search(name: str) -> str:
    """
    清洗基金名称用于搜索
    - 移除后缀 A/B/C/H 等份额分类
    - 移除括号内容
    - 只取前几个关键字
    """
    if not name:
        return ""
    
    # 移除括号及其内容
    name = re.sub(r'[\(（].*?[\)）]', '', name)
    
    # 移除末尾的份额分类 A/B/C/D/E/F/H/R 等
    name = re.sub(r'[A-Ha-h]$', '', name.strip())
    
    # 移除"混合"、"股票"、"债券"、"指数"等通用词（便于搜索匹配）
    # 但保留核心关键词
    
    # 只取前 6 个字符（通常是基金名称的核心部分）
    if len(name) > 6:
        name = name[:6]
    
    return name.strip()


async def recognize_funds_from_screenshot(
    image_base64: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> List[FundFromOCR]:
    """
    使用 AI 视觉模型识别截图
    
    Args:
        image_base64: Base64 编码的图片
        base_url: API 基础地址，如果不指定则使用环境变量
        api_key: API Key，如果不指定则使用环境变量
        model: 视觉模型，如果不指定则使用环境变量配置
    """
    # 优先使用请求中的配置，否则回退到环境变量
    final_api_key = api_key or os.getenv("SILICONFLOW_API_KEY") or os.getenv("OPENAI_API_KEY")
    final_base_url = base_url or os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    final_model = model or os.getenv("VISION_MODEL", "Qwen/Qwen2-VL-72B-Instruct")
    
    if not final_api_key:
        raise ValueError("请配置 API Key（在设置页面或 .env 文件中）")

    # 处理 Base64 前缀
    if ',' in image_base64:
        image_base64 = image_base64.split(',')[1]

    client = OpenAI(
        api_key=final_api_key,
        base_url=final_base_url
    )

    # 提示词
    prompt = """
    请分析这张基金持仓截图，提取出所有基金的以下信息：
    1. 基金名称 (name)
    2. 基金代码 (code, 6位数字)
    3. 持有金额 (amount)
    4. 持有份额 (shares, 如果有的话)

    请直接返回 JSON 数组格式，不要包含 markdown 标记。例如：
    [
        {"name": "银华集成电路混合C", "code": "013841", "amount": 19515.74, "shares": 10677.76},
        {"name": "华泰柏瑞", "code": "011452", "amount": 4756.31}
    ]
    """

    try:
        # 使用最终确定的模型
        print(f"使用视觉模型: {final_model}, Base URL: {final_base_url[:30]}...") 

        response = client.chat.completions.create(
            model=final_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1024
        )

        content = response.choices[0].message.content
        
        # 清理 markdown 标记
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        data = json.loads(content)
        
        # 智能修正：用名称搜索来校验/修正代码
        from .fund import search_fund_by_name
        
        results = []
        for item in data:
            fund_obj = FundFromOCR(**item)
            original_code = fund_obj.code
            original_name = fund_obj.name
            
            print(f"处理基金: 名称={fund_obj.name}, AI识别代码={fund_obj.code}")
            
            # 尝试用名称搜索来校验代码
            try:
                # 清洗名称用于搜索
                search_name = clean_fund_name_for_search(fund_obj.name)
                print(f"  搜索关键词: {search_name}")
                
                search_results = await search_fund_by_name(search_name)
                
                if search_results:
                    # 找到匹配结果
                    best_match = search_results[0]
                    
                    if best_match['code'] != original_code:
                        print(f"  修正代码: AI={original_code} -> 搜索={best_match['code']}")
                    else:
                        print(f"  代码校验通过: {best_match['code']}")
                    
                    fund_obj.code = best_match['code']
                else:
                    # 搜索无结果，保留 AI 原始识别的代码
                    print(f"  搜索无结果，保留AI代码: {original_code}")
                    # 不修改 fund_obj.code，保持原值
                    
            except Exception as ex:
                # 搜索出错，保留 AI 原始识别的代码
                print(f"  搜索失败: {ex}，保留AI代码: {original_code}")
                # 不修改 fund_obj.code，保持原值
            
            # 确保代码不为空（如果AI也没识别出来，就跳过这只基金）
            if fund_obj.code and len(fund_obj.code) == 6 and fund_obj.code.isdigit():
                results.append(fund_obj)
            else:
                print(f"  警告: 无法确定代码，跳过基金: {original_name}")
            
        return results

    except Exception as e:
        print(f"AI 识别失败: {e}")
        # 如果是模型不支持，可能需要提示用户
        raise Exception(f"AI 识别失败: {str(e)}")

