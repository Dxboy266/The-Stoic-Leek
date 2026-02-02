import { api } from '@/lib/api';

export interface GenerateRequest {
    amount: number;
    total_assets: number;
    api_key: string;
    model?: string;
    exercises?: string[];
}

export interface PrescriptionResponse {
    amount: number;
    total_assets: number;
    roi: number;
    mood: string;
    exercise: string;
    advice: string;
    full: string;
    generated_at: string;
}

export const PrescriptionService = {
    generate: (data: GenerateRequest) => api.post<any, PrescriptionResponse>('/prescription/generate', data),
    generateAnonymous: (data: GenerateRequest) => api.post<any, PrescriptionResponse>('/prescription/generate-anonymous', data),
};
