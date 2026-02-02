'use client';

import { useState } from 'react';
import { X, CheckCircle, XCircle, RotateCw, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { Lesson } from './data';

interface LessonViewerProps {
    lesson: Lesson | null;
    isOpen: boolean;
    onClose: () => void;
    onComplete: (lessonId: string) => void;
}

export function LessonViewer({ lesson, isOpen, onClose, onComplete }: LessonViewerProps) {
    if (!lesson) return null;

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="max-w-2xl min-h-[500px] flex flex-col p-0 overflow-hidden">
                <DialogHeader className="p-6 border-b">
                    <DialogTitle className="flex items-center gap-2">
                        <span className="text-xl">{lesson.icon || '📝'}</span>
                        {lesson.title}
                    </DialogTitle>
                </DialogHeader>

                <div className="flex-1 p-6 bg-gray-50 dark:bg-gray-900/50">
                    {lesson.type === 'flashcard' && <FlashcardView lesson={lesson} onComplete={() => onComplete(lesson.id)} />}
                    {lesson.type === 'quiz' && <QuizView lesson={lesson} onComplete={() => onComplete(lesson.id)} />}
                    {lesson.type === 'article' && <ArticleView lesson={lesson} onComplete={() => onComplete(lesson.id)} />}
                </div>
            </DialogContent>
        </Dialog>
    );
}

// 1. Flashcard View
function FlashcardView({ lesson, onComplete }: { lesson: Lesson; onComplete: () => void }) {
    const [isFlipped, setIsFlipped] = useState(false);

    return (
        <div className="h-full flex flex-col items-center justify-center gap-8 perspective-1000">
            <div
                className="relative w-full max-w-md h-64 cursor-pointer group perspective-1000"
                onClick={() => setIsFlipped(!isFlipped)}
            >
                <div className={cn(
                    "w-full h-full relative preserve-3d transition-transform duration-500 shadow-xl rounded-2xl",
                    isFlipped ? "rotate-y-180" : ""
                )}>
                    {/* Front */}
                    <div className="absolute inset-0 backface-hidden bg-white dark:bg-gray-800 rounded-2xl flex flex-col items-center justify-center p-8 border-2 border-blue-100 dark:border-blue-900">
                        <span className="text-sm text-gray-400 uppercase tracking-widest mb-4">Concept</span>
                        <h3 className="text-3xl font-bold text-center text-gray-900 dark:text-white">
                            {lesson.content?.front}
                        </h3>
                        <p className="text-xs text-gray-400 mt-8 animate-pulse">点击翻转</p>
                    </div>

                    {/* Back */}
                    <div className="absolute inset-0 backface-hidden rotate-y-180 bg-blue-50 dark:bg-blue-950 rounded-2xl flex flex-col items-center justify-center p-8 border-2 border-blue-200 text-center">
                        <span className="text-sm text-blue-400 uppercase tracking-widest mb-4">Explanation</span>
                        <p className="text-lg text-gray-700 dark:text-gray-200 whitespace-pre-line leading-relaxed">
                            {lesson.content?.back}
                        </p>
                    </div>
                </div>
            </div>

            <div className="flex gap-4">
                <Button variant="outline" onClick={() => setIsFlipped(!isFlipped)}>
                    <RotateCw className="w-4 h-4 mr-2" />
                    {isFlipped ? "看正面" : "看背面"}
                </Button>
                <Button onClick={onComplete} className={cn(!isFlipped && "opacity-50 pointer-events-none")}>
                    我学会了
                </Button>
            </div>
        </div>
    );
}

// 2. Quiz View
function QuizView({ lesson, onComplete }: { lesson: Lesson; onComplete: () => void }) {
    const [selectedOption, setSelectedOption] = useState<number | null>(null);
    const [isSubmitted, setIsSubmitted] = useState(false);

    const isCorrect = selectedOption === lesson.content?.correctAnswer;

    const handleSubmit = () => {
        setIsSubmitted(true);
        if (selectedOption === lesson.content?.correctAnswer) {
            setTimeout(onComplete, 2000); // 2秒后自动完成
        }
    };

    return (
        <div className="h-full flex flex-col max-w-lg mx-auto">
            <div className="flex-1 space-y-6">
                <h3 className="text-xl font-medium text-gray-900 dark:text-white leading-normal">
                    {lesson.content?.question}
                </h3>

                <div className="space-y-3">
                    {lesson.content?.options?.map((option, index) => (
                        <div
                            key={index}
                            onClick={() => !isSubmitted && setSelectedOption(index)}
                            className={cn(
                                "p-4 rounded-lg border-2 cursor-pointer transition-all flex items-center justify-between",
                                !isSubmitted && selectedOption === index && "border-blue-500 bg-blue-50 dark:bg-blue-900/20",
                                !isSubmitted && selectedOption !== index && "border-gray-200 dark:border-gray-700 hover:border-blue-300",
                                isSubmitted && index === lesson.content?.correctAnswer && "border-green-500 bg-green-50 dark:bg-green-900/20",
                                isSubmitted && selectedOption === index && index !== lesson.content?.correctAnswer && "border-red-500 bg-red-50 dark:bg-red-900/20"
                            )}
                        >
                            <span>{option}</span>
                            {isSubmitted && index === lesson.content?.correctAnswer && <CheckCircle className="w-5 h-5 text-green-500" />}
                            {isSubmitted && selectedOption === index && index !== lesson.content?.correctAnswer && <XCircle className="w-5 h-5 text-red-500" />}
                        </div>
                    ))}
                </div>

                {isSubmitted && (
                    <div className={cn(
                        "p-4 rounded-lg text-sm",
                        isCorrect ? "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300" : "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300"
                    )}>
                        <strong>{isCorrect ? "回答正确！🎉" : "回答错误 😅"}</strong>
                        <p className="mt-1">{lesson.content?.explanation}</p>
                    </div>
                )}
            </div>

            <div className="pt-6 border-t mt-6">
                <Button
                    className="w-full"
                    disabled={selectedOption === null || isSubmitted}
                    onClick={handleSubmit}
                >
                    提交答案
                </Button>
            </div>
        </div>
    );
}

// 3. Article View
function ArticleView({ lesson, onComplete }: { lesson: Lesson; onComplete: () => void }) {
    return (
        <div className="h-full flex flex-col">
            <ScrollArea className="flex-1 pr-4">
                <article className="prose dark:prose-invert max-w-none">
                    {/* 简单渲染 Markdown 风格文本 */}
                    {lesson.content?.text?.split('\n').map((line, i) => {
                        if (line.startsWith('# ')) return <h1 key={i} className="text-2xl font-bold mb-4">{line.slice(2)}</h1>
                        if (line.startsWith('### ')) return <h3 key={i} className="text-lg font-bold mt-6 mb-2">{line.slice(4)}</h3>
                        if (line.startsWith('- ')) return <li key={i} className="ml-4">{line.slice(2)}</li>
                        if (line.startsWith('**')) return <strong key={i}>{line.replaceAll('**', '')}</strong>
                        if (line === '') return <div key={i} className="h-4"></div>
                        return <p key={i} className="mb-2 text-gray-700 dark:text-gray-300 leading-relaxed">{line}</p>
                    })}
                </article>
            </ScrollArea>

            <div className="pt-6 border-t mt-6 flex justify-end">
                <Button onClick={onComplete} className="gap-2">
                    读完了 <ArrowRight className="w-4 h-4" />
                </Button>
            </div>
        </div>
    );
}
