import { z } from "zod";
import { MIN_PASSWORD_LENGTH, MIN_NAME_LENGTH } from "./constants";

// Password validation helper
const passwordSchema = z
    .string()
    .min(MIN_PASSWORD_LENGTH, `Password must be at least ${MIN_PASSWORD_LENGTH} characters`)
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[0-9]/, "Password must contain at least one number");

// Sign Up validation schema
export const signUpSchema = z
    .object({
        name: z.string().min(MIN_NAME_LENGTH, `Name must be at least ${MIN_NAME_LENGTH} characters`),
        email: z.string().email("Please enter a valid email address"),
        password: passwordSchema,
        confirmPassword: z.string(),
        agreeToTerms: z.boolean().refine((val) => val === true, {
            message: "You must agree to the terms to continue",
        }),
    })
    .refine((data) => data.password === data.confirmPassword, {
        message: "Passwords do not match",
        path: ["confirmPassword"],
    });

// Sign In validation schema
export const signInSchema = z.object({
    email: z.string().email("Please enter a valid email address"),
    password: z.string().min(1, "Password is required"),
    rememberMe: z.boolean().optional(),
});

// Reset Password validation schema
export const resetPasswordSchema = z.object({
    email: z.string().email("Please enter a valid email address"),
});

// New Password validation schema
export const newPasswordSchema = z
    .object({
        password: passwordSchema,
        confirmPassword: z.string(),
    })
    .refine((data) => data.password === data.confirmPassword, {
        message: "Passwords do not match",
        path: ["confirmPassword"],
    });

// Profile validation schema
export const profileSchema = z.object({
    name: z.string().min(MIN_NAME_LENGTH, `Name must be at least ${MIN_NAME_LENGTH} characters`),
    country: z.string().min(1, "Country is required"),
    customInstructions: z.string().max(500, "Custom instructions must be 500 characters or less").optional(),
});

// OTP validation schema
export const otpSchema = z.object({
    code: z.string().length(6, "OTP must be 6 digits"),
});

// Password strength calculator
export function calculatePasswordStrength(password: string): {
    strength: "weak" | "medium" | "strong";
    score: number;
} {
    let score = 0;

    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;

    if (score <= 2) return { strength: "weak", score };
    if (score <= 4) return { strength: "medium", score };
    return { strength: "strong", score };
}

// Email validation helper
export function isValidEmail(email: string): boolean {
    return z.string().email().safeParse(email).success;
}
