import axios from 'axios';
import emailjs from '@emailjs/browser';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Types
export interface Lead {
    company_name: string;
    email?: string;
    quote_value: number;
    item_count: number;
    conversion_days: number;
    lead_score?: number;
    conversion_probability?: number;
    industry?: string;
    segment?: string;
    maturity_level?: string;
}

export interface UseCase {
    id: string;
    title: string;
    description: string;
    industry: string;
    pain_points: string[];
    solution_summary: string;
    success_metrics?: string;
    relevant_segments: string[];
}

export interface MatchResults {
    recommended_use_case: UseCase;
    segment_assigned: string;
    maturity_level: string;
    industry_detected: string;
}

export interface LeadInput {
    quote_value: number;
    item_count: number;
    conversion_days: number;
    company_name?: string;
}

export interface LeadScoreResponse {
    lead_score: number;
    conversion_probability: number;
}

export interface EmailInput {
    customer_name: string;
    customer_email?: string;
    lead_score: number;
    quote_value: number;
    item_count: number;
    use_case_id?: string;
}

export interface SendEmailInput {
    customer_name: string;
    customer_email: string;
    lead_score: number;
    quote_value: number;
    item_count: number;
    subject?: string;
    use_case_id?: string;
    email_body?: string;
}

export interface SendEmailResponse {
    success: boolean;
    message: string;
    email_body: string;
}

export interface ScheduleEmailInput {
    customer_name: string;
    customer_email: string;
    subject: string;
    lead_score: number;
    quote_value: number;
    item_count: number;
    scheduled_at: string;
}

export interface ScheduledEmail {
    _id: string;
    customer_name: string;
    customer_email: string;
    subject: string;
    lead_score: number;
    quote_value: number;
    item_count: number;
    scheduled_at: string;
    status: 'pending' | 'sent' | 'failed' | 'cancelled';
    created_at: string;
    sent_at: string | null;
}

const EMAILJS_SERVICE_ID = import.meta.env.VITE_EMAILJS_SERVICE_ID;
const EMAILJS_TEMPLATE_ID = import.meta.env.VITE_EMAILJS_TEMPLATE_ID;
const EMAILJS_PUBLIC_KEY = import.meta.env.VITE_EMAILJS_PUBLIC_KEY;

const sendEmailWithEmailJS = async ({
    customer_name,
    customer_email,
    subject,
    email_body,
}: {
    customer_name: string;
    customer_email: string;
    subject: string;
    email_body: string;
}) => {
    if (!EMAILJS_SERVICE_ID || !EMAILJS_TEMPLATE_ID || !EMAILJS_PUBLIC_KEY) {
        throw new Error(
            'EmailJS environment variables are missing. Please set VITE_EMAILJS_SERVICE_ID, VITE_EMAILJS_TEMPLATE_ID, and VITE_EMAILJS_PUBLIC_KEY.'
        );
    }

    const templateParams = {
        to_email: customer_email,
        to_name: customer_name,
        subject: subject,
        message: email_body,
        from_name: 'AI Outbound Sales',
    };

    return emailjs.send(
        EMAILJS_SERVICE_ID,
        EMAILJS_TEMPLATE_ID,
        templateParams,
        {
            publicKey: EMAILJS_PUBLIC_KEY,
        }
    );
};

// API Functions
export const apiService = {
    async healthCheck(): Promise<{ status: string }> {
        const response = await api.get('/health');
        return response.data;
    },

    async getLeads(): Promise<Lead[]> {
        const response = await api.get('/leads');
        return response.data;
    },

    async getUseCases(): Promise<UseCase[]> {
        const response = await api.get('/use-cases');
        return response.data;
    },

    async matchUseCase(data: LeadInput): Promise<MatchResults> {
        const response = await api.post('/match-use-case', data);
        return response.data;
    },

    async predictLeadScore(data: LeadInput): Promise<LeadScoreResponse> {
        const response = await api.post('/predict', data);
        return response.data;
    },

    async generateEmail(data: EmailInput): Promise<{ email_body: string }> {
        const response = await api.post('/generate-email-llama2', data);
        return response.data;
    },

    async sendEmail(data: SendEmailInput): Promise<SendEmailResponse> {
        try {
            let finalEmailBody = data.email_body || '';

            if (!finalEmailBody) {
                const generated = await api.post('/generate-email-llama2', {
                    customer_name: data.customer_name,
                    customer_email: data.customer_email,
                    lead_score: data.lead_score,
                    quote_value: data.quote_value,
                    item_count: data.item_count,
                    use_case_id: data.use_case_id,
                });

                finalEmailBody = generated.data.email_body;
            }

            const finalSubject = data.subject || 'AI-Powered Sales Outreach';

            await sendEmailWithEmailJS({
                customer_name: data.customer_name,
                customer_email: data.customer_email,
                subject: finalSubject,
                email_body: finalEmailBody,
            });

            return {
                success: true,
                message: `Email sent successfully to ${data.customer_email}`,
                email_body: finalEmailBody,
            };
        } catch (error: any) {
            console.error('EmailJS send failed:', error);

            return {
                success: false,
                message:
                    error?.text ||
                    error?.message ||
                    'Failed to send email using EmailJS',
                email_body: data.email_body || '',
            };
        }
    },

    async scheduleEmail(data: ScheduleEmailInput): Promise<{ success: boolean; job: ScheduledEmail }> {
        const response = await api.post('/emails/schedule', data);
        return response.data;
    },

    async getScheduledEmails(): Promise<ScheduledEmail[]> {
        const response = await api.get('/emails/scheduled');
        return response.data;
    },

    async cancelScheduledEmail(jobId: string): Promise<{ success: boolean; message: string }> {
        const response = await api.delete(`/emails/scheduled/${jobId}`);
        return response.data;
    },

    async deleteScheduledEmail(jobId: string): Promise<{ success: boolean; message: string }> {
        const response = await api.delete(`/emails/scheduled/${jobId}/delete`);
        return response.data;
    },

    async sendScheduledEmailNow(jobId: string): Promise<{ success: boolean; message: string; status: string }> {
        const response = await api.post(`/emails/scheduled/${jobId}/send-now`);
        return response.data;
    },
};

export default api;