'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { RefreshCw, AlertCircle, Database, Gauge } from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { NorthboundCard } from './northbound-card';
import { HotSectorsTable } from './hot-sectors-table';
import { AiMarketSummary } from './ai-market-summary';
import { MarketService } from '@/services/market';
import { useUserStore } from '@/store/user';

export function MarketDashboard() {
    const [northbound, setNorthbound] = useState<any>(null);
    const [sectors, setSectors] = useState<any[]>([]);
    const [summary, setSummary] = useState<any>(null);

    const [loadingNorthbound, setLoadingNorthbound] = useState(true);
    const [loadingSectors, setLoadingSectors] = useState(true);
    const [loadingSummary, setLoadingSummary] = useState(false);
    const [usingMockData, setUsingMockData] = useState(false);

    const { settings, updateSettings } = useUserStore();
    const hasInitialized = useRef(false);

    // 获取北向资金（带超时）
    const fetchNorthbound = useCallback(async () => {
        setLoadingNorthbound(true);
        try {
            const timeoutPromise = new Promise((_, reject) =>
                setTimeout(() => reject(new Error('请求超时')), 3000)
            );
            const data = await Promise.race([MarketService.getNorthbound(), timeoutPromise]);
            setNorthbound(data);
            setUsingMockData(false);
        } catch (err: any) {
            console.warn('使用模拟数据:', err.message);
            // 使用上个交易日的模拟数据
            const lastFriday = new Date();
            lastFriday.setDate(lastFriday.getDate() - ((lastFriday.getDay() + 2) % 7));
            setNorthbound({
                date: lastFriday.toISOString().split('T')[0],
                shanghai_net: 45.32,
                shenzhen_net: 28.15,
                total_net: 73.47,
                unit: '亿元'
            });
            setUsingMockData(true);
        } finally {
            setLoadingNorthbound(false);
        }
    }, []);

    // 获取热门板块
    const fetchSectors = useCallback(async () => {
        setLoadingSectors(true);
        try {
            const data = await MarketService.getHotSectors();
            setSectors(data);
        } catch (err: any) {
            console.error('Failed to fetch sectors:', err);
            // 使用模拟数据
            setSectors([
                { name: '半导体', change_pct: 4.25, leading_stocks: [] },
                { name: '人工智能', change_pct: 3.87, leading_stocks: [] },
                { name: '新能源车', change_pct: 2.56, leading_stocks: [] },
                { name: '光伏', change_pct: 1.92, leading_stocks: [] },
                { name: '军工', change_pct: 1.45, leading_stocks: [] },
                { name: '房地产', change_pct: -2.31, leading_stocks: [] },
                { name: '白酒', change_pct: -1.87, leading_stocks: [] },
                { name: '银行', change_pct: -0.95, leading_stocks: [] },
                { name: '保险', change_pct: -0.72, leading_stocks: [] },
                { name: '券商', change_pct: -0.45, leading_stocks: [] },
            ]);
        } finally {
            setLoadingSectors(false);
        }
    }, []);

    // 生成 AI 总结
    const generateSummary = useCallback(async () => {
        const apiKey = localStorage.getItem('siliconflow_api_key');

        setLoadingSummary(true);
        try {
            if (apiKey) {
                // 真实调用
                const data = await MarketService.getDailySummary({ api_key: apiKey });
                setSummary(data);

                // 持久化保存
                updateSettings({
                    market_summary: {
                        content: data.ai_summary,
                        date: new Date().toISOString().split('T')[0]
                    }
                });
            } else {
                // 模拟数据 (如果没有 Key)
                await new Promise(resolve => setTimeout(resolve, 1500));
                const mockSummary = `今日北向资金净流入 73.47 亿，外资这是又来"抄底"了？别高兴太早，这帮老狐狸上周刚跑路，今天回来不过是低吸高抛的老把戏。

半导体涨疯了，散户们又开始幻想"国产替代"的春天。醒醒吧，这轮上涨不是你能吃到的，等你追进去，大概率就是接盘侠的命运。

建议：今日不动如山，看戏就好。真想操作？先去做 20 个波比跳冷静一下再说。`;

                setSummary({
                    ai_summary: mockSummary,
                    generated_at: new Date().toISOString()
                });

                // 即使是 Mock 也保存一下体验会好点
                updateSettings({
                    market_summary: {
                        content: mockSummary,
                        date: new Date().toISOString().split('T')[0]
                    }
                });
            }
        } catch (err: any) {
            console.error('Failed to generate summary:', err);
            toast.error('生成 AI 总结失败');
        } finally {
            setLoadingSummary(false);
        }
    }, [updateSettings]);

    // 刷新所有数据
    const refreshAll = useCallback(() => {
        fetchNorthbound();
        fetchSectors();
        toast.success('数据已刷新');
    }, [fetchNorthbound, fetchSectors]);

    // 初始加载
    useEffect(() => {
        if (hasInitialized.current) return;
        hasInitialized.current = true;

        fetchNorthbound();
        fetchSectors();

        // 自动加载或生成辣评
        const today = new Date().toISOString().split('T')[0];
        // 这里的 settings 可能是旧的（闭包），所以还是得小心。
        // 最稳妥的是直接读取 store 的最新状态，或者依赖 settings 但加锁
        const currentSettings = useUserStore.getState().settings;

        if (currentSettings.market_summary && currentSettings.market_summary.date === today) {
            setSummary({
                ai_summary: currentSettings.market_summary.content,
                generated_at: new Date().toISOString() // 暂用当前时间
            });
        } else {
            // 自动生成
            generateSummary();
        }
    }, []); // 真正的只执行一次

    return (
        <div className="space-y-8">
            {/* 头部操作栏 */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">市场雷达</h1>
                    <p className="text-base text-gray-600 dark:text-gray-400">追踪聪明钱的动向，洞察市场机会</p>
                </div>
                <div className="flex gap-3">
                    {usingMockData && (
                        <Badge variant="outline" className="text-orange-600 border-orange-300 bg-orange-50 dark:bg-orange-950">
                            <Database className="w-3 h-3 mr-1" />
                            模拟数据
                        </Badge>
                    )}
                    <Button variant="outline" onClick={refreshAll} className="gap-2">
                        <RefreshCw className="w-4 h-4" />
                        <span className="hidden sm:inline">刷新</span>
                    </Button>
                    <Button
                        onClick={generateSummary}
                        disabled={loadingSummary}
                        className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 shadow-md gap-2"
                    >
                        {loadingSummary ? '生成中...' : '重新生成 AI 辣评'}
                    </Button>
                </div>
            </div>

            {/* 主内容区 */}
            <div className="grid gap-8 lg:grid-cols-3">
                {/* 左列：北向资金 + 情绪指数 */}
                <div className="lg:col-span-1 space-y-8">
                    <NorthboundCard data={northbound} isLoading={loadingNorthbound} />

                    {/* 情绪指数小卡片 */}
                    <div className="bg-white dark:bg-gray-900 rounded-xl p-6 shadow-md border border-gray-100 dark:border-gray-800 flex flex-col justify-center relative overflow-hidden group hover:shadow-lg transition-all duration-300">
                        <div className="flex items-center justify-between mb-4 relative z-10">
                            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center gap-2">
                                <Gauge className="w-4 h-4" /> 韭菜恐慌指数
                            </h3>
                            <Badge variant="outline" className="bg-red-50 text-red-600 border-red-200">极度恐慌</Badge>
                        </div>

                        <div className="flex items-baseline gap-2 mb-4 relative z-10">
                            <span className="text-5xl font-bold text-gray-900 dark:text-white tracking-tighter">12</span>
                            <span className="text-sm text-gray-400 font-medium">/ 100</span>
                        </div>

                        <div className="w-full bg-gray-100 dark:bg-gray-800 h-3 rounded-full overflow-hidden relative z-10">
                            <div
                                className="bg-gradient-to-r from-green-500 via-yellow-400 to-red-500 h-full rounded-full transition-all duration-1000"
                                style={{ width: '12%' }}
                            />
                        </div>

                        <div className="flex justify-between text-xs text-gray-400 mt-2 relative z-10">
                            <span>0 (甚至不敢看账户)</span>
                            <span>100 (贷款加仓)</span>
                        </div>

                        {/* 装饰背景 */}
                        <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/5 rounded-full blur-3xl group-hover:bg-red-500/10 transition-colors" />
                    </div>
                </div>

                {/* 右列：热门板块 (限制高度) */}
                <div className="lg:col-span-2">
                    <HotSectorsTable data={sectors} isLoading={loadingSectors} />
                </div>
            </div>

            {/* AI 总结 - 全宽 */}
            <AiMarketSummary
                summary={summary?.ai_summary || ''}
                generatedAt={summary?.generated_at}
                isLoading={loadingSummary}
            />
        </div>
    );
}
