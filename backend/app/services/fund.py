"""
基金数据服务 - 获取基金实时数据
使用腾讯 gtimg API 获取准确的净值和涨跌数据
"""

import re
import aiohttp
from typing import Optional

# 腾讯基金 API (与小倍养基等一致)
TENCENT_FUND_API = "http://qt.gtimg.cn/q=jj{code}"


async def fetch_fund_realtime(code: str) -> Optional[dict]:
    """
    获取单个基金的实时估值数据
    使用腾讯 gtimg API，数据与小倍养基等主流 App 一致
    
    腾讯 API 返回格式:
    v_jj013841="013841~银华集成电路混合C~0.0000~0.0000~~1.8277~1.8277~-5.6720~2026-02-02~";
    字段: 代码~名称~???~???~~最新净值~昨日净值~涨跌幅%~日期~
    """
    if not code or len(code) != 6:
        return None
    
    url = TENCENT_FUND_API.format(code=code)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    return await fallback_fetch(code)
                
                # 腾讯返回 GBK 编码
                raw_bytes = await resp.read()
                text = raw_bytes.decode('gbk', errors='ignore')
                
                # 解析格式: v_jj013841="013841~名称~...~净值~昨日净值~涨幅~日期~";
                match = re.search(r'v_jj\d+="([^"]+)"', text)
                if not match:
                    return await fallback_fetch(code)
                
                parts = match.group(1).split('~')
                
                if len(parts) < 8:
                    return await fallback_fetch(code)
                
                # parts[0]: 代码
                # parts[1]: 名称
                # parts[5]: 最新净值
                # parts[6]: 昨日净值 (或相同值)
                # parts[7]: 涨跌幅
                # parts[8]: 日期
                
                current_nav = float(parts[5]) if parts[5] else 0
                yesterday_nav = float(parts[6]) if parts[6] else current_nav
                change_pct = float(parts[7]) if parts[7] else 0
                date_str = parts[8] if len(parts) > 8 else ""
                
                # 如果 parts[6] 和 parts[5] 相同，则从涨跌幅反推昨日净值
                if yesterday_nav == current_nav and change_pct != 0:
                    yesterday_nav = round(current_nav / (1 + change_pct / 100), 4)
                
                return {
                    "code": parts[0],
                    "name": parts[1],
                    "gsz": current_nav,         # 最新净值
                    "gszzl": change_pct,        # 涨跌幅%
                    "dwjz": yesterday_nav,      # 昨日净值
                    "gztime": date_str,         # 日期
                    "jzrq": date_str,
                }
                
    except Exception as e:
        print(f"腾讯 API 获取失败: {e}, 尝试备用接口")
        return await fallback_fetch(code)


async def fallback_fetch(code: str) -> Optional[dict]:
    """
    备用接口：天天基金估值 (数据可能有偏差)
    """
    url = f"http://fundgz.1234567.com.cn/js/{code}.js"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return None
                    
                text = await resp.text()
                
                # 解析 JSONP: jsonpgz({...});
                match = re.search(r'jsonpgz\((.+?)\);?$', text)
                if not match:
                    return None
                    
                import json
                data = json.loads(match.group(1))
                
                return {
                    "code": data.get("fundcode", code),
                    "name": data.get("name", "未知基金"),
                    "gsz": float(data.get("gsz", 0)),
                    "gszzl": float(data.get("gszzl", 0)),
                    "dwjz": float(data.get("dwjz", 0)),
                    "gztime": data.get("gztime", ""),
                    "jzrq": data.get("jzrq", ""),
                }
    except Exception as e:
        print(f"备用接口也失败: {e}")
        return None


async def batch_fetch_funds(codes: list[str]) -> list[dict]:
    """
    批量获取多个基金数据
    """
    results = []
    for code in codes:
        data = await fetch_fund_realtime(code)
        if data:
            results.append(data)
    return results
