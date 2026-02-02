import { create } from 'zustand';

interface FundHolding {
    code: string;
    shares: number;
    costPrice?: number;
}

interface UserSettings {
    total_assets?: number;
    exercises?: string[];
    today_record?: any;
    record_date?: string;
    market_summary?: { content: string; date: string };
    funds?: FundHolding[];
}

interface UserState {
    settings: UserSettings;
    isLoaded: boolean; // 标记数据是否已从后端加载
    updateSettings: (settings: Partial<UserSettings>) => void;
    setLoaded: (loaded: boolean) => void;
    reset: () => void;
}

// 纯内存 Store，不使用 LocalStorage
// 数据持久化通过后端 JSON 文件实现
export const useUserStore = create<UserState>()((set) => ({
    settings: {},
    isLoaded: false,
    updateSettings: (newSettings) => set((state) => ({
        settings: { ...state.settings, ...newSettings }
    })),
    setLoaded: (loaded) => set({ isLoaded: loaded }),
    reset: () => set({ settings: {}, isLoaded: false }),
}));

