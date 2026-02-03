'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { Loader2 } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AuthService } from '@/services/auth';
import { useUserStore } from '@/store/user';

const formSchema = z.object({
    email: z.string().email('请输入有效的邮箱'),
    password: z.string().min(6, '密码至少 6 位'),
});

export function AuthForm() {
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
    const setAuth = useUserStore((state) => state.setAuth);

    const loginForm = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: { email: '', password: '' },
    });

    const registerForm = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: { email: '', password: '' },
    });

    async function onLogin(values: z.infer<typeof formSchema>) {
        setIsLoading(true);
        try {
            const res = await AuthService.login(values) as any;
            setAuth(res.user, res.access_token);
            toast.success('登录成功');
            router.push('/');
        } catch (error: any) {
            toast.error(error.detail || '登录失败');
        } finally {
            setIsLoading(false);
        }
    }

    async function onRegister(values: z.infer<typeof formSchema>) {
        setIsLoading(true);
        try {
            await AuthService.register(values);
            toast.success('注册成功！请查收验证邮件');
            // 可以在这里自动切换到登录 tab
        } catch (error: any) {
            toast.error(error.detail || '注册失败');
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <Card className="w-full max-w-md mx-auto backdrop-blur-md bg-white/80 dark:bg-black/50 border-white/20 shadow-xl">
            <CardHeader className="text-center space-y-2">
                <div className="mx-auto w-16 h-16 bg-gradient-to-tr from-green-400 to-blue-500 rounded-2xl flex items-center justify-center text-3xl shadow-lg mb-2">
                    🌱
                </div>
                <CardTitle className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
                    韭菜的自我修养
                </CardTitle>
                <CardDescription>
                    Market volatility is noise; Muscle pain is real.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <Tabs defaultValue="login" className="w-full">
                    <TabsList className="grid w-full grid-cols-2 mb-4">
                        <TabsTrigger value="login">登录</TabsTrigger>
                        <TabsTrigger value="register">注册</TabsTrigger>
                    </TabsList>

                    <TabsContent value="login">
                        <Form {...loginForm}>
                            <form onSubmit={loginForm.handleSubmit(onLogin)} className="space-y-4">
                                <FormField
                                    control={loginForm.control}
                                    name="email"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>邮箱</FormLabel>
                                            <FormControl>
                                                <Input placeholder="leek@example.com" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={loginForm.control}
                                    name="password"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>密码</FormLabel>
                                            <FormControl>
                                                <Input type="password" placeholder="******" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <Button type="submit" className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-300" disabled={isLoading}>
                                    {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                    登录
                                </Button>
                            </form>
                        </Form>
                    </TabsContent>

                    <TabsContent value="register">
                        <Form {...registerForm}>
                            <form onSubmit={registerForm.handleSubmit(onRegister)} className="space-y-4">
                                <FormField
                                    control={registerForm.control}
                                    name="email"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>邮箱</FormLabel>
                                            <FormControl>
                                                <Input placeholder="leek@example.com" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={registerForm.control}
                                    name="password"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>密码</FormLabel>
                                            <FormControl>
                                                <Input type="password" placeholder="至少 6 位" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <Button type="submit" className="w-full" variant="outline" disabled={isLoading}>
                                    {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                    注册
                                </Button>
                            </form>
                        </Form>
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    );
}
