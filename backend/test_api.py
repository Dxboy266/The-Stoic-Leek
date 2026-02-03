import aiohttp
import asyncio

async def test():
    # 测试1: 天天基金HTTP接口
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get('http://fundgz.1234567.com.cn/js/161725.js', timeout=aiohttp.ClientTimeout(total=10)) as r:
                print('=== 天天基金 HTTP ===')
                print('Status:', r.status)
                text = await r.text()
                print('Content:', text[:200] if text else 'Empty')
    except Exception as e:
        print('天天基金 HTTP 错误:', e)
    
    # 测试2: 腾讯接口
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get('http://qt.gtimg.cn/q=jj161725', timeout=aiohttp.ClientTimeout(total=10)) as r:
                print('\n=== 腾讯接口 ===')
                print('Status:', r.status)
                raw = await r.read()
                text = raw.decode('gbk', errors='ignore')
                print('Content:', text[:200] if text else 'Empty')
    except Exception as e:
        print('腾讯接口错误:', e)

asyncio.run(test())
