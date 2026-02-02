'use client';

import { useState, useCallback } from 'react';
import { api } from '@/lib/api';

// 基金实时数据类型
export interface FundRealtime {
    code: string;
    name: string;
    gsz: number;       // 实时估值
    gszzl: number;     // 涨跌幅%
    dwjz: number;      // 昨日净值
    gztime: string;    // 估值时间
    jzrq: string;      // 净值日期
}

// 持仓基金类型
export interface FundHolding {
    code: string;
    shares: number;      // 份额
    costPrice?: number;  // 成本价（第二阶段）
}

// 单个基金查询 Hook
export function useFundRealtime() {
    const [data, setData] = useState<FundRealtime | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetch = useCallback(async (code: string) => {
        if (!code || code.length !== 6) {
            setError('请输入6位基金代码');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            // api 拦截器已返回 response.data
            const result = await api.get(`/fund/${code}`);
            setData(result as unknown as FundRealtime);
        } catch (err: any) {
            const message = err.detail || err.message || '获取失败';
            setError(message);
            setData(null);
        } finally {
            setLoading(false);
        }
    }, []);

    const reset = useCallback(() => {
        setData(null);
        setError(null);
    }, []);

    return { data, loading, error, fetch, reset };
}

// 批量获取基金数据
export async function batchFetchFunds(codes: string[]): Promise<FundRealtime[]> {
    if (codes.length === 0) return [];

    try {
        const result = await api.get('/fund/batch/query', {
            params: { codes: codes.join(',') }
        });
        return result as unknown as FundRealtime[];
    } catch (err) {
        console.error('批量获取基金失败:', err);
        return [];
    }
}

// 计算涨跌金额
export function calculateChange(fund: FundRealtime, shares: number): number {
    // 涨跌金额 = (实时估值 - 昨日净值) × 份额
    return (fund.gsz - fund.dwjz) * shares;
}

// 计算持仓市值
export function calculateMarketValue(fund: FundRealtime, shares: number): number {
    return fund.gsz * shares;
}
