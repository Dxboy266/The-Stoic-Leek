import axios from 'axios';
import { useUserStore } from '@/store/user';

// API 基础配置
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
});

// 请求拦截器：自动注入 Token
api.interceptors.request.use(
  (config) => {
    const token = useUserStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：处理错误
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // 统一处理 401
    if (error.response?.status === 401) {
      useUserStore.getState().logout();
    }
    return Promise.reject(error.response?.data || error);
  }
);
