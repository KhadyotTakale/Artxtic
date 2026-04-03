import { toast } from "sonner";
import { User, Generation, PricingPlan, ApiResponse, AuthResponse, GenerationResponse } from "@/types";

const API_BASE_URL = "http://localhost:8000/api/v1";

interface RequestOptions extends RequestInit {
    params?: Record<string, string>;
}

async function fetchAPI<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const { params, ...init } = options;

    // Build URL with query params
    const url = new URL(`${API_BASE_URL}${endpoint}`);
    if (params) {
        Object.entries(params).forEach(([key, value]) => {
            if (value) url.searchParams.append(key, value);
        });
    }

    // Default headers
    const headers = {
        "Content-Type": "application/json",
        ...init.headers,
    };

    try {
        const response = await fetch(url.toString(), {
            ...init,
            headers,
            credentials: "include", // Important for cookies
        });

        const data = await response.json();

        if (!response.ok) {
            let errorMessage = data.detail || data.message || data.error?.message || "An error occurred";

            if (typeof errorMessage === 'object') {
                errorMessage = JSON.stringify(errorMessage);
            }

            toast.error(errorMessage);
            throw new Error(errorMessage);
        }

        return data;
    } catch (error) {
        if (error instanceof Error) {
            // Don't toast here if it was already toasted above
            if (!error.message) toast.error("Network error");
            throw error;
        }
        toast.error("An unknown error occurred");
        throw new Error("An unknown error occurred");
    }
}

export const api = {
    auth: {
        sendOTP: (email: string, name?: string) =>
            fetchAPI<{ message: string; email: string }>("/auth/send-otp", {
                method: "POST",
                body: JSON.stringify({ email, name }),
            }),

        verifyOTP: (email: string, otp: string, name?: string) =>
            fetchAPI<AuthResponse>("/auth/verify-otp-login", {
                method: "POST",
                body: JSON.stringify({ email, otp, name }),
            }),

        getMe: () =>
            fetchAPI<{ data: User }>("/auth/me"),

        logout: () =>
            fetchAPI<{ message: string }>("/auth/logout", { method: "POST" }),

        forgotPassword: (email: string) =>
            fetchAPI<{ message: string }>("/auth/forgot-password", {
                method: "POST",
                body: JSON.stringify({ email }),
            }),

        resetPassword: (token: string, newPassword: string) =>
            fetchAPI<{ message: string }>("/auth/reset-password", {
                method: "POST",
                body: JSON.stringify({ token, new_password: newPassword }),
            }),
    },

    generation: {
        createImage: (data: any) =>
            fetchAPI<{ job_id: string; status: string; message: string; error_message?: string }>("/generate/image", {
                method: "POST",
                body: JSON.stringify(data),
            }),

        createVideo: (data: any) =>
            fetchAPI<{ job_id: string; status: string; message: string; error_message?: string }>("/generate/video", {
                method: "POST",
                body: JSON.stringify(data),
            }),

        getStatus: (jobId: string) =>
            fetchAPI<GenerationResponse>(`/generate/status/${jobId}`),
    },

    library: {
        getHistory: () =>
            fetchAPI<{ data: Generation[]; total: number; page: number; total_pages: number }>("/library/history"),

        getStarred: () =>
            fetchAPI<{ data: Generation[]; total: number; page: number; total_pages: number }>("/library/starred"),

        toggleStar: (id: string) =>
            fetchAPI<{ starred: boolean }>(`/library/${id}/star`, { method: "POST" }),

        delete: (id: string) =>
            fetchAPI<{ message: string }>(`/library/${id}`, { method: "DELETE" }),
    },

    user: {
        getProfile: () =>
            fetchAPI<{ data: User }>("/user/profile"),

        updateProfile: (data: Partial<User>) =>
            fetchAPI<{ message: string }>("/user/profile", {
                method: "PUT",
                body: JSON.stringify(data),
            }),

        getSubscription: () =>
            fetchAPI<{ data: any }>("/user/subscription"),
    },

    subscription: {
        getPlans: () =>
            fetchAPI<{ success: boolean; data: any[] }>("/subscription/plans"),

        createCheckout: (planId: string) =>
            fetchAPI<{ checkout_url: string }>("/subscription/checkout", {
                method: "POST",
                body: JSON.stringify({ plan_id: planId }),
            }),
    }
};
