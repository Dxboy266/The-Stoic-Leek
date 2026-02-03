import { create } from 'zustand';

// ==================== 基金相关类型 ====================
interface FundHolding {
    code: string;
    shares: number;
    costPrice?: number;
}

// ==================== AI 配置相关类型 ====================

/** AI 模型定义 */
export interface AIModel {
    id: string;
    name: string;
    type: 'chat' | 'vision' | 'both';
    tags?: string[]; // 例如 ['免费', '推荐', '限免']
}

/** AI 提供商配置 */
export interface AIProviderConfig {
    id: string;
    name: string;
    baseUrl: string;
    apiKey: string;
    chatModel: string;
    visionModel: string;
    isCustom?: boolean;
}

/** AI 设置 */
export interface AISettings {
    activeProvider: string;
    providers: AIProviderConfig[];
}

/** 预设提供商模板 */
export interface ProviderTemplate {
    id: string;
    name: string;
    baseUrl: string;
    chatModels: AIModel[];
    visionModels: AIModel[];
    defaultChatModel: string;
    defaultVisionModel: string;
    getKeyUrl?: string;
}

// ==================== 预设配置 ====================

/** 预设的 AI 提供商模板 */
export const PROVIDER_TEMPLATES: ProviderTemplate[] = [
    {
        id: 'siliconflow',
        name: 'SiliconFlow (硅基流动)',
        baseUrl: 'https://api.siliconflow.cn/v1',
        getKeyUrl: 'https://cloud.siliconflow.cn/',
        chatModels: [
            { id: 'deepseek-ai/DeepSeek-V3', name: 'DeepSeek V3', type: 'chat', tags: ['收费', '强力'] },
            { id: 'deepseek-ai/DeepSeek-R1', name: 'DeepSeek R1', type: 'chat', tags: ['收费', '深度推理'] },
            { id: 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B', name: 'DeepSeek R1 (Qwen-7B蒸馏)', type: 'chat', tags: ['免费', '推荐'] },
            { id: 'deepseek-ai/DeepSeek-R1-Distill-Llama-8B', name: 'DeepSeek R1 (Llama-8B蒸馏)', type: 'chat', tags: ['免费'] },
            { id: 'Qwen/Qwen2.5-7B-Instruct', name: 'Qwen2.5 7B', type: 'chat', tags: ['免费', '快'] },
            { id: 'Qwen/Qwen2.5-72B-Instruct', name: 'Qwen2.5 72B', type: 'chat', tags: ['收费', '均衡'] },
        ],
        visionModels: [
            { id: 'Pro/Qwen/Qwen2-VL-7B-Instruct', name: 'Qwen2-VL 7B Pro', type: 'vision', tags: ['免费', '推荐'] },
            { id: 'Qwen/Qwen2-VL-72B-Instruct', name: 'Qwen2-VL 72B', type: 'vision', tags: ['收费', '最强'] },
            { id: 'OpenGVLab/InternVL2-26B', name: 'InternVL2 26B', type: 'vision', tags: ['免费'] },
            { id: 'deepseek-ai/deepseek-vl2', name: 'DeepSeek VL2', type: 'vision', tags: ['免费'] },
        ],
        defaultChatModel: 'deepseek-ai/DeepSeek-V3',
        defaultVisionModel: 'Pro/Qwen/Qwen2-VL-7B-Instruct',
    },
    {
        id: 'openai',
        name: 'OpenAI',
        baseUrl: 'https://api.openai.com/v1',
        getKeyUrl: 'https://platform.openai.com/api-keys',
        chatModels: [
            { id: 'gpt-4o', name: 'GPT-4o', type: 'both', tags: ['收费', '推荐'] },
            { id: 'gpt-4o-mini', name: 'GPT-4o Mini', type: 'both', tags: ['收费', '便宜'] },
            { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', type: 'chat', tags: ['收费'] },
            { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', type: 'chat', tags: ['收费'] },
        ],
        visionModels: [
            { id: 'gpt-4o', name: 'GPT-4o', type: 'both', tags: ['收费', '强力'] },
            { id: 'gpt-4o-mini', name: 'GPT-4o Mini', type: 'both', tags: ['收费', '快'] },
        ],
        defaultChatModel: 'gpt-4o',
        defaultVisionModel: 'gpt-4o',
    },
    {
        id: 'deepseek',
        name: 'DeepSeek (官方)',
        baseUrl: 'https://api.deepseek.com/v1',
        getKeyUrl: 'https://platform.deepseek.com/',
        chatModels: [
            { id: 'deepseek-chat', name: 'DeepSeek V3', type: 'chat', tags: ['收费'] },
            { id: 'deepseek-reasoner', name: 'DeepSeek R1', type: 'chat', tags: ['收费'] },
        ],
        visionModels: [],
        defaultChatModel: 'deepseek-chat',
        defaultVisionModel: '',
    },
    {
        id: 'custom',
        name: '自定义',
        baseUrl: '',
        chatModels: [],
        visionModels: [],
        defaultChatModel: '',
        defaultVisionModel: '',
    },
];

/** 创建默认的 AI 设置 */
export function createDefaultAISettings(): AISettings {
    const siliconflow = PROVIDER_TEMPLATES.find(p => p.id === 'siliconflow')!;
    return {
        activeProvider: 'siliconflow',
        providers: [{
            id: 'siliconflow',
            name: siliconflow.name,
            baseUrl: siliconflow.baseUrl,
            apiKey: '',
            chatModel: siliconflow.defaultChatModel,
            visionModel: siliconflow.defaultVisionModel,
        }],
    };
}

/** 获取提供商模板 */
export function getProviderTemplate(providerId: string): ProviderTemplate | undefined {
    return PROVIDER_TEMPLATES.find(p => p.id === providerId);
}

// ==================== 用户设置类型 ====================

interface UserSettings {
    total_assets?: number;
    exercises?: string[];
    today_record?: any;
    record_date?: string;
    market_summary?: { content: string; date: string };
    funds?: FundHolding[];
    aiSettings?: AISettings;  // AI 配置
}

interface UserState {
    settings: UserSettings;
    isLoaded: boolean;
    updateSettings: (settings: Partial<UserSettings>) => void;
    setLoaded: (loaded: boolean) => void;
    reset: () => void;

    // AI 设置辅助方法
    getActiveProvider: () => AIProviderConfig | undefined;
    updateProviderConfig: (providerId: string, config: Partial<AIProviderConfig>) => void;
    setActiveProvider: (providerId: string) => void;
    addProvider: (config: AIProviderConfig) => void;

    // 认证相关
    user?: { email: string; id: string };
    token?: string;
    setAuth: (user: { email: string; id: string }, token: string) => void;
    logout: () => void;
}

// ==================== Store ====================

export const useUserStore = create<UserState>()((set, get) => ({
    settings: {},
    isLoaded: false,

    updateSettings: (newSettings) => set((state) => ({
        settings: { ...state.settings, ...newSettings }
    })),

    setLoaded: (loaded) => set({ isLoaded: loaded }),

    reset: () => set({ settings: {}, isLoaded: false }),

    // 获取当前激活的提供商配置
    getActiveProvider: () => {
        const { settings } = get();
        const aiSettings = settings.aiSettings || createDefaultAISettings();
        return aiSettings.providers.find(p => p.id === aiSettings.activeProvider);
    },

    // 更新指定提供商的配置
    updateProviderConfig: (providerId, config) => set((state) => {
        const aiSettings = state.settings.aiSettings || createDefaultAISettings();
        const providers = aiSettings.providers.map(p =>
            p.id === providerId ? { ...p, ...config } : p
        );
        return {
            settings: {
                ...state.settings,
                aiSettings: { ...aiSettings, providers }
            }
        };
    }),

    // 设置激活的提供商
    setActiveProvider: (providerId) => set((state) => {
        const aiSettings = state.settings.aiSettings || createDefaultAISettings();
        return {
            settings: {
                ...state.settings,
                aiSettings: { ...aiSettings, activeProvider: providerId }
            }
        };
    }),

    // 添加新的提供商配置
    addProvider: (config) => set((state) => {
        const aiSettings = state.settings.aiSettings || createDefaultAISettings();
        // 如果已存在则更新，否则添加
        const exists = aiSettings.providers.find(p => p.id === config.id);
        const providers = exists
            ? aiSettings.providers.map(p => p.id === config.id ? config : p)
            : [...aiSettings.providers, config];
        return {
            settings: {
                ...state.settings,
                aiSettings: { ...aiSettings, providers }
            }
        };
    }),

    // 认证方法实现
    setAuth: (user, token) => set({ user, token }),
    logout: () => set({ user: undefined, token: undefined }),
}));
