'use client';

import { useState, useEffect } from 'react';
import { Key, Dumbbell, RotateCcw } from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useUserStore } from '@/store/user';
import { cn } from '@/lib/utils';

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

    return (
        <div className="space-y-8 max-w-2xl mx-auto">
            <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">设置</h1>
                <p className="text-base text-gray-600 dark:text-gray-400">配置你的 AI 和战术偏好</p>
            </div>

            {/* API Key 配置 - 编辑 .env 文件 */}
            <Card className="border-0 shadow-lg">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center">
                            <Key className="w-5 h-5 text-white" />
                        </div>
                        SiliconFlow API Key
                    </CardTitle>
                    <CardDescription>
                        用于生成 AI 毒舌建议和市场辣评。
                        <a
                            href="https://cloud.siliconflow.cn/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline ml-1"
                        >
                            点击获取免费 API Key →
                        </a>
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="p-4 bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg">
                        <p className="text-sm text-blue-800 dark:text-blue-200 mb-3">
                            <strong>📁 配置方式</strong>：直接编辑后端配置文件
                        </p>
                        <div className="bg-white dark:bg-gray-900 p-3 rounded-md font-mono text-sm border">
                            <p className="text-gray-500 mb-1"># 文件路径</p>
                            <p className="text-blue-600">backend/.env</p>
                            <p className="text-gray-500 mt-3 mb-1"># 添加或修改这一行</p>
                            <p className="text-green-600">SILICONFLOW_API_KEY=sk-你的密钥</p>
                        </div>
                        <p className="text-xs text-gray-500 mt-3">
                            修改后需要重启后端服务 (重新运行 start_backend.bat)
                        </p>
                    </div>
                    <div className="p-3 bg-yellow-50 dark:bg-yellow-950/50 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                        <p className="text-sm text-yellow-700 dark:text-yellow-300">
                            💡 没有 API Key 也能使用基础功能（盈亏对冲），但无法生成 AI 个性化建议和市场辣评。
                        </p>
                    </div>
                </CardContent>
            </Card>

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
                        所有数据都保存在本地文件，不上传任何服务器
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="p-4 bg-gray-50 dark:bg-gray-800 border rounded-lg font-mono text-sm">
                        <p className="text-gray-500 mb-1"># 用户数据文件</p>
                        <p className="text-blue-600">backend/stoic_leek_data.json</p>
                        <p className="text-gray-500 mt-3 mb-1"># API 密钥文件</p>
                        <p className="text-blue-600">backend/.env</p>
                    </div>
                    <p className="text-xs text-gray-500 mt-3">
                        你可以直接编辑这些文件来修改数据。修改 .env 后需要重启后端。
                    </p>
                </CardContent>
            </Card>
        </div>
    );
}
