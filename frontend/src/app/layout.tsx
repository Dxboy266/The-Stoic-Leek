import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Toaster } from '@/components/ui/sonner';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: '韭菜的自我修养 - The Stoic Leek',
  description: '市场涨跌皆虚妄，唯有酸痛最真实。',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
          <main className="container mx-auto px-4 py-8 max-w-5xl">
            {children}
          </main>
          <Toaster />
        </div>
      </body>
    </html>
  );
}
