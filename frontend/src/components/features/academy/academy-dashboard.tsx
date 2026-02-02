'use client';

import { useState } from 'react';
import { Flame, Trophy, Star } from 'lucide-react';
import { toast } from 'sonner';
import { UnitCard } from './unit-card';
import { LessonViewer } from './lesson-viewer';
import { ACADEMY_DATA, Lesson } from './data';

export function AcademyDashboard() {
    const [activeLesson, setActiveLesson] = useState<Lesson | null>(null);

    // 模拟用户进度
    const stats = {
        xp: 1250,
        streak: 3,
        level: 2
    };

    const handleLessonComplete = (lessonId: string) => {
        toast.success('恭喜！课程已完成 +50 XP');
        setActiveLesson(null);
        // 这里未来应该调用 API 更新用户进度 State
    };

    return (
        <div className="space-y-8">
            {/* 头部状态栏 */}
            <div className="flex items-center justify-between bg-white dark:bg-gray-900 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800">
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-2 text-orange-500">
                        <Flame className="fill-orange-500 w-5 h-5" />
                        <span className="font-bold text-lg">{stats.streak}</span>
                        <span className="text-xs text-muted-foreground">天连胜</span>
                    </div>
                    <div className="flex items-center gap-2 text-yellow-500">
                        <Star className="fill-yellow-500 w-5 h-5" />
                        <span className="font-bold text-lg">{stats.xp}</span>
                        <span className="text-xs text-muted-foreground">XP</span>
                    </div>
                </div>
                <div className="flex items-center gap-2 text-purple-600">
                    <Trophy className="w-5 h-5" />
                    <span className="text-sm font-semibold">Level {stats.level} 韭菜苗</span>
                </div>
            </div>

            {/* 课程地图 */}
            <div className="grid gap-8 max-w-2xl mx-auto">
                {ACADEMY_DATA.map((unit) => (
                    <UnitCard
                        key={unit.id}
                        unit={unit}
                        onLessonSelect={setActiveLesson}
                    />
                ))}
            </div>

            {/* 底部提示 */}
            <div className="text-center text-sm text-gray-400 py-8">
                更多课程正在生成中...
            </div>

            {/* 课程查看器 */}
            <LessonViewer
                lesson={activeLesson}
                isOpen={!!activeLesson}
                onClose={() => setActiveLesson(null)}
                onComplete={handleLessonComplete}
            />
        </div>
    );
}
