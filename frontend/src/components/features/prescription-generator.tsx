'use client';

import { useState, useEffect, useRef } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Loader2, TrendingUp, Dumbbell, Brain, Sprout, RefreshCw, Download } from 'lucide-react';
import { toast } from 'sonner';
import { toPng } from 'html-to-image';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { PrescriptionService } from '@/services/prescription';
import { useUserStore } from '@/store/user';
import { formatCurrency, formatPercent } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';

const formSchema = z.object({
    total_assets: z.coerce.number().min(1, '本金必须大于0'),
    amount: z.coerce.number(),
});

export function PrescriptionGenerator() {
    const [result, setResult] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isDownloading, setIsDownloading] = useState(false);
    const { settings, updateSettings } = useUserStore();

    // 用于截图的 Ref
    const resultRef = useRef<HTMLDivElement>(null);

    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {
            total_assets: 0,
            amount: 0,
        },
    });

    const hasRecordToday = !!(settings.today_record && settings.record_date === new Date().toISOString().split('T')[0]);

    useEffect(() => {
        if (settings.total_assets && form.getValues('total_assets') === 0) {
            form.setValue('total_assets', settings.total_assets);
        }

        if (hasRecordToday) {
            setResult(settings.today_record);
            form.setValue('amount', settings.today_record.amount);
            // 注意：不覆盖 total_assets，那是历史值。这里只做简单回填。
        }
    }, [settings, form, hasRecordToday]);

    async function onSubmit(values: z.infer<typeof formSchema>) {
        setIsLoading(true);
        try {
            const apiKey = localStorage.getItem('siliconflow_api_key') || '';
            const today = new Date().toISOString().split('T')[0];
            const exercises = settings.exercises || [];

            const res = await PrescriptionService.generate({
                ...values,
                api_key: apiKey,
                exercises: exercises.length > 0 ? exercises : undefined
            });

            if (hasRecordToday) {
                const newRecord = {
                    ...settings.today_record,
                    mood: res.mood,
                    exercise: res.exercise,
                    advice: res.advice,
                    full: res.full
                };

                setResult(newRecord);
                updateSettings({
                    today_record: newRecord
                });
                toast.success('AI 建议已刷新 (账面数据未变)');
            } else {
                const newTotalAssets = values.total_assets + values.amount;
                setResult(res);
                updateSettings({
                    total_assets: newTotalAssets,
                    today_record: res,
                    record_date: today,
                });
                toast.success(`处方已生成! 明日本金已更新为 ¥${newTotalAssets}`);
            }

        } catch (error: any) {
            // 临时模拟结果 (开发用)
            if (process.env.NODE_ENV === 'development') {
                const mockRes = {
                    amount: values.amount,
                    total_assets: values.total_assets,
                    roi: (values.amount / values.total_assets) * 100,
                    mood: "模拟上头",
                    exercise: "深蹲×20 (模拟)",
                    advice: "这是模拟数据，请配置 API Key 以获取真实毒舌建议。",
                    full: ""
                };
                if (hasRecordToday) {
                    const newRecord = { ...settings.today_record, ...mockRes };
                    setResult(newRecord);
                    updateSettings({ today_record: newRecord });
                } else {
                    setResult(mockRes);
                    // 不更新 Store 以免脏数据
                }
                toast.warning('使用了模拟数据 (无 API Key 或请求失败)');
            } else {
                toast.error(error.detail || '生成失败');
            }
        } finally {
            setIsLoading(false);
        }
    }

    const handleDownload = async () => {
        if (!resultRef.current) return;
        setIsDownloading(true);

        try {
            // 使用 html-to-image 直接生成 PNG
            const dataUrl = await toPng(resultRef.current, {
                quality: 1,
                pixelRatio: 2,
                backgroundColor: '#ffffff',
                style: {
                    // 移除可能导致问题的样式
                    backdropFilter: 'none',
                    boxShadow: 'none',
                },
            });

            const link = document.createElement('a');
            link.download = `stoic-leek-card-${new Date().toISOString().split('T')[0]}.png`;
            link.href = dataUrl;
            link.click();
            toast.success('分享卡片已保存', { duration: 3000 });
        } catch (err: any) {
            console.error('生成图片错误:', err);
            toast.error(`生成图片失败: ${err?.message || '未知错误'}`, {
                duration: 8000,
                dismissible: true
            });
        } finally {
            setIsDownloading(false);
        }
    };

    return (
        <div className="grid gap-6 md:grid-cols-2">
            {/* 左侧：输入区 */}
            <Card className="border-0 shadow-lg bg-white/70 backdrop-blur-md dark:bg-gray-900/50">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-blue-500" />
                        输入今日战绩
                    </CardTitle>
                    <CardDescription>诚实面对你的贪婪与恐惧</CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                            <FormField
                                control={form.control}
                                name="total_assets"
                                render={({ field }) => {
                                    const { value, onChange, ...fieldProps } = field;
                                    return (
                                        <FormItem>
                                            <FormLabel>当前本金 (元)</FormLabel>
                                            <FormControl>
                                                <div className="relative">
                                                    <span className="absolute left-3 top-2.5 text-gray-400">¥</span>
                                                    <Input
                                                        className="pl-7 bg-white/50"
                                                        placeholder="10000"
                                                        type="number"
                                                        {...fieldProps}
                                                        value={(value ?? '') as string | number}
                                                        onChange={onChange}
                                                        disabled={hasRecordToday}
                                                    />
                                                </div>
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    );
                                }}
                            />

                            <FormField
                                control={form.control}
                                name="amount"
                                render={({ field }) => {
                                    const { value, onChange, ...fieldProps } = field;
                                    return (
                                        <FormItem>
                                            <FormLabel>今日盈亏 (元)</FormLabel>
                                            <FormControl>
                                                <div className="relative">
                                                    <span className="absolute left-3 top-2.5 text-gray-400">¥</span>
                                                    <Input
                                                        className="pl-7 bg-white/50"
                                                        placeholder="正数盈利，负数亏损"
                                                        type="number"
                                                        {...fieldProps}
                                                        value={(value ?? '') as string | number}
                                                        onChange={(e) => onChange(e.target.valueAsNumber || 0)}
                                                        disabled={hasRecordToday}
                                                    />
                                                </div>
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    );
                                }}
                            />

                            <Button
                                type="submit"
                                className={`w-full shadow-lg ${hasRecordToday
                                    ? "bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 shadow-orange-500/20"
                                    : "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-blue-500/20"
                                    }`}
                                disabled={isLoading}
                            >
                                {isLoading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        AI 思考中...
                                    </>
                                ) : hasRecordToday ? (
                                    <>
                                        <RefreshCw className="mr-2 h-4 w-4" />
                                        重新生成 AI 建议 (不改账本)
                                    </>
                                ) : (
                                    '生成对冲处方'
                                )}
                            </Button>

                            {hasRecordToday && (
                                <p className="text-xs text-center text-gray-400">
                                    今日账本已锁定，明天继续加油。
                                </p>
                            )}
                        </form>
                    </Form>
                </CardContent>
            </Card>

            {/* 右侧：结果区 */}
            <div className="space-y-6">
                {result ? (
                    <div className="animate-in slide-in-from-bottom-4 duration-500 fade-in space-y-6">
                        {/* 截图区域 */}
                        <div
                            ref={resultRef}
                            className="space-y-6 p-8 rounded-2xl bg-white shadow-xl border border-gray-100"
                            style={{ position: 'relative' }}
                        >
                            {/* 水印/Logo */}
                            <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-100">
                                <div className="flex items-center gap-2">
                                    <img src="/logo.png" alt="Logo" className="w-8 h-8 rounded-lg shadow-sm" />
                                    <span className="text-sm font-bold tracking-widest text-gray-700">THE STOIC LEEK</span>
                                </div>
                                <span className="text-xs text-gray-400 font-mono">{new Date().toLocaleDateString()}</span>
                            </div>

                            {/* 数据卡片 */}
                            <div className="grid grid-cols-3 gap-4">
                                <Card className="bg-gray-50 border-0 flex flex-col items-center justify-center p-4">
                                    <div className={`text-2xl font-bold flex items-center justify-center gap-0.5 ${result.amount >= 0 ? 'text-red-500' : 'text-green-500'}`}>
                                        {result.amount > 0 && <span>+</span>}
                                        <span>{formatCurrency(result.amount)}</span>
                                    </div>
                                    <div className="text-xs text-gray-500 mt-1">今日盈亏</div>
                                </Card>
                                <Card className="bg-gray-50 border-0 flex flex-col items-center justify-center p-4">
                                    <div className={`text-2xl font-bold ${result.roi >= 0 ? 'text-red-500' : 'text-green-500'}`}>
                                        {formatPercent(result.roi)}
                                    </div>
                                    <div className="text-xs text-gray-500 mt-1">收益率</div>
                                </Card>
                                <Card className="bg-gray-50 border-0 flex flex-col items-center justify-center p-4">
                                    <div className="text-xl font-bold text-blue-600">{result.mood}</div>
                                    <div className="text-xs text-gray-500 mt-1">AI 诊断</div>
                                </Card>
                            </div>

                            {/* 运动处方 */}
                            <Card className="border-l-4 border-l-blue-500 shadow-sm bg-gradient-to-br from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-medium flex items-center gap-2 text-blue-700 dark:text-blue-300">
                                        <Dumbbell className="w-4 h-4" /> 运动处方
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-lg font-bold text-gray-800 dark:text-gray-100">
                                        {result.exercise}
                                    </div>
                                </CardContent>
                            </Card>

                            {/* AI 建议 */}
                            <Card className="border-l-4 border-l-purple-500 shadow-sm bg-gradient-to-br from-purple-50 to-white dark:from-gray-900 dark:to-gray-800">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-medium flex items-center gap-2 text-purple-700 dark:text-purple-300">
                                        <Brain className="w-4 h-4" /> 毒舌建议
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-md text-gray-700 dark:text-gray-300 leading-relaxed italic">
                                        "{result.advice}"
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* 下载按钮 */}
                        <Button
                            variant="outline"
                            className="w-full gap-2 transition-all active:scale-95"
                            onClick={handleDownload}
                            disabled={isDownloading}
                        >
                            {isDownloading ? (
                                <>
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    生成图片中...
                                </>
                            ) : (
                                <>
                                    <Download className="w-4 h-4" />
                                    保存分享卡片
                                </>
                            )}
                        </Button>
                    </div>
                ) : (
                    <div className="h-full min-h-[300px] flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-xl bg-white/30">
                        <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
                            <Sprout className="w-8 h-8 text-gray-400" />
                        </div>
                        <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">等待投喂数据</h3>
                        <p className="text-sm text-gray-500 mt-2 max-w-xs">
                            在左侧输入你的投资战绩，AI 将为你生成专属的身心对冲方案。
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
