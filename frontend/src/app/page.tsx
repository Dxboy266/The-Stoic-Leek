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

  // 从后端 JSON 文件加载数据 (只执行一次)
  useEffect(() => {
    if (isLoaded) return; // 已加载过，跳过

    import('@/services/persistence').then(mod => {
      const PersistenceService = mod.PersistenceService;
      PersistenceService.load().then(res => {
        if (res.data && Object.keys(res.data).length > 0) {
          updateSettings(res.data);
          console.log("✅ 从后端 JSON 加载数据:", res.data);
        }
        setLoaded(true);
      }).catch(err => {
        console.log("⚠️ 后端加载跳过 (可能后端未启动):", err);
        setLoaded(true); // 即使失败也标记为已加载
      });
    });
  }, [isLoaded, setLoaded, updateSettings]);

  // 数据变化时自动保存到后端 JSON 文件 (2秒防抖)
  useEffect(() => {
    if (!isLoaded) return; // 首次加载未完成时不保存
    if (Object.keys(settings).length === 0) return; // 空数据不保存

    const timer = setTimeout(() => {
      import('@/services/persistence').then(mod => {
        mod.PersistenceService.save(settings)
          .then(() => console.log("💾 数据已保存到后端 JSON"))
          .catch(e => console.error("❌ 保存失败:", e));
      });
    }, 2000);
    return () => clearTimeout(timer);
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
    <div className="min-h-screen pb-12">
      <Navbar />

      <Tabs defaultValue="fund" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5 lg:w-[700px] mx-auto p-1 bg-white/50 backdrop-blur rounded-xl">
          <TabsTrigger value="fund" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <TrendingUp className="w-4 h-4 mr-2" />
            <span className="hidden sm:inline">基金</span>
          </TabsTrigger>
          <TabsTrigger value="market" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <CandlestickChart className="w-4 h-4 mr-2" />
            <span className="hidden sm:inline">市场</span>
          </TabsTrigger>
          <TabsTrigger value="prescription" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <Activity className="w-4 h-4 mr-2" />
            <span className="hidden sm:inline">对冲</span>
          </TabsTrigger>
          <TabsTrigger value="academy" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <GraduationCap className="w-4 h-4 mr-2" />
            <span className="hidden sm:inline">学院</span>
          </TabsTrigger>
          <TabsTrigger value="settings" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm">
            <Settings className="w-4 h-4 mr-2" />
            <span className="hidden sm:inline">设置</span>
          </TabsTrigger>
        </TabsList>

        <div className="mt-8 animate-in fade-in duration-500">
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
