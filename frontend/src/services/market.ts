import { api } from '@/lib/api';

export const MarketService = {
    getNorthbound: () => api.get('/market/northbound'),
    getHotSectors: () => api.get('/market/hot-sectors'),
    getDailySummary: (params: { api_key: string; model?: string }) =>
        api.get('/market/daily-summary', { params }),
};
