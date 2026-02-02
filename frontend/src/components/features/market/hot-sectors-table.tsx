'use client';

import { TrendingUp, TrendingDown, Flame, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface SectorData {
    name: string;
    change_pct: number;
    leading_stocks: string[];
}

interface HotSectorsTableProps {
    data: SectorData[];
    isLoading?: boolean;
}

export function HotSectorsTable({ data, isLoading }: HotSectorsTableProps) {
    if (isLoading) {
        return (
            <Card className="border-0 shadow-lg bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
                <CardContent className="flex items-center justify-center h-64">
                    <Loader2 className="w-8 h-8 animate-spin text-purple-500" />
                </CardContent>
            </Card>
        );
    }

    // 分离涨跌板块
    const gainers = data.filter(s => s.change_pct > 0).slice(0, 5);
    const losers = data.filter(s => s.change_pct < 0).sort((a, b) => a.change_pct - b.change_pct).slice(0, 5);

    return (
        <div className="h-full p-6 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800">
            <div className="pb-4 flex items-center gap-2">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center shadow-sm">
                    <Flame className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-semibold">今日板块热力图</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-[360px] overflow-y-auto pr-2 custom-scrollbar">
                {/* 涨幅榜 */}
                <div>
                    <div className="flex items-center gap-2 mb-3">
                        <TrendingUp className="w-4 h-4 text-red-500" />
                        <span className="text-sm font-medium text-red-600">领涨板块</span>
                    </div>
                    <div className="space-y-2">
                        {gainers.map((sector, index) => (
                            <div
                                key={sector.name}
                                className={cn(
                                    "flex items-center justify-between p-3 rounded-lg transition-all duration-200",
                                    "bg-gradient-to-r from-red-50 to-transparent dark:from-red-950/30 dark:to-transparent",
                                    "hover:from-red-100 hover:to-red-50 dark:hover:from-red-900/40"
                                )}
                            >
                                <div className="flex items-center gap-3">
                                    <span className={cn(
                                        "w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold",
                                        index === 0 ? "bg-red-500 text-white" : "bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300"
                                    )}>
                                        {index + 1}
                                    </span>
                                    <span className="font-medium text-gray-800 dark:text-gray-200">{sector.name}</span>
                                </div>
                                <Badge className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300 hover:bg-red-200">
                                    +{sector.change_pct.toFixed(2)}%
                                </Badge>
                            </div>
                        ))}
                    </div>
                </div>

                {/* 跌幅榜 */}
                <div>
                    <div className="flex items-center gap-2 mb-3">
                        <TrendingDown className="w-4 h-4 text-green-500" />
                        <span className="text-sm font-medium text-green-600">领跌板块</span>
                    </div>
                    <div className="space-y-2">
                        {losers.map((sector, index) => (
                            <div
                                key={sector.name}
                                className={cn(
                                    "flex items-center justify-between p-3 rounded-lg transition-all duration-200",
                                    "bg-gradient-to-r from-green-50 to-transparent dark:from-green-950/30 dark:to-transparent",
                                    "hover:from-green-100 hover:to-green-50 dark:hover:from-green-900/40"
                                )}
                            >
                                <div className="flex items-center gap-3">
                                    <span className={cn(
                                        "w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold",
                                        index === 0 ? "bg-green-500 text-white" : "bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300"
                                    )}>
                                        {index + 1}
                                    </span>
                                    <span className="font-medium text-gray-800 dark:text-gray-200">{sector.name}</span>
                                </div>
                                <Badge className="bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 hover:bg-green-200">
                                    {sector.change_pct.toFixed(2)}%
                                </Badge>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
