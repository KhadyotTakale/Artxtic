"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";
import { useAuth } from "@/contexts/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function ResetPasswordPage() {
    const { forgotPassword, isLoading } = useAuth();
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const [submitted, setSubmitted] = useState(false);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (!email.trim()) {
            setError("Email is required");
            return;
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            setError("Invalid email address");
            return;
        }

        try {
            await forgotPassword(email);
            setSubmitted(true);
        } catch (err) {
            setError("Failed to send reset email. Please try again.");
        }
    };

    if (submitted) {
        return (
            <div className="w-full max-w-md space-y-8">
                <div className="text-center space-y-4">
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                        <span className="material-icons text-3xl text-green-600">check_circle</span>
                    </div>
                    <h2 className="text-4xl font-serif text-black">Check Your Email</h2>
                    <p className="text-gray-600 font-light">
                        We've sent a password reset link to <br />
                        <span className="font-medium text-black">{email}</span>
                    </p>
                </div>

                <div className="text-center">
                    <Link
                        href="/sign-in"
                        className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-black transition-colors"
                    >
                        <span className="material-icons text-base mr-1">arrow_back</span>
                        Back to Sign In
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="w-full max-w-md space-y-8">
            <div className="text-center space-y-2">
                <h2 className="text-4xl font-serif text-black">Reset Password</h2>
                <p className="text-gray-600 font-light">
                    Enter your email and we'll send you a link to reset your password
                </p>
            </div>

            <form className="space-y-6 mt-8" onSubmit={handleSubmit}>
                <Input
                    label="Email Address"
                    type="email"
                    value={email}
                    onChange={(e) => {
                        setEmail(e.target.value);
                        setError("");
                    }}
                    placeholder="john@example.com"
                    error={error}
                    disabled={isLoading}
                />

                <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    fullWidth
                    loading={isLoading}
                >
                    Send Reset Link
                </Button>
            </form>

            <div className="text-center">
                <Link
                    href="/sign-in"
                    className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-black transition-colors"
                >
                    <span className="material-icons text-base mr-1">arrow_back</span>
                    Back to Sign In
                </Link>
            </div>
        </div>
    );
}
