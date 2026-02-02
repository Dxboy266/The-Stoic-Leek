import { api } from '@/lib/api';

export const PersistenceService = {
    // api拦截器已返回response.data，这里直接拿到的就是后端返回的对象
    load: () => api.get('/persistence/load') as Promise<{ data: any }>,
    save: (data: any) => api.post('/persistence/save', { data }),
};
