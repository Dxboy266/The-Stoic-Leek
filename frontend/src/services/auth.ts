import { api } from '@/lib/api';

export const AuthService = {
    login: (data: any) => api.post('/auth/login', data),
    register: (data: any) => api.post('/auth/register', data),
    logout: () => api.post('/auth/logout'),
};
