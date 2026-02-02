'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { Plus, Search, RefreshCw, TrendingUp, Loader2, Wallet } from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { FundCard } from './fund-card';
import { useFundRealtime, batchFetchFunds, FundRealtime, FundHolding, calculateChange, calculateMarketValue } from '@/hooks/use-fund';
import { useUserStore } from '@/store/user';
import { cn } from '@/lib/utils';

export function FundDashboard() {
    // 查询相关
    const [searchCode, setSearchCode] = useState('');
    const { data: searchResult, loading: searching, error: searchError, fetch: searchFund, reset: resetSearch } = useFundRealtime();

    // 持仓相关
    const [holdings, setHoldings] = useState<FundHolding[]>([]);
    const [fundDataMap, setFundDataMap] = useState<Map<string, FundRealtime>>(new Map());
    const [loadingHoldings, setLoadingHoldings] = useState(false);

    // 添加持仓弹窗
    const [addDialogOpen, setAddDialogOpen] = useState(false);
    const [addCode, setAddCode] = useState('');
    const [addShares, setAddShares] = useState('');

    // 编辑持仓弹窗
    const [editDialogOpen, setEditDialogOpen] = useState(false);
    const [editCode, setEditCode] = useState('');
    const [editShares, setEditShares] = useState('');

    const { settings, updateSettings } = useUserStore();
    const hasInitialized = useRef(false);

    // 从 store 加载持仓
    useEffect(() => {
        if (hasInitialized.current) return;
        hasInitialized.current = true;

        const savedFunds = settings.funds as FundHolding[] | undefined;
        if (savedFunds && savedFunds.length > 0) {
            setHoldings(savedFunds);
        }
    }, [settings.funds]);

    // 持仓变化时刷新数据
    useEffect(() => {
        if (holdings.length > 0) {
            refreshHoldings();
        }
    }, [holdings.length]);

    // 刷新持仓数据
    const refreshHoldings = useCallback(async () => {
        if (holdings.length === 0) return;

        setLoadingHoldings(true);
        try {
            const codes = holdings.map(h => h.code);
            const data = await batchFetchFunds(codes);

            const newMap = new Map<string, FundRealtime>();
            data.forEach(fund => newMap.set(fund.code, fund));
            setFundDataMap(newMap);
        } catch (err) {
            console.error('刷新持仓失败:', err);
            toast.error('刷新持仓数据失败');
        } finally {
            setLoadingHoldings(false);
        }
    }, [holdings]);

    // 保存持仓到 store
    const saveHoldings = useCallback((newHoldings: FundHolding[]) => {
        setHoldings(newHoldings);
        updateSettings({ funds: newHoldings });
    }, [updateSettings]);

    // 搜索基金
    const handleSearch = () => {
        if (searchCode.trim()) {
            searchFund(searchCode.trim());
        }
    };

    // 添加到持仓
    const handleAddToHoldings = () => {
        if (!addCode || addCode.length !== 6) {
            toast.error('请输入6位基金代码');
            return;
        }

        if (holdings.some(h => h.code === addCode)) {
            toast.error('该基金已在持仓中');
            return;
        }

        const shares = parseFloat(addShares) || 0;
        const newHolding: FundHolding = {
            code: addCode,
            shares: shares,
        };

        saveHoldings([...holdings, newHolding]);
        setAddDialogOpen(false);
        setAddCode('');
        setAddShares('');
        toast.success('添加成功');
    };

    // 从查询结果快速添加
    const handleQuickAdd = () => {
        if (searchResult) {
            if (holdings.some(h => h.code === searchResult.code)) {
                toast.error('该基金已在持仓中');
                return;
            }
            setAddCode(searchResult.code);
            setAddDialogOpen(true);
        }
    };

    // 删除持仓
    const handleDelete = (code: string) => {
        const newHoldings = holdings.filter(h => h.code !== code);
        saveHoldings(newHoldings);
        fundDataMap.delete(code);
        setFundDataMap(new Map(fundDataMap));
        toast.success('已删除');
    };

    // 打开编辑弹窗
    const handleOpenEdit = (code: string, currentShares: number) => {
        setEditCode(code);
        setEditShares(currentShares.toString());
        setEditDialogOpen(true);
    };

    // 保存编辑
    const handleSaveEdit = () => {
        const newShares = parseFloat(editShares) || 0;
        if (newShares < 0) {
            toast.error('份额不能为负数');
            return;
        }

        const newHoldings = holdings.map(h =>
            h.code === editCode ? { ...h, shares: newShares } : h
        );
        saveHoldings(newHoldings);
        setEditDialogOpen(false);
        toast.success('份额已更新');

        // 刷新数据以更新计算
        refreshHoldings();
    };

    // 计算汇总
    const summary = holdings.reduce((acc, holding) => {
        const fund = fundDataMap.get(holding.code);
        if (fund && holding.shares > 0) {
            acc.totalValue += calculateMarketValue(fund, holding.shares);
            acc.totalChange += calculateChange(fund, holding.shares);
        }
        return acc;
    }, { totalValue: 0, totalChange: 0 });

    return (
        <div className="space-y-8">
            {/* 头部 */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">基金估值</h1>
                    <p className="text-base text-gray-600 dark:text-gray-400">实时追踪基金净值估算</p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" onClick={refreshHoldings} disabled={loadingHoldings} className="gap-2">
                        <RefreshCw className={cn("w-4 h-4", loadingHoldings && "animate-spin")} />
                        <span className="hidden sm:inline">刷新</span>
                    </Button>
                    <Button
                        onClick={() => setAddDialogOpen(true)}
                        className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 shadow-md gap-2"
                    >
                        <Plus className="w-4 h-4" />
                        添加持仓
                    </Button>
                </div>
            </div>

            {/* 快速查询 */}
            <Card className="border-0 shadow-lg bg-white/80 dark:bg-gray-900/80 backdrop-blur">
                <CardHeader className="pb-3">
                    <CardTitle className="text-lg flex items-center gap-2">
                        <Search className="w-5 h-5 text-purple-500" />
                        快速查询
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex gap-3">
                        <Input
                            placeholder="输入6位基金代码，如 110022"
                            value={searchCode}
                            onChange={(e) => setSearchCode(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                            className="flex-1"
                        />
                        <Button onClick={handleSearch} disabled={searching} className="gap-2">
                            {searching ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                            查询
                        </Button>
                    </div>

                    {/* 查询结果 */}
                    {searchError && (
                        <p className="text-red-500 text-sm mt-3">{searchError}</p>
                    )}

                    {searchResult && (
                        <div className="mt-4">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-gray-500">查询结果</span>
                                <Button size="sm" variant="outline" onClick={handleQuickAdd} className="gap-1">
                                    <Plus className="w-3 h-3" />
                                    添加到持仓
                                </Button>
                            </div>
                            <FundCard fund={searchResult} />
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* 持仓汇总 */}
            {holdings.length > 0 && (
                <Card className="border-0 shadow-lg bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white">
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
                                <Wallet className="w-5 h-5" />
                            </div>
                            <h3 className="text-lg font-semibold">持仓汇总</h3>
                            <Badge variant="secondary" className="bg-white/20 text-white border-0">
                                {holdings.length} 只基金
                            </Badge>
                        </div>
                        <div className="grid grid-cols-2 gap-6">
                            <div>
                                <p className="text-sm text-white/70 mb-1">总市值</p>
                                <p className="text-3xl font-bold">¥{summary.totalValue.toFixed(2)}</p>
                            </div>
                            <div className="text-right">
                                <p className="text-sm text-white/70 mb-1">今日盈亏</p>
                                <p className={cn(
                                    "text-3xl font-bold",
                                    summary.totalChange >= 0 ? "text-yellow-200" : "text-green-200"
                                )}>
                                    {summary.totalChange >= 0 ? '+' : ''}¥{summary.totalChange.toFixed(2)}
                                </p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* 持仓列表 */}
            {holdings.length > 0 ? (
                <div>
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-purple-500" />
                        我的持仓
                    </h2>
                    {loadingHoldings && holdings.length > fundDataMap.size ? (
                        <div className="flex items-center justify-center py-12">
                            <Loader2 className="w-8 h-8 animate-spin text-purple-500" />
                        </div>
                    ) : (
                        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                            {holdings.map(holding => {
                                const fund = fundDataMap.get(holding.code);
                                return fund ? (
                                    <FundCard
                                        key={holding.code}
                                        fund={fund}
                                        holding={holding}
                                        onDelete={handleDelete}
                                        onEdit={handleOpenEdit}
                                    />
                                ) : (
                                    <Card key={holding.code} className="border-0 shadow-md bg-gray-50 dark:bg-gray-800">
                                        <CardContent className="p-4 flex items-center justify-center h-32">
                                            <div className="text-center">
                                                <p className="text-gray-500 mb-1">{holding.code}</p>
                                                <Loader2 className="w-5 h-5 animate-spin mx-auto text-gray-400" />
                                            </div>
                                        </CardContent>
                                    </Card>
                                );
                            })}
                        </div>
                    )}
                </div>
            ) : (
                <Card className="border-0 shadow-md bg-gray-50 dark:bg-gray-800">
                    <CardContent className="py-12 text-center">
                        <Wallet className="w-12 h-12 mx-auto text-gray-300 mb-4" />
                        <p className="text-gray-500 mb-4">还没有添加持仓基金</p>
                        <Button onClick={() => setAddDialogOpen(true)} className="gap-2">
                            <Plus className="w-4 h-4" />
                            添加第一只基金
                        </Button>
                    </CardContent>
                </Card>
            )}

            {/* 添加持仓弹窗 */}
            <Dialog open={addDialogOpen} onOpenChange={setAddDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>添加持仓基金</DialogTitle>
                        <DialogDescription>
                            输入基金代码和持有份额
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <Label htmlFor="fund-code">基金代码</Label>
                            <Input
                                id="fund-code"
                                placeholder="如 110022"
                                value={addCode}
                                onChange={(e) => setAddCode(e.target.value)}
                                maxLength={6}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="fund-shares">持有份额（可选）</Label>
                            <Input
                                id="fund-shares"
                                type="number"
                                placeholder="如 1000"
                                value={addShares}
                                onChange={(e) => setAddShares(e.target.value)}
                            />
                            <p className="text-xs text-gray-500">填写份额后可计算今日盈亏</p>
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setAddDialogOpen(false)}>取消</Button>
                        <Button onClick={handleAddToHoldings}>添加</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* 编辑持仓弹窗 */}
            <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>修改持仓份额</DialogTitle>
                        <DialogDescription>
                            基金代码: {editCode}
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <Label htmlFor="edit-shares">持有份额</Label>
                            <Input
                                id="edit-shares"
                                type="number"
                                placeholder="如 1000"
                                value={editShares}
                                onChange={(e) => setEditShares(e.target.value)}
                                autoFocus
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setEditDialogOpen(false)}>取消</Button>
                        <Button onClick={handleSaveEdit}>保存</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
