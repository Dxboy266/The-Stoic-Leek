'use client';

import { TrendingUp, TrendingDown, Clock, Trash2, Edit3 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { FundRealtime, FundHolding, calculateChange, calculateMarketValue } from '@/hooks/use-fund';

interface FundCardProps {
    fund: FundRealtime;
    holding?: FundHolding;
    onDelete?: (code: string) => void;
    onEdit?: (code: string, shares: number) => void;
}

export function FundCard({ fund, holding, onDelete, onEdit }: FundCardProps) {
    const isPositive = fund.gszzl >= 0;
    const Icon = isPositive ? TrendingUp : TrendingDown;

    // 计算盈亏
    const shares = holding?.shares || 0;
    const changeAmount = shares > 0 ? calculateChange(fund, shares) : 0;
    const marketValue = shares > 0 ? calculateMarketValue(fund, shares) : 0;

    return (
        <Card className={cn(
            "border-0 shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl hover:scale-[1.01]",
            isPositive
                ? "bg-gradient-to-br from-red-50 via-rose-50 to-pink-50 dark:from-red-950/50 dark:to-rose-900/50"
                : "bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 dark:from-green-950/50 dark:to-emerald-900/50"
        )}>
            <CardContent className="p-4">
                {/* 头部：基金名称和代码 */}
                <div className="flex items-start justify-between mb-3">
                    <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-900 dark:text-gray-100 truncate text-base">
                            {fund.name}
                        </h3>
                        <p className="text-xs text-gray-500 mt-0.5">{fund.code}</p>
                    </div>
                    <div className="flex items-center gap-1">
                        <div className={cn(
                            "w-8 h-8 rounded-lg flex items-center justify-center",
                            isPositive ? "bg-red-500/20" : "bg-green-500/20"
                        )}>
                            <Icon className={cn("w-4 h-4", isPositive ? "text-red-600" : "text-green-600")} />
                        </div>
                        {onEdit && holding && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => onEdit(fund.code, holding.shares)}
                                className="h-8 w-8 p-0 text-gray-400 hover:text-blue-500 hover:bg-blue-50"
                                title="修改份额"
                            >
                                <Edit3 className="w-4 h-4" />
                            </Button>
                        )}
                        {onDelete && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => onDelete(fund.code)}
                                className="h-8 w-8 p-0 text-gray-400 hover:text-red-500 hover:bg-red-50"
                                title="删除"
                            >
                                <Trash2 className="w-4 h-4" />
                            </Button>
                        )}
                    </div>
                </div>

                {/* 估值和涨跌幅 */}
                <div className="grid grid-cols-2 gap-4 mb-3">
                    <div>
                        <p className="text-xs text-gray-500 mb-1">实时估值</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">
                            ¥{fund.gsz.toFixed(4)}
                        </p>
                    </div>
                    <div className="text-right">
                        <p className="text-xs text-gray-500 mb-1">涨跌幅</p>
                        <p className={cn(
                            "text-2xl font-bold",
                            isPositive ? "text-red-600 dark:text-red-400" : "text-green-600 dark:text-green-400"
                        )}>
                            {isPositive ? '+' : ''}{fund.gszzl.toFixed(2)}%
                        </p>
                    </div>
                </div>

                {/* 持仓信息（如果有） */}
                {shares > 0 && (
                    <div className="grid grid-cols-2 gap-4 p-3 rounded-lg bg-white/60 dark:bg-gray-800/60">
                        <div>
                            <p className="text-xs text-gray-500 mb-1">持仓市值</p>
                            <p className="font-semibold text-gray-900 dark:text-white">
                                ¥{marketValue.toFixed(2)}
                            </p>
                            <p className="text-xs text-gray-400 mt-0.5">{shares.toFixed(2)} 份</p>
                        </div>
                        <div className="text-right">
                            <p className="text-xs text-gray-500 mb-1">今日盈亏</p>
                            <p className={cn(
                                "font-semibold",
                                changeAmount >= 0 ? "text-red-600" : "text-green-600"
                            )}>
                                {changeAmount >= 0 ? '+' : ''}¥{changeAmount.toFixed(2)}
                            </p>
                        </div>
                    </div>
                )}

                {/* 更新时间 */}
                <div className="flex items-center justify-end mt-3 text-xs text-gray-400">
                    <Clock className="w-3 h-3 mr-1" />
                    {fund.gztime || '暂无更新'}
                </div>
            </CardContent>
        </Card>
    );
}
