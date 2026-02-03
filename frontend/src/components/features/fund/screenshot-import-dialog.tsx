'use client';

import { useState, useRef, useCallback } from 'react';
import { Camera, Upload, Loader2, Check, X, ImageIcon } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
} from '@/components/ui/dialog';
import { api } from '@/lib/api';
import { cn } from '@/lib/utils';
import { useUserStore } from '@/store/user';

// 识别结果类型
interface RecognizedFund {
    name: string;
    code?: string;
    amount?: number;
    shares?: number;
    selected?: boolean;
}

interface ScreenshotImportDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onImport: (funds: { code: string; shares: number }[]) => void;
}

export function ScreenshotImportDialog({ open, onOpenChange, onImport }: ScreenshotImportDialogProps) {
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [recognizedFunds, setRecognizedFunds] = useState<RecognizedFund[]>([]);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // 获取用户设置的 AI 配置
    const { settings, getActiveProvider } = useUserStore();

    // 处理文件选择
    const handleFileSelect = useCallback(async (file: File) => {
        if (!file.type.startsWith('image/')) {
            setError('请选择图片文件');
            return;
        }

        // 读取文件为 Base64
        const reader = new FileReader();
        reader.onload = async (e) => {
            const base64 = e.target?.result as string;
            setImagePreview(base64);
            setError(null);
            setRecognizedFunds([]);

            // 调用 OCR API
            await recognizeImage(base64);
        };
        reader.readAsDataURL(file);
    }, []);

    // 调用后端识别
    const recognizeImage = async (imageBase64: string) => {
        setLoading(true);
        setError(null);

        // 获取当前激活的 AI 提供商配置
        const provider = getActiveProvider();

        try {
            const response = await api.post('/fund/import/screenshot', {
                image: imageBase64,
                baseUrl: provider?.baseUrl,
                apiKey: provider?.apiKey,
                model: provider?.visionModel || 'Qwen/Qwen2-VL-72B-Instruct'
            }) as { success: boolean; funds: RecognizedFund[]; message: string };

            if (response.success && response.funds.length > 0) {
                // 默认全选
                setRecognizedFunds(response.funds.map(f => ({ ...f, selected: true })));
            } else {
                setError(response.message || '未能识别出基金信息');
            }
        } catch (err: any) {
            setError(err.detail || err.message || '识别失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    // 切换选中状态
    const toggleSelect = (index: number) => {
        setRecognizedFunds(prev =>
            prev.map((f, i) => i === index ? { ...f, selected: !f.selected } : f)
        );
    };

    // 确认导入
    const handleConfirmImport = () => {
        const selectedFunds = recognizedFunds
            .filter(f => f.selected && f.code)
            .map(f => ({
                code: f.code!,
                shares: f.shares || f.amount || 0
            }));

        if (selectedFunds.length === 0) {
            setError('请选择至少一只基金');
            return;
        }

        onImport(selectedFunds);
        handleClose();
    };

    // 关闭并重置
    const handleClose = () => {
        setImagePreview(null);
        setRecognizedFunds([]);
        setError(null);
        onOpenChange(false);
    };

    // 拖拽上传
    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file) handleFileSelect(file);
    }, [handleFileSelect]);

    return (
        <Dialog open={open} onOpenChange={handleClose}>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <Camera className="w-5 h-5 text-purple-500" />
                        截图导入持仓
                    </DialogTitle>
                    <DialogDescription>
                        上传支付宝/天天基金的持仓页面截图，自动识别基金信息
                    </DialogDescription>
                </DialogHeader>

                <div className="space-y-4 py-4">
                    {/* 上传区域 */}
                    {!imagePreview && (
                        <div
                            className={cn(
                                "border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors",
                                "hover:border-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20",
                                "border-gray-300 dark:border-gray-600"
                            )}
                            onClick={() => fileInputRef.current?.click()}
                            onDrop={handleDrop}
                            onDragOver={(e) => e.preventDefault()}
                        >
                            <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                            <p className="text-gray-600 dark:text-gray-400 mb-2">
                                点击上传或拖拽截图到这里
                            </p>
                            <p className="text-sm text-gray-400">
                                支持 JPG、PNG 格式
                            </p>
                        </div>
                    )}

                    <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        className="hidden"
                        onChange={(e) => {
                            const file = e.target.files?.[0];
                            if (file) handleFileSelect(file);
                        }}
                    />

                    {/* 图片预览 */}
                    {imagePreview && (
                        <div className="relative">
                            <img
                                src={imagePreview}
                                alt="截图预览"
                                className="w-full max-h-64 object-contain rounded-lg border"
                            />
                            <Button
                                variant="ghost"
                                size="sm"
                                className="absolute top-2 right-2 h-8 w-8 p-0 bg-black/50 hover:bg-black/70 text-white rounded-full"
                                onClick={() => {
                                    setImagePreview(null);
                                    setRecognizedFunds([]);
                                }}
                            >
                                <X className="w-4 h-4" />
                            </Button>
                        </div>
                    )}

                    {/* Loading */}
                    {loading && (
                        <div className="flex items-center justify-center py-8">
                            <Loader2 className="w-8 h-8 animate-spin text-purple-500 mr-3" />
                            <span className="text-gray-600">正在识别中...</span>
                        </div>
                    )}

                    {/* 错误提示 */}
                    {error && (
                        <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg">
                            <p className="mb-3">识别失败: {error}</p>
                            <div className="flex gap-2">
                                {imagePreview && (
                                    <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => recognizeImage(imagePreview)}
                                        disabled={loading}
                                    >
                                        🔄 重试识别
                                    </Button>
                                )}
                                <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => {
                                        setError(null);
                                        setImagePreview(null);
                                    }}
                                >
                                    📷 重新上传
                                </Button>
                            </div>
                        </div>
                    )}

                    {/* 识别结果 */}
                    {recognizedFunds.length > 0 && (
                        <div className="space-y-2">
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                识别结果（点击选择要导入的基金）
                            </p>
                            <div className="space-y-2 max-h-60 overflow-y-auto">
                                {recognizedFunds.map((fund, index) => (
                                    <div
                                        key={index}
                                        onClick={() => toggleSelect(index)}
                                        className={cn(
                                            "flex items-center justify-between p-3 rounded-lg border cursor-pointer transition-colors",
                                            fund.selected
                                                ? "border-purple-500 bg-purple-50 dark:bg-purple-900/30"
                                                : "border-gray-200 dark:border-gray-700 hover:border-gray-300"
                                        )}
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className={cn(
                                                "w-5 h-5 rounded-full border-2 flex items-center justify-center",
                                                fund.selected
                                                    ? "border-purple-500 bg-purple-500"
                                                    : "border-gray-300"
                                            )}>
                                                {fund.selected && <Check className="w-3 h-3 text-white" />}
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900 dark:text-white">
                                                    {fund.name}
                                                </p>
                                                <p className="text-sm text-gray-500">
                                                    {fund.code || '代码未识别'}
                                                    {fund.amount && ` · ¥${fund.amount.toLocaleString()}`}
                                                    {fund.shares && ` · ${fund.shares.toFixed(2)}份`}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                <DialogFooter>
                    <Button variant="outline" onClick={handleClose}>
                        取消
                    </Button>
                    {recognizedFunds.length > 0 && (
                        <Button
                            onClick={handleConfirmImport}
                            className="bg-gradient-to-r from-purple-600 to-indigo-600"
                        >
                            导入 {recognizedFunds.filter(f => f.selected).length} 只基金
                        </Button>
                    )}
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
