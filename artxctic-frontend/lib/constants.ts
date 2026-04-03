// App-wide constants

export const APP_NAME = "Artxctic";
export const APP_DESCRIPTION = "AI-powered media generation platform";

// File upload limits
export const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
export const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"];

// Character limits
export const MAX_PROMPT_LENGTH = 2000;
export const MAX_CUSTOM_INSTRUCTIONS_LENGTH = 500;
export const MIN_PASSWORD_LENGTH = 8;
export const MIN_NAME_LENGTH = 2;

// OTP
export const OTP_LENGTH = 6;
export const OTP_RESEND_TIMEOUT = 60; // seconds

// Routes
export const ROUTES = {
  HOME: "/",
  SIGN_UP: "/sign-up",
  SIGN_IN: "/sign-in",
  VERIFY_OTP: "/verify-otp",
  RESET_PASSWORD: "/reset-password",
  RESET_PASSWORD_CONFIRM: "/reset-password/confirm",
  PLAYGROUND: "/playground",
  LIBRARY: "/library",
  PROFILE: "/profile",
  PRICING: "/pricing",
  PAYMENT_SUCCESS: "/payment-success",
  PAYMENT_FAILURE: "/payment-failure",
} as const;

// Media types
export const MEDIA_TYPES = {
  IMAGE: "image",
  VIDEO: "video",
} as const;

// Aspect ratios
export const ASPECT_RATIOS = [
  { value: "9:16", label: "9:16 (Portrait)" },
  { value: "16:9", label: "16:9 (Landscape)" },
  { value: "1:1", label: "1:1 (Square)" },
  { value: "4:5", label: "4:5 (Portrait)" },
] as const;

// AI Models
export const AI_MODELS = [
  { value: "model-1", label: "Model 1" },
  { value: "model-2", label: "Model 2" },
] as const;

// Pricing plans
export const PLAN_TYPES = {
  FREE: "free",
  PRO: "pro",
  ENTERPRISE: "enterprise",
} as const;

// Toast duration
export const TOAST_DURATION = 3000; // milliseconds

// Animation durations
export const ANIMATION_DURATION = {
  FAST: 150,
  NORMAL: 200,
  SLOW: 300,
} as const;
