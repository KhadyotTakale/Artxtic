// TypeScript type definitions for Artxctic

export interface User {
    id: string;
    name: string;
    email: string;
    avatar?: string;
    country: string;
    customInstructions?: string;
    plan: "free" | "pro" | "enterprise";
    subscriptionRenewalDate?: string;
    createdAt: string;
}

export interface Generation {
    id: string;
    prompt: string;
    type: "image" | "video";
    url: string;
    thumbnailUrl: string;
    model: string;
    aspectRatio: string;
    starred: boolean;
    createdAt: string;
    duration?: string; // for videos
    status?: "pending" | "processing" | "completed" | "failed";
}

export interface PricingPlan {
    id: string;
    name: string;
    price: number;
    currency: string;
    billing: string;
    features: PricingFeature[];
    cta: string;
    recommended: boolean;
}

export interface PricingFeature {
    text: string;
    included: boolean;
}

export interface Testimonial {
    id: string;
    quote: string;
    author: string;
    role: string;
    avatar: string;
}

export interface SamplePrompt {
    text: string;
    category?: string;
}

// Form types
export interface SignUpFormData {
    name: string;
    email: string;
    password: string;
    confirmPassword: string;
    agreeToTerms: boolean;
}

export interface SignInFormData {
    email: string;
    password: string;
    rememberMe: boolean;
}

export interface ResetPasswordFormData {
    email: string;
}

export interface NewPasswordFormData {
    password: string;
    confirmPassword: string;
}

export interface ProfileFormData {
    name: string;
    country: string;
    customInstructions?: string;
}

export interface GenerationConfig {
    mediaType: "image" | "video";
    aspectRatio: string;
    model: string;
    referenceImage?: File;
}

// API Response types (for future backend integration)
export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
    message?: string;
}

export interface AuthResponse {
    user: User;
    token: string;
}

export interface GenerationResponse {
    job_id: string;
    status: string;
    media?: {
        id: string;
        type: string;
        url: string;
        thumbnail_url?: string;
        prompt: string;
        aspect_ratio?: string;
        model_used?: string;
        file_size?: number;
        width?: number;
        height?: number;
        duration?: number;
        is_starred?: boolean;
        created_at: string;
    }[];
    error_message?: string;
}

// Toast types
export type ToastType = "success" | "error" | "info" | "warning";

export interface Toast {
    id: string;
    type: ToastType;
    message: string;
    duration?: number;
}

// Filter types
export type MediaFilter = "all" | "images" | "videos";
export type LibraryTab = "starred" | "history";
