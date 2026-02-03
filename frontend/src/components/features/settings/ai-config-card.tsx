'use client';

import { useState, useEffect } from 'react';
import { Key, Eye, EyeOff, Check, ExternalLink, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import {
    useUserStore,
    PROVIDER_TEMPLATES,
    getProviderTemplate,
    createDefaultAISettings,
    type AIProviderConfig,
    type ProviderTemplate,
} from '@/store/user';
import { api } from '@/lib/api';

interface AIConfigCardProps {
    onSave?: () => void;
}

export function AIConfigCard({ onSave }: AIConfigCardProps) {
    const { settings, updateSettings, updateProviderConfig, addProvider, setActiveProvider } = useUserStore();

    // 获取当前 AI 设置
    const aiSettings = settings.aiSettings || createDefaultAISettings();
    const activeProviderId = aiSettings.activeProvider;

    // 当前编辑的提供商配置
    const [editingProvider, setEditingProvider] = useState<AIProviderConfig | null>(null);
    const [showApiKey, setShowApiKey] = useState(false);
    const [testing, setTesting] = useState(false);
    const [testResult, setTestResult] = useState<'success' | 'error' | null>(null);

    // 初始化编辑状态
    useEffect(() => {
        // 找到当前选中的 provider 配置
        const provider = settings.aiSettings?.providers.find(p => p.id === activeProviderId);

        if (provider) {
            // 只有当 ID 变化时才重置 editingProvider，防止输入时被重置
            setEditingProvider(prev => {
                if (prev?.id === provider.id) return prev;
                return { ...provider };
            });
        } else {
            // ...
            const template = getProviderTemplate(activeProviderId);
            if (template) {
                // ...
                const newProvider: AIProviderConfig = {
                    id: template.id,
                    name: template.name,
                    baseUrl: template.baseUrl,
                    apiKey: '',
                    chatModel: template.defaultChatModel,
                    visionModel: template.defaultVisionModel,
                };
                setEditingProvider(newProvider);
            }
        }
    }, [activeProviderId]); // 关键：移除 aiSettings.providers 依赖，因为我们在组件内部修改它会导致死循环

    // 切换提供商
    const handleProviderChange = (providerId: string) => {
        // 先保存当前编辑
        if (editingProvider) {
            addProvider(editingProvider);
        }
        setActiveProvider(providerId);

        // 检查是否已有配置
        const existing = aiSettings.providers.find(p => p.id === providerId);
        if (!existing) {
            const template = getProviderTemplate(providerId);
            if (template) {
                const newProvider: AIProviderConfig = {
                    id: template.id,
                    name: template.name,
                    baseUrl: template.baseUrl,
                    apiKey: '',
                    chatModel: template.defaultChatModel,
                    visionModel: template.defaultVisionModel,
                };
                addProvider(newProvider);
            }
        }
    };

    // 更新当前编辑的配置
    const updateField = (field: keyof AIProviderConfig, value: string) => {
        if (!editingProvider) return;
        setEditingProvider({ ...editingProvider, [field]: value });
        setTestResult(null);
    };

    // 保存配置
    const handleSave = async () => {
        if (!editingProvider) return;

        addProvider(editingProvider);

        // 触发持久化保存
        if (onSave) {
            onSave();
        }

        toast.success('AI 配置已保存');
    };

    // 测试连接
    const handleTestConnection = async () => {
        if (!editingProvider?.apiKey) {
            toast.error('请先输入 API Key');
            return;
        }

        setTesting(true);
        setTestResult(null);

        try {
            const response = await api.post('/ai/test', {
                baseUrl: editingProvider.baseUrl,
                apiKey: editingProvider.apiKey,
                model: editingProvider.chatModel,
            }) as { success: boolean; message: string };

            if (response.success) {
                setTestResult('success');
                toast.success('连接成功！');
            } else {
                setTestResult('error');
                toast.error(response.message || '连接失败');
            }
        } catch (err: any) {
            setTestResult('error');
            toast.error(err.detail || err.message || '连接测试失败');
        } finally {
            setTesting(false);
        }
    };

    const currentTemplate = getProviderTemplate(activeProviderId);
    const isCustom = activeProviderId === 'custom';

    return (
        <Card className="border-0 shadow-lg">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center">
                        <Key className="w-5 h-5 text-white" />
                    </div>
                    AI 配置
                </CardTitle>
                <CardDescription>
                    选择 AI 提供商并配置 API Key
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
                {/* 提供商选择 */}
                <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3 block">
                        选择 AI 提供商
                    </label>
                    <div className="flex flex-wrap gap-2">
                        {PROVIDER_TEMPLATES.map((template) => (
                            <button
                                key={template.id}
                                onClick={() => handleProviderChange(template.id)}
                                className={cn(
                                    "px-4 py-2 rounded-lg text-sm font-medium transition-all border",
                                    activeProviderId === template.id
                                        ? "bg-purple-100 border-purple-300 text-purple-700 dark:bg-purple-900/40 dark:border-purple-700 dark:text-purple-300"
                                        : "bg-white border-gray-200 text-gray-600 hover:border-purple-200 hover:text-purple-600 dark:bg-gray-900 dark:border-gray-700 dark:text-gray-400"
                                )}
                            >
                                {template.name}
                                {activeProviderId === template.id && (
                                    <Check className="inline w-4 h-4 ml-1" />
                                )}
                            </button>
                        ))}
                    </div>
                </div>

                {/* 获取 Key 链接 */}
                {currentTemplate?.getKeyUrl && (
                    <a
                        href={currentTemplate.getKeyUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-sm text-blue-600 hover:underline"
                    >
                        点击获取 {currentTemplate.name} API Key
                        <ExternalLink className="w-3 h-3" />
                    </a>
                )}

                {/* API Key 输入 */}
                <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                        API Key
                    </label>
                    <div className="flex gap-2">
                        <div className="relative flex-1">
                            <Input
                                type={showApiKey ? 'text' : 'password'}
                                placeholder="sk-..."
                                value={editingProvider?.apiKey || ''}
                                onChange={(e) => updateField('apiKey', e.target.value)}
                                className="pr-10"
                            />
                            <button
                                type="button"
                                onClick={() => setShowApiKey(!showApiKey)}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                            >
                                {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                            </button>
                        </div>
                        <Button
                            variant="outline"
                            onClick={handleTestConnection}
                            disabled={testing || !editingProvider?.apiKey}
                        >
                            {testing ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                            ) : testResult === 'success' ? (
                                <CheckCircle2 className="w-4 h-4 text-green-500" />
                            ) : testResult === 'error' ? (
                                <AlertCircle className="w-4 h-4 text-red-500" />
                            ) : (
                                '测试'
                            )}
                        </Button>
                    </div>
                </div>

                {/* 自定义 Base URL（仅自定义模式） */}
                {isCustom && (
                    <div>
                        <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                            API Base URL
                        </label>
                        <Input
                            placeholder="https://api.example.com/v1"
                            value={editingProvider?.baseUrl || ''}
                            onChange={(e) => updateField('baseUrl', e.target.value)}
                        />
                    </div>
                )}

                {/* 对话模型选择 */}
                <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                        对话模型（用于 AI 建议）
                    </label>
                    {isCustom ? (
                        <Input
                            placeholder="gpt-4o"
                            value={editingProvider?.chatModel || ''}
                            onChange={(e) => updateField('chatModel', e.target.value)}
                        />
                    ) : (
                        <div className="flex flex-wrap gap-2">
                            {currentTemplate?.chatModels.map((model) => (
                                <button
                                    key={model.id}
                                    onClick={() => updateField('chatModel', model.id)}
                                    className={cn(
                                        "px-3 py-1.5 rounded-lg text-sm border transition-all flex items-center gap-2",
                                        editingProvider?.chatModel === model.id
                                            ? "bg-blue-100 border-blue-300 text-blue-700 dark:bg-blue-900/40 dark:border-blue-700 dark:text-blue-300"
                                            : "bg-white border-gray-200 text-gray-600 hover:border-blue-200 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400"
                                    )}
                                >
                                    {model.name}
                                    {model.tags && model.tags.map(tag => (
                                        <span key={tag} className={cn(
                                            "text-[10px] px-1.5 py-0.5 rounded-full scale-90 origin-left",
                                            tag === '免费' ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300" :
                                                tag === '收费' ? "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300" :
                                                    "bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300"
                                        )}>
                                            {tag}
                                        </span>
                                    ))}
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                {/* 视觉模型选择 */}
                {(isCustom || (currentTemplate?.visionModels && currentTemplate.visionModels.length > 0)) && (
                    <div>
                        <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                            视觉模型（用于截图识别）
                        </label>
                        {isCustom ? (
                            <Input
                                placeholder="gpt-4o"
                                value={editingProvider?.visionModel || ''}
                                onChange={(e) => updateField('visionModel', e.target.value)}
                            />
                        ) : (
                            <div className="flex flex-wrap gap-2">
                                {currentTemplate?.visionModels.map((model) => (
                                    <button
                                        key={model.id}
                                        onClick={() => updateField('visionModel', model.id)}
                                        className={cn(
                                            "px-3 py-1.5 rounded-lg text-sm border transition-all flex items-center gap-2",
                                            editingProvider?.visionModel === model.id
                                                ? "bg-teal-100 border-teal-300 text-teal-700 dark:bg-teal-900/40 dark:border-teal-700 dark:text-teal-300"
                                                : "bg-white border-gray-200 text-gray-600 hover:border-teal-200 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400"
                                        )}
                                    >
                                        {model.name}
                                        {model.tags && model.tags.map(tag => (
                                            <span key={tag} className={cn(
                                                "text-[10px] px-1.5 py-0.5 rounded-full scale-90 origin-left",
                                                tag === '免费' ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300" :
                                                    tag === '收费' ? "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300" :
                                                        "bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300"
                                            )}>
                                                {tag}
                                            </span>
                                        ))}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {/* 无视觉模型提示 */}
                {!isCustom && currentTemplate?.visionModels.length === 0 && (
                    <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                        <p className="text-sm text-yellow-700 dark:text-yellow-300">
                            ⚠️ {currentTemplate.name} 不支持视觉模型，截图识别功能将无法使用。建议使用 SiliconFlow 或 OpenAI。
                        </p>
                    </div>
                )}

                {/* 保存按钮 */}
                <div className="flex justify-end pt-2">
                    <Button
                        onClick={handleSave}
                        className="bg-gradient-to-r from-purple-600 to-indigo-600"
                    >
                        保存配置
                    </Button>
                </div>

                {/* 提示信息 */}
                <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                        💡 配置保存在本地文件中，不会上传到任何服务器。切换提供商后，之前的配置会被保留。
                    </p>
                </div>
            </CardContent>
        </Card>
    );
}
