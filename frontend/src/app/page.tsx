'use client';
import { useEffect, useState } from 'react';
import Image from 'next/image';

import { useUserStore } from '@/store/user';
import { Navbar } from '@/components/shared/navbar';
import { PrescriptionGenerator } from '@/components/features/prescription-generator';
import { MarketDashboard } from '@/components/features/market';
import { AcademyDashboard } from '@/components/features/academy';
import { SettingsPage } from '@/components/features/settings';
import { FundDashboard } from '@/components/features/fund';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Activity, CandlestickChart, GraduationCap, Settings, TrendingUp } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function HomePage() {
  const { settings, updateSettings, isLoaded, setLoaded } = useUserStore();
  const [landingVisible, setLandingVisible] = useState(true);

  // 从 LocalStorage 加载数据 (只执行一次)
  useEffect(() => {
    if (isLoaded) return;

    // 优先尝试从 LocalStorage 读取
    const localData = localStorage.getItem('stoic_leek_data');
    if (localData) {
      try {
        const parsed = JSON.parse(localData);
        updateSettings(parsed);
        console.log("✅ 从 LocalStorage 加载数据:", parsed);
      } catch (e) {
        console.error("解析本地数据失败", e);
      }
    }

    // 标记加载完成
    setLoaded(true);
  }, [isLoaded, setLoaded, updateSettings]);

  // 数据变化时保存到 LocalStorage (Web 版独立数据)
  useEffect(() => {
    if (!isLoaded) return; // 首次加载未完成时不保存
    if (Object.keys(settings).length === 0) return; // 空数据不保存

    try {
      localStorage.setItem('stoic_leek_data', JSON.stringify(settings));
      console.log("💾 数据已保存到 LocalStorage");
    } catch (e) {
      console.error("❌ LocalStorage 保存失败:", e);
    }
  }, [settings, isLoaded]);

  if (landingVisible) {
    return (
      <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900 items-center justify-center p-4">
        <div className="animate-in fade-in zoom-in duration-700 text-center flex flex-col items-center">
          <div className="relative w-48 h-48 mb-8 rounded-3xl overflow-hidden shadow-2xl hover:scale-105 transition-transform">
            <Image src="/logo.png" alt="Stoic Leek" fill className="object-cover" />
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-blue-600 mb-6 pb-2">
            韭菜的自我修养
          </h1>
          <p className="text-gray-500 max-w-md mb-10 text-lg text-center">
            市场涨跌皆虚妄<br />
            唯有酸痛最真实
          </p>
          <Button
            size="lg"
            onClick={() => setLandingVisible(false)}
            className="rounded-full px-12 h-14 text-lg shadow-xl"
          >
            开始自我修养
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-20 sm:pb-12 px-3 sm:px-6 lg:px-8">
      <Navbar />

      <Tabs defaultValue="fund" className="space-y-4 sm:space-y-6">
        {/* 移动端底部固定导航 / PC端顶部导航 */}
        <TabsList className="fixed bottom-0 left-0 right-0 z-50 grid w-full grid-cols-5 p-2 bg-white/95 dark:bg-gray-900/95 backdrop-blur border-t border-gray-200 dark:border-gray-800 sm:static sm:border-0 sm:w-auto sm:max-w-[600px] sm:mx-auto sm:rounded-xl sm:bg-white/50">
          <TabsTrigger value="fund" className="flex flex-col sm:flex-row items-center gap-1 sm:gap-2 py-2 sm:py-2 rounded-lg text-xs sm:text-sm data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <TrendingUp className="w-5 h-5 sm:w-4 sm:h-4" />
            <span>基金</span>
          </TabsTrigger>
          <TabsTrigger value="market" className="flex flex-col sm:flex-row items-center gap-1 sm:gap-2 py-2 sm:py-2 rounded-lg text-xs sm:text-sm data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <CandlestickChart className="w-5 h-5 sm:w-4 sm:h-4" />
            <span>市场</span>
          </TabsTrigger>
          <TabsTrigger value="prescription" className="flex flex-col sm:flex-row items-center gap-1 sm:gap-2 py-2 sm:py-2 rounded-lg text-xs sm:text-sm data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <Activity className="w-5 h-5 sm:w-4 sm:h-4" />
            <span>对冲</span>
          </TabsTrigger>
          <TabsTrigger value="academy" className="flex flex-col sm:flex-row items-center gap-1 sm:gap-2 py-2 sm:py-2 rounded-lg text-xs sm:text-sm data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <GraduationCap className="w-5 h-5 sm:w-4 sm:h-4" />
            <span>学院</span>
          </TabsTrigger>
          <TabsTrigger value="settings" className="flex flex-col sm:flex-row items-center gap-1 sm:gap-2 py-2 sm:py-2 rounded-lg text-xs sm:text-sm data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <Settings className="w-5 h-5 sm:w-4 sm:h-4" />
            <span>设置</span>
          </TabsTrigger>
        </TabsList>

        <div className="mt-2 sm:mt-8 animate-in fade-in duration-500">
          <TabsContent value="fund">
            <FundDashboard />
          </TabsContent>

          <TabsContent value="market">
            <MarketDashboard />
          </TabsContent>

          <TabsContent value="prescription" className="space-y-4">
            <PrescriptionGenerator />
          </TabsContent>

          <TabsContent value="academy">
            <AcademyDashboard />
          </TabsContent>

          <TabsContent value="settings">
            <SettingsPage />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
