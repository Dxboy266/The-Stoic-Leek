'use client';

import { useState, useEffect } from 'react';
import { Dumbbell, RotateCcw } from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useUserStore } from '@/store/user';
import { cn } from '@/lib/utils';
import { AIConfigCard } from './ai-config-card';
import { savePersistence } from '@/services/persistence';

const EXERCISE_POOL = [
    "波比跳 (Burpees)",
    "深蹲 (Squats)",
    "俯卧撑 (Push-ups)",
    "平板支撑 (Plank)",
    "卷腹 (Crunches)",
    "开合跳 (Jumping Jacks)",
    "弓步蹲 (Lunges)",
    "高抬腿 (High Knees)",
    "靠墙静蹲 (Wall Sit)"
];

export function SettingsPage() {
    const [newExercise, setNewExercise] = useState('');

    // 动作池设置
    const { settings, updateSettings } = useUserStore();
    const selectedExercises = settings.exercises || EXERCISE_POOL;

    useEffect(() => {
        // 如果 Store 里没有 exercises，初始化为全部
        if (!settings.exercises) {
            updateSettings({ exercises: EXERCISE_POOL });
        }
    }, [settings.exercises, updateSettings]);

    const toggleExercise = (ex: string) => {
        let newExercises;
        if (selectedExercises.includes(ex)) {
            // 不允许清空所有动作，至少保留一个
            if (selectedExercises.length <= 1) {
                toast.error('韭菜也是要有底线的，至少保留一个惩罚动作！');
                return;
            }
            newExercises = selectedExercises.filter(e => e !== ex);
        } else {
            newExercises = [...selectedExercises, ex];
        }
        updateSettings({ exercises: newExercises });
    };

    const resetExercises = () => {
        updateSettings({ exercises: EXERCISE_POOL });
        toast.success('动作池已重置');
    };

    const handleAddExercise = () => {
        const value = newExercise.trim();
        if (!value) return;

        if (selectedExercises.includes(value)) {
            toast.error('该动作已存在');
            return;
        }

        updateSettings({ exercises: [...selectedExercises, value] });
        setNewExercise('');
        toast.success(`已添加动作: ${value}`);
    };

    // 保存设置
    const handleSaveSettings = async () => {
        // 数据会自动通过 Store 监听保存到 LocalStorage
        toast.success('设置已保存');
    };

    return (
        <div className="space-y-6 sm:space-y-8 max-w-2xl mx-auto">
            <div>
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100 mb-1 sm:mb-2">设置</h1>
                <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400">配置你的 AI 和战术偏好</p>
            </div>

            {/* AI 配置卡片 */}
            <AIConfigCard onSave={handleSaveSettings} />

            {/* 动作池配置 */}
            <Card className="border-0 shadow-lg">
                <CardHeader className="flex flex-row items-center justify-between">
                    <div>
                        <CardTitle className="flex items-center gap-2">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center">
                                <Dumbbell className="w-5 h-5 text-white" />
                            </div>
                            动作惩罚池
                        </CardTitle>
                        <CardDescription className="mt-2">
                            AI 会从选中的动作中为你开具运动处方。
                        </CardDescription>
                    </div>
                    <Button variant="ghost" size="sm" onClick={resetExercises} className="text-gray-500">
                        <RotateCcw className="w-4 h-4 mr-1" /> 重置
                    </Button>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-wrap gap-3 mb-6">
                        {Array.from(new Set([...EXERCISE_POOL, ...selectedExercises])).map((ex) => {
                            const isSelected = selectedExercises.includes(ex);
                            return (
                                <button
                                    key={ex}
                                    onClick={() => toggleExercise(ex)}
                                    className={cn(
                                        "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border",
                                        isSelected
                                            ? "bg-blue-100 border-blue-200 text-blue-700 dark:bg-blue-900/40 dark:border-blue-800 dark:text-blue-300 shadow-sm"
                                            : "bg-white border-gray-200 text-gray-500 hover:border-blue-200 hover:text-blue-500 dark:bg-gray-900 dark:border-gray-800 dark:text-gray-400"
                                    )}
                                >
                                    {ex}
                                </button>
                            );
                        })}
                    </div>

                    <div className="flex gap-2">
                        <Input
                            placeholder="输入新动作 (如: 登山跑)"
                            value={newExercise}
                            onChange={(e) => setNewExercise(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleAddExercise()}
                            className="max-w-xs"
                        />
                        <Button variant="secondary" onClick={handleAddExercise} disabled={!newExercise.trim()}>
                            添加
                        </Button>
                    </div>

                    <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-sm text-blue-700 dark:text-blue-300">
                        <p>
                            当前已选中 {selectedExercises.length} 个动作。当你亏损时，AI 将混合这些动作让你冷静一下。
                        </p>
                    </div>
                </CardContent>
            </Card>

            {/* 数据存储说明 */}
            <Card className="border-0 shadow-lg">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
                            <span className="text-white text-lg">💾</span>
                        </div>
                        数据存储
                    </CardTitle>
                    <CardDescription>
                        数据仅保存在你的浏览器 (LocalStorage)。不会上传到服务器，每个人数据互相独立。
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg text-sm text-yellow-800 dark:text-yellow-200">
                        <p>
                            ⚠️ 注意：如果你清理浏览器缓存或更换浏览器，数据将会丢失。请妥善保管你的 AI Key。
                        </p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
