'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { LogOut, User } from 'lucide-react';
import { useUserStore } from '@/store/user';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

export function Navbar() {
    return (
        <nav className="flex items-center justify-between py-4 mb-8">
            <Link href="/" className="flex items-center space-x-2 group">
                <div className="w-12 h-12 relative overflow-hidden rounded-xl shadow-md group-hover:scale-110 transition-transform bg-white">
                    <Image src="/logo.png" alt="Logo" fill className="object-cover" />
                </div>
                <div className="flex flex-col">
                    <span className="font-bold text-lg leading-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">
                        The Stoic Leek
                    </span>
                    <span className="text-xs text-muted-foreground font-medium">韭菜的自我修养</span>
                </div>
            </Link>

            <div className="flex items-center space-x-4">
                {/* 右侧区域留空或用于未来扩展 */}
            </div>
        </nav>
    );
}
