"""
基金数据服务 - 获取基金实时数据
使用腾讯 gtimg API 获取准确的净值和涨跌数据
"""

import re
import aiohttp
from typing import Optional

# 腾讯基金 API (与小倍养基等一致)
TENCENT_FUND_API = "http://qt.gtimg.cn/q=jj{code}"
# 腾讯智能提示 API (用于搜索)
TENCENT_SMARTBOX_API = "http://smartbox.gtimg.cn/s3/?t=all&q={keyword}"


async def fetch_fund_realtime(code: str) -> Optional[dict]:
    """
    获取单个基金的实时估值数据
    
    优先使用天天基金 fundgz 接口（提供盘中实时估值）
    失败时 fallback 到腾讯 gtimg 接口（提供收盘净值）
    
    返回字段:
        - gsz: 估算净值（盘中实时估值）
        - gszzl: 涨跌幅%
        - dwjz: 昨日净值
        - gztime: 估值时间
    """
    if not code or len(code) != 6:
        return None
    
    # 优先使用天天基金估值接口（盘中实时）
    result = await fetch_from_eastmoney(code)
    if result:
        return result
    
    # 失败则 fallback 到腾讯接口
    return await fetch_from_tencent(code)


async def fetch_from_eastmoney(code: str) -> Optional[dict]:
    """
    天天基金估值 API（盘中实时估值）
    接口: http://fundgz.1234567.com.cn/js/{code}.js
    数据格式: jsonpgz({"fundcode":"013841","name":"银华...","gszzl":"-0.12","gsz":"1.8255","gztime":"2026-02-03 15:00"})
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
                    "gsz": float(data.get("gsz", 0)),      # 盘中估值
                    "gszzl": float(data.get("gszzl", 0)),  # 涨跌幅%
                    "dwjz": float(data.get("dwjz", 0)),    # 昨日净值
                    "gztime": data.get("gztime", ""),      # 估值时间
                    "jzrq": data.get("jzrq", ""),          # 净值日期
                }
    except Exception as e:
        print(f"天天基金接口失败: {e}")
        return None


async def fetch_from_tencent(code: str) -> Optional[dict]:
    """
    腾讯 gtimg API（收盘净值，数据更准确但非实时）
    接口: http://qt.gtimg.cn/q=jj{code}
    数据格式: v_jj013841="013841~银华集成电路混合C~0.0000~0.0000~~1.8277~1.8277~-5.6720~2026-02-02~";
    """
    url = TENCENT_FUND_API.format(code=code)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    return None
                
                # 腾讯返回 GBK 编码
                raw_bytes = await resp.read()
                text = raw_bytes.decode('gbk', errors='ignore')
                
                # 解析格式: v_jj013841="013841~名称~...~净值~昨日净值~涨幅~日期~";
                match = re.search(r'v_jj\d+="([^"]+)"', text)
                if not match:
                    return None
                
                parts = match.group(1).split('~')
                
                if len(parts) < 8:
                    return None
                
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
        print(f"腾讯 API 获取失败: {e}")
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


async def search_fund_by_name(keyword: str) -> list[dict]:
    """
    通过名称搜索基金，返回匹配的列表
    优先使用本地缓存（天天基金全量列表），更稳定可靠
    """
    if not keyword:
        return []
    
    # 优先使用本地缓存（天天基金全量列表，最可靠）
    results = await search_from_local_cache(keyword)
    if results:
        return results
    
    # 备用：东方财富搜索 API
    results = await search_from_eastmoney(keyword)
    if results:
        return results
    
    # 最后备用：腾讯 SmartBox（返回场内代码，可能不适用）
    return await search_from_tencent(keyword)



async def search_from_eastmoney(keyword: str) -> list[dict]:
    """
    东方财富(天天基金)搜索 API
    接口: https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx
    这是 leek-fund 使用的数据源，更稳定可靠
    """
    url = f"https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=1&key={keyword}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=5),
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            ) as resp:
                if resp.status != 200:
                    return []
                
                data = await resp.json()
                
                # 返回格式: {"Datas": [{"CODE": "013841", "NAME": "银华集成电路混合C", ...}], ...}
                funds = []
                datas = data.get("Datas", [])
                
                for item in datas:
                    code = item.get("CODE", "")
                    name = item.get("NAME", "")
                    fund_type = item.get("CATEGORYDESC", "jj")  # 基金类型描述
                    
                    if code and len(code) == 6:
                        funds.append({
                            "code": code,
                            "name": name,
                            "type": fund_type
                        })
                
                return funds
                
    except Exception as e:
        print(f"东方财富搜索失败: {e}")
        return []


async def search_from_tencent(keyword: str) -> list[dict]:
    """
    腾讯 SmartBox 搜索 API (备用)
    返回格式: v_hint="sh~511880~银华日利ETF~yhrletf~ETF^sz~161810~银华LOF~yhxylof-~LOF"
    每条记录用 ^ 分隔，内部用 ~ 分隔：市场~代码~名称~拼音~类型
    """
    url = TENCENT_SMARTBOX_API.format(keyword=keyword)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status != 200:
                    return []
                
                raw_bytes = await resp.read()
                text = raw_bytes.decode('gbk', errors='ignore')
                
                match = re.search(r'v_hint="([^"]+)"', text)
                if not match:
                    return []
                
                content = match.group(1)
                if not content or content == "N":
                    return []
                
                # 解析格式：用 ^ 分隔多条记录
                records = content.split('^')
                funds = []
                
                for record in records:
                    # 每条记录用 ~ 分隔：市场~代码~名称~拼音~类型
                    parts = record.split('~')
                    if len(parts) >= 5:
                        market = parts[0]  # sh, sz
                        code = parts[1]    # 511880 (ETF/LOF 代码)
                        name = parts[2]    # 银华日利ETF
                        pinyin = parts[3]  # yhrletf
                        fund_type = parts[4]  # ETF, LOF, etc.
                        
                        # 注意：这里返回的是交易所代码（如511880），不是场外基金代码（如013841）
                        # 我们只接受 6 位代码，但不能直接用于场外基金查询
                        if code and len(code) == 6 and fund_type not in ['GP', 'gp']:
                            funds.append({
                                "code": code,
                                "name": name,
                                "type": fund_type
                            })
                
                return funds

    except Exception as e:
        print(f"腾讯搜索失败: {e}")
        return []


# 全量基金代码列表缓存（启动时加载）
_fund_code_cache: list[dict] = []
_fund_cache_loaded = False


async def load_fund_code_cache():
    """
    从天天基金加载全量基金代码列表
    接口: http://fund.eastmoney.com/js/fundcode_search.js
    """
    global _fund_code_cache, _fund_cache_loaded
    
    if _fund_cache_loaded:
        return
    
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status != 200:
                    print("加载基金代码列表失败")
                    return
                
                text = await resp.text()
                
                # 格式: var r = [["000001","HXCZHH","华夏成长混合","混合型","HUAXIACHENGZHANGHUNHE"],...]
                match = re.search(r'var r\s*=\s*(\[.+\])', text, re.DOTALL)
                if match:
                    import json
                    data = json.loads(match.group(1))
                    
                    for item in data:
                        if len(item) >= 3:
                            _fund_code_cache.append({
                                "code": item[0],
                                "pinyin": item[1],
                                "name": item[2],
                                "type": item[3] if len(item) > 3 else "基金"
                            })
                    
                    _fund_cache_loaded = True
                    print(f"基金代码列表加载完成，共 {len(_fund_code_cache)} 只基金")
                    
    except Exception as e:
        print(f"加载基金代码列表失败: {e}")


async def search_from_local_cache(keyword: str) -> list[dict]:
    """
    从本地缓存搜索基金（基于天天基金全量列表）
    """
    global _fund_code_cache, _fund_cache_loaded
    
    # 确保缓存已加载
    if not _fund_cache_loaded:
        await load_fund_code_cache()
    
    if not _fund_code_cache:
        return []
    
    keyword_lower = keyword.lower()
    results = []
    
    for fund in _fund_code_cache:
        # 匹配代码、名称或拼音
        if (keyword_lower in fund["name"].lower() or 
            keyword_lower in fund.get("pinyin", "").lower() or
            keyword_lower in fund["code"]):
            results.append({
                "code": fund["code"],
                "name": fund["name"],
                "type": fund["type"]
            })
            if len(results) >= 10:  # 最多返回 10 条
                break
    
    return results

