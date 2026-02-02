'use client';

import { useState } from 'react';
import { Lock, CheckCircle2, PlayCircle, BookOpen, Brain, Zap, ChevronDown, ChevronUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { Unit, Chapter, Lesson } from './data';

interface UnitCardProps {
    unit: Unit;
    onLessonSelect: (lesson: Lesson) => void;
}

export function UnitCard({ unit, onLessonSelect }: UnitCardProps) {
    const isLocked = unit.isLocked;
    const [expandedChapter, setExpandedChapter] = useState<string | null>(null);

    // 默认展开第一个章节
    useState(() => {
        if (unit.chapters.length > 0) {
            setExpandedChapter(unit.chapters[0].id);
        }
    });

    return (
        <Card className={cn(
            "border-0 shadow-lg overflow-hidden transition-all duration-300",
            isLocked ? "opacity-60 grayscale" : "hover:shadow-xl"
        )}>
            {/* Unit Header */}
            <div className={cn(
                "p-6 flex items-start justify-between",
                unit.color === 'blue' && "bg-gradient-to-r from-blue-500 to-cyan-500 text-white",
                unit.color === 'purple' && "bg-gradient-to-r from-purple-500 to-indigo-500 text-white",
                unit.color === 'red' && "bg-gradient-to-r from-red-500 to-orange-500 text-white",
                isLocked && "bg-gray-200 dark:bg-gray-800 text-gray-500"
            )}>
                <div>
                    <h3 className="text-lg font-bold tracking-tight">{unit.title}</h3>
                    <p className="text-sm opacity-90 mt-1">{unit.description}</p>
                </div>
                <div className="text-4xl">{unit.icon}</div>
            </div>

            {/* Chapters */}
            <CardContent className="p-0 bg-white dark:bg-gray-900">
                {isLocked ? (
                    <div className="p-8 flex flex-col items-center justify-center text-gray-400 gap-2">
                        <Lock className="w-8 h-8" />
                        <span className="text-sm">完成上一单元以解锁</span>
                    </div>
                ) : (
                    <div className="divide-y divide-gray-100 dark:divide-gray-800">
                        {unit.chapters.map((chapter, index) => (
                            <div key={chapter.id}>
                                {/* Chapter Header */}
                                <button
                                    onClick={() => setExpandedChapter(expandedChapter === chapter.id ? null : chapter.id)}
                                    className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors text-left"
                                >
                                    <div className="flex flex-col">
                                        <span className="font-semibold text-sm">Chapter {index + 1}: {chapter.title}</span>
                                        <span className="text-xs text-muted-foreground font-normal">{chapter.description}</span>
                                    </div>
                                    {expandedChapter === chapter.id ? (
                                        <ChevronUp className="w-5 h-5 text-gray-400" />
                                    ) : (
                                        <ChevronDown className="w-5 h-5 text-gray-400" />
                                    )}
                                </button>

                                {/* Chapter Content */}
                                {expandedChapter === chapter.id && (
                                    <div className="px-6 pb-4 space-y-1 animate-in fade-in slide-in-from-top-2 duration-200">
                                        {chapter.lessons.map((lesson) => (
                                            <LessonItem
                                                key={lesson.id}
                                                lesson={lesson}
                                                onClick={() => onLessonSelect(lesson)}
                                            />
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </CardContent>
        </Card>
    );
}

function LessonItem({ lesson, onClick }: { lesson: Lesson; onClick: () => void }) {
    const getIcon = () => {
        switch (lesson.type) {
            case 'video': return <PlayCircle className="w-4 h-4" />;
            case 'quiz': return <Brain className="w-4 h-4" />;
            case 'flashcard': return <Zap className="w-4 h-4" />;
            case 'article': return <BookOpen className="w-4 h-4" />;
        }
    };

    return (
        <div
            onClick={() => !lesson.isLocked && onClick()}
            className={cn(
                "group flex items-center justify-between p-4 rounded-xl border transition-all cursor-pointer mb-2",
                lesson.isCompleted
                    ? "bg-green-50/50 border-green-100 text-green-700 dark:bg-green-900/10 dark:border-green-900/20 dark:text-green-300"
                    : "bg-white dark:bg-gray-800 border-gray-100 dark:border-gray-700 hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-md hover:-translate-y-0.5",
                lesson.isLocked && "opacity-50 grayscale cursor-not-allowed pointer-events-none bg-gray-50 border-gray-100 dark:bg-gray-900"
            )}>
            <div className="flex items-center gap-4">
                <div className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center transition-colors",
                    lesson.isCompleted
                        ? "bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400"
                        : "bg-gray-100 text-gray-500 group-hover:bg-blue-50 group-hover:text-blue-500 dark:bg-gray-700 dark:text-gray-400 dark:group-hover:bg-blue-900/50 dark:group-hover:text-blue-400",
                    lesson.isLocked && "bg-transparent border border-gray-200"
                )}>
                    {lesson.isCompleted ? (
                        <CheckCircle2 className="w-5 h-5" />
                    ) : (
                        getIcon()
                    )}
                </div>
                <div>
                    <p className="text-sm font-semibold group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{lesson.title}</p>
                    <p className="text-xs opacity-70 flex items-center gap-1 mt-0.5">
                        <Badge variant="outline" className="text-[10px] h-4 px-1 py-0">{lesson.type.toUpperCase()}</Badge>
                        <span>• {lesson.duration}</span>
                    </p>
                </div>
            </div>

            {!lesson.isLocked && !lesson.isCompleted && (
                <Button size="sm" className="h-8 rounded-full px-4 text-xs opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
                    开始学习
                </Button>
            )}

            {lesson.isCompleted && (
                <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300">已完成</Badge>
            )}
        </div>
    );
}
