"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter, usePathname } from "next/navigation";
import { User } from "@/types";
import { api } from "@/lib/api";
import { toast } from "sonner";

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    sendOTP: (email: string, name?: string) => Promise<void>;
    verifyOTPAndSignup: (name: string, email: string, otp: string) => Promise<void>;
    verifyOTPAndLogin: (email: string, otp: string) => Promise<void>;
    logout: () => void;
    forgotPassword: (email: string) => Promise<void>;
    resetPassword: (token: string, newPassword: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();
    const pathname = usePathname();

    const isPublicRoute = (path: string) => {
        return ["/sign-in", "/sign-up", "/"].includes(path);
    };

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await api.auth.getMe();
                setUser(response.data);
            } catch (error) {
                console.error("Not authenticated", error);
                setUser(null);
                if (!isPublicRoute(pathname)) {
                    router.push("/sign-in");
                }
            } finally {
                setIsLoading(false);
            }
        };

        checkAuth();
    }, [pathname]);

    const sendOTP = async (email: string, name?: string): Promise<void> => {
        await api.auth.sendOTP(email, name);
        toast.success(`OTP sent to ${email}`);
    };

    const verifyOTPAndSignup = async (name: string, email: string, otp: string): Promise<void> => {
        setIsLoading(true);
        try {
            const response = await api.auth.verifyOTP(email, otp, name);
            setUser(response.user);
            toast.success("Account created successfully!");
            router.push("/playground");
        } catch (error) {
            console.error("Signup failed", error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const verifyOTPAndLogin = async (email: string, otp: string): Promise<void> => {
        setIsLoading(true);
        try {
            const response = await api.auth.verifyOTP(email, otp);
            setUser(response.user);
            toast.success("Logged in successfully!");
            router.push("/playground");
        } catch (error) {
            console.error("Login failed", error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const logout = async () => {
        try {
            await api.auth.logout();
        } catch (error) {
            console.error("Logout failed", error);
        } finally {
            setUser(null);
            router.push("/sign-in");
            toast.success("Logged out successfully");
        }
    };

    const forgotPassword = async (email: string): Promise<void> => {
        setIsLoading(true);
        try {
            await api.auth.forgotPassword(email);
            toast.success("Password reset email sent (if account exists)");
        } catch (error) {
            console.error("Forgot password failed", error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const resetPassword = async (token: string, newPassword: string): Promise<void> => {
        setIsLoading(true);
        try {
            await api.auth.resetPassword(token, newPassword);
            toast.success("Password reset successful. Please login.");
            router.push("/sign-in");
        } catch (error) {
            console.error("Reset password failed", error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                isLoading,
                sendOTP,
                verifyOTPAndSignup,
                verifyOTPAndLogin,
                logout,
                forgotPassword,
                resetPassword,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}

