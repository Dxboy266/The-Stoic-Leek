'use client';

import { Brain, Loader2, Sparkles, Quote } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface AiMarketSummaryProps {
    summary: string;
    generatedAt?: string;
    isLoading?: boolean;
}

export function AiMarketSummary({ summary, generatedAt, isLoading }: AiMarketSummaryProps) {
    if (isLoading) {
        return (
            <Card className="border-0 shadow-lg bg-gradient-to-br from-purple-50 via-violet-50 to-indigo-100 dark:from-purple-950 dark:via-violet-950 dark:to-indigo-900">
                <CardContent className="flex flex-col items-center justify-center h-48 gap-3">
                    <Loader2 className="w-8 h-8 animate-spin text-purple-500" />
                    <p className="text-sm text-purple-600 dark:text-purple-300">AI 正在分析市场...</p>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="border-0 shadow-xl bg-gradient-to-br from-purple-50 via-violet-50 to-indigo-100 dark:from-purple-950 dark:via-violet-950 dark:to-indigo-900 overflow-hidden relative">
            {/* 装饰背景 */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-200/50 to-transparent rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-indigo-200/50 to-transparent rounded-full blur-2xl" />

            <CardHeader className="pb-2 relative z-10">
                <CardTitle className="text-lg font-semibold flex items-center gap-2">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center shadow-lg">
                        <Brain className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex flex-col">
                        <span className="text-gray-800 dark:text-gray-100">AI 市场辣评</span>
                        <span className="text-xs font-normal text-gray-500">斯多葛策略分析</span>
                    </div>
                    <Sparkles className="w-5 h-5 text-yellow-500 ml-auto animate-pulse" />
                </CardTitle>
            </CardHeader>
            <CardContent className="relative z-10">
                <div className="relative">
                    {/* 引号装饰 */}
                    <Quote className="absolute -top-2 -left-2 w-8 h-8 text-purple-200 dark:text-purple-800 rotate-180" />

                    <div className="pl-6 pr-4 py-2">
                        <p className="text-gray-700 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">
                            {summary || "等待 AI 生成今日市场点评..."}
                        </p>
                    </div>

                    <Quote className="absolute -bottom-2 -right-2 w-8 h-8 text-purple-200 dark:text-purple-800" />
                </div>

                {generatedAt && (
                    <p className="text-xs text-gray-400 mt-4 text-right">
                        生成于 {new Date(generatedAt).toLocaleTimeString('zh-CN')}
                    </p>
                )}
            </CardContent>
        </Card>
    );
}
