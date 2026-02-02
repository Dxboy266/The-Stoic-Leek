'use client';

import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, ArrowUpRight, ArrowDownRight, RefreshCw, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface NorthboundData {
    date: string;
    shanghai_net: number;
    shenzhen_net: number;
    total_net: number;
    unit: string;
}

interface NorthboundCardProps {
    data: NorthboundData | null;
    isLoading?: boolean;
}

export function NorthboundCard({ data, isLoading }: NorthboundCardProps) {
    if (isLoading) {
        return (
            <Card className="bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 border-0 shadow-lg">
                <CardContent className="flex items-center justify-center h-48">
                    <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
                </CardContent>
            </Card>
        );
    }

    if (!data) {
        return (
            <Card className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 border-0 shadow-lg">
                <CardContent className="flex items-center justify-center h-48">
                    <p className="text-gray-500">暂无数据</p>
                </CardContent>
            </Card>
        );
    }

    const isPositive = data.total_net >= 0;
    const Icon = isPositive ? TrendingUp : TrendingDown;
    const ArrowIcon = isPositive ? ArrowUpRight : ArrowDownRight;

    return (
        <Card className={cn(
            "border-0 shadow-xl overflow-hidden transition-all duration-300 hover:shadow-2xl hover:scale-[1.02]",
            isPositive
                ? "bg-gradient-to-br from-red-50 via-rose-50 to-pink-100 dark:from-red-950 dark:to-rose-900"
                : "bg-gradient-to-br from-green-50 via-emerald-50 to-teal-100 dark:from-green-950 dark:to-emerald-900"
        )}>
            <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                    <CardTitle className="text-lg font-semibold text-gray-800 dark:text-gray-100 flex items-center gap-2">
                        <div className={cn(
                            "w-10 h-10 rounded-xl flex items-center justify-center",
                            isPositive ? "bg-red-500/20" : "bg-green-500/20"
                        )}>
                            <Icon className={cn("w-5 h-5", isPositive ? "text-red-600" : "text-green-600")} />
                        </div>
                        北向资金
                    </CardTitle>
                    <Badge variant="outline" className="text-xs font-normal">
                        {data.date}
                    </Badge>
                </div>
            </CardHeader>
            <CardContent className="pt-2">
                {/* 总体净流入 */}
                <div className="mb-6">
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">当日净流入</p>
                    <div className="flex items-end gap-2">
                        <span className={cn(
                            "text-4xl font-bold tracking-tight",
                            isPositive ? "text-red-600 dark:text-red-400" : "text-green-600 dark:text-green-400"
                        )}>
                            {isPositive ? '+' : ''}{data.total_net.toFixed(2)}
                        </span>
                        <span className="text-lg text-gray-500 mb-1">{data.unit}</span>
                        <ArrowIcon className={cn(
                            "w-6 h-6 mb-1",
                            isPositive ? "text-red-500" : "text-green-500"
                        )} />
                    </div>
                </div>

                {/* 分渠道数据 */}
                <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 rounded-lg bg-white/50 dark:bg-gray-800/50">
                        <p className="text-xs text-gray-500 mb-1">沪股通</p>
                        <p className={cn(
                            "text-lg font-semibold",
                            data.shanghai_net >= 0 ? "text-red-600" : "text-green-600"
                        )}>
                            {data.shanghai_net >= 0 ? '+' : ''}{data.shanghai_net.toFixed(2)}亿
                        </p>
                    </div>
                    <div className="p-3 rounded-lg bg-white/50 dark:bg-gray-800/50">
                        <p className="text-xs text-gray-500 mb-1">深股通</p>
                        <p className={cn(
                            "text-lg font-semibold",
                            data.shenzhen_net >= 0 ? "text-red-600" : "text-green-600"
                        )}>
                            {data.shenzhen_net >= 0 ? '+' : ''}{data.shenzhen_net.toFixed(2)}亿
                        </p>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
