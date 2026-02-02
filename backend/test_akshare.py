"""
AkShare 数据源测试脚本
运行此脚本验证金融数据接口是否正常工作
"""

import asyncio
import sys
from datetime import date


def test_akshare_installation():
    """测试 AkShare 是否安装"""
    print("=" * 50)
    print("🧪 测试 AkShare 安装...")
    try:
        import akshare as ak
        print(f"✅ AkShare 版本: {ak.__version__}")
        return True
    except ImportError:
        print("❌ AkShare 未安装")
        print("   请运行: pip install akshare")
        return False


def test_northbound_flow():
    """测试北向资金数据"""
    print("\n" + "=" * 50)
    print("🧪 测试北向资金数据接口...")
    try:
        import akshare as ak
        
        # 使用正确的接口名获取北向资金历史数据
        df = ak.stock_hsgt_hist_em(symbol="北向资金")
        
        if df.empty:
            print("⚠️ 数据为空")
            return False
        
        print(f"✅ 获取到 {len(df)} 条记录")
        print(f"   数据列: {list(df.columns)}")
        
        # 显示最新一条
        latest = df.iloc[-1]
        print(f"\n   📊 最新数据:")
        for col in df.columns:
            print(f"      {col}: {latest.get(col, 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_industry_sectors():
    """测试行业板块数据"""
    print("\n" + "=" * 50)
    print("🧪 测试行业板块数据接口...")
    try:
        import akshare as ak
        
        # 使用正确的接口名获取行业板块行情
        df = ak.stock_board_industry_spot_em()
        
        if df.empty:
            print("⚠️ 数据为空")
            return False
        
        print(f"✅ 获取到 {len(df)} 个板块")
        print(f"   数据列: {list(df.columns)}")
        
        # 按涨跌幅排序
        change_col = '涨跌幅' if '涨跌幅' in df.columns else '涨幅'
        name_col = '板块名称' if '板块名称' in df.columns else '名称'
        
        if change_col in df.columns:
            df_sorted = df.sort_values(change_col, ascending=False)
            
            print(f"\n   📈 今日涨幅 Top 5:")
            for i, (_, row) in enumerate(df_sorted.head(5).iterrows()):
                name = row.get(name_col, 'N/A')
                change = row.get(change_col, 0)
                print(f"      {i+1}. {name}: {change:+.2f}%")
            
            print(f"\n   📉 今日跌幅 Top 5:")
            for i, (_, row) in enumerate(df_sorted.tail(5).iterrows()):
                name = row.get(name_col, 'N/A')
                change = row.get(change_col, 0)
                print(f"      {i+1}. {name}: {change:+.2f}%")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_etf_flow():
    """测试 ETF 数据"""
    print("\n" + "=" * 50)
    print("🧪 测试 ETF 数据接口...")
    try:
        import akshare as ak
        
        # 获取 ETF 实时行情
        df = ak.fund_etf_spot_em()
        
        if df.empty:
            print("⚠️ 数据为空")
            return False
        
        print(f"✅ 获取到 {len(df)} 只 ETF")
        print(f"   数据列: {list(df.columns)[:10]}...")  # 只显示前10列
        
        # 显示几只热门 ETF
        hot_etfs = ['沪深300ETF', '中证500ETF', '创业板ETF', '科创50ETF']
        
        print(f"\n   📊 热门 ETF 行情:")
        for etf_name in hot_etfs:
            if '名称' in df.columns:
                match = df[df['名称'].str.contains(etf_name.replace('ETF', ''), na=False)]
                if not match.empty:
                    row = match.iloc[0]
                    name = row.get('名称', 'N/A')
                    change = row.get('涨跌幅', 0)
                    print(f"      {name}: {change:+.2f}%")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_dragon_tiger():
    """测试龙虎榜数据"""
    print("\n" + "=" * 50)
    print("🧪 测试龙虎榜数据接口...")
    try:
        import akshare as ak
        
        # 获取龙虎榜数据
        df = ak.stock_lhb_detail_em(start_date="20260120", end_date="20260125")
        
        if df.empty:
            print("⚠️ 近期无龙虎榜数据（可能是周末或节假日）")
            # 尝试获取更早的数据
            df = ak.stock_lhb_detail_em(start_date="20260101", end_date="20260125")
        
        if df.empty:
            print("⚠️ 数据为空")
            return False
        
        print(f"✅ 获取到 {len(df)} 条龙虎榜记录")
        print(f"   数据列: {list(df.columns)}")
        
        # 显示最新几条
        print(f"\n   📊 最新龙虎榜:")
        for i, (_, row) in enumerate(df.head(5).iterrows()):
            name = row.get('名称', row.get('股票名称', 'N/A'))
            reason = row.get('上榜原因', 'N/A')[:20] if row.get('上榜原因') else 'N/A'
            print(f"      {i+1}. {name} - {reason}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "🌱" * 25)
    print("   韭菜的自我修养 v2.0 - 数据源测试")
    print("🌱" * 25)
    
    results = {}
    
    # 测试 AkShare 安装
    if not test_akshare_installation():
        print("\n❌ AkShare 未安装，无法继续测试")
        print("   请先运行: pip install akshare")
        sys.exit(1)
    
    # 测试各个接口
    results['北向资金'] = test_northbound_flow()
    results['行业板块'] = test_industry_sectors()
    results['ETF 行情'] = test_etf_flow()
    results['龙虎榜'] = test_dragon_tiger()
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 测试结果汇总:")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"   {name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 所有测试通过！数据源可用。")
    else:
        print("⚠️ 部分测试失败，请检查网络或 AkShare 版本。")
    
    return all_passed


if __name__ == "__main__":
    main()
