"use client";

import { useState, FormEvent, useRef, KeyboardEvent } from "react";
import Link from "next/link";
import { useAuth } from "@/contexts/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function SignUpPage() {
    const { sendOTP, verifyOTPAndSignup, isLoading } = useAuth();
    const [step, setStep] = useState<"email" | "otp">("email");
    const [formData, setFormData] = useState({
        name: "",
        email: "",
    });
    const [otp, setOtp] = useState(["", "", "", "", "", ""]);
    const [errors, setErrors] = useState<Record<string, string>>({});
    const [countdown, setCountdown] = useState(0);
    const otpRefs = useRef<(HTMLInputElement | null)[]>([]);

    const validateEmail = () => {
        const newErrors: Record<string, string> = {};

        if (!formData.name.trim()) {
            newErrors.name = "Name is required";
        }

        if (!formData.email.trim()) {
            newErrors.email = "Email is required";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
            newErrors.email = "Invalid email address";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSendOTP = async (e: FormEvent) => {
        e.preventDefault();

        if (!validateEmail()) return;

        try {
            await sendOTP(formData.email);
            setStep("otp");
            setCountdown(60);

            // Start countdown
            const timer = setInterval(() => {
                setCountdown((prev) => {
                    if (prev <= 1) {
                        clearInterval(timer);
                        return 0;
                    }
                    return prev - 1;
                });
            }, 1000);
        } catch (error) {
            setErrors({ submit: "Failed to send OTP. Please try again." });
        }
    };

    const handleResendOTP = async () => {
        try {
            await sendOTP(formData.email);
            setCountdown(60);

            const timer = setInterval(() => {
                setCountdown((prev) => {
                    if (prev <= 1) {
                        clearInterval(timer);
                        return 0;
                    }
                    return prev - 1;
                });
            }, 1000);
        } catch (error) {
            setErrors({ submit: "Failed to resend OTP. Please try again." });
        }
    };

    const handleOTPChange = (index: number, value: string) => {
        if (!/^\d*$/.test(value)) return;

        const newOtp = [...otp];
        newOtp[index] = value.slice(-1);
        setOtp(newOtp);

        // Auto-advance to next input
        if (value && index < 5) {
            otpRefs.current[index + 1]?.focus();
        }
    };

    const handleOTPKeyDown = (index: number, e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Backspace" && !otp[index] && index > 0) {
            otpRefs.current[index - 1]?.focus();
        }
    };

    const handleOTPPaste = (e: React.ClipboardEvent) => {
        e.preventDefault();
        const pastedData = e.clipboardData.getData("text").slice(0, 6);
        if (!/^\d+$/.test(pastedData)) return;

        const newOtp = pastedData.split("").concat(Array(6).fill("")).slice(0, 6);
        setOtp(newOtp);

        const lastFilledIndex = Math.min(pastedData.length - 1, 5);
        otpRefs.current[lastFilledIndex]?.focus();
    };

    const handleVerifyOTP = async (e: FormEvent) => {
        e.preventDefault();

        const otpValue = otp.join("");
        if (otpValue.length !== 6) {
            setErrors({ otp: "Please enter all 6 digits" });
            return;
        }

        try {
            await verifyOTPAndSignup(formData.name, formData.email, otpValue);
        } catch (error) {
            setErrors({ submit: "Invalid OTP. Please try again." });
        }
    };

    const handleChange = (field: string, value: string) => {
        setFormData(prev => ({ ...prev, [field]: value }));
        if (errors[field]) {
            setErrors(prev => ({ ...prev, [field]: "" }));
        }
    };

    if (step === "otp") {
        return (
            <div className="w-full max-w-md space-y-8">
                <div className="text-center space-y-2">
                    <h2 className="text-4xl font-bold text-black">Verify OTP</h2>
                    <p className="text-gray-600">
                        Enter the 6-digit code sent to<br />
                        <span className="font-medium text-black">{formData.email}</span>
                    </p>
                </div>

                <form className="space-y-6 mt-8" onSubmit={handleVerifyOTP}>
                    <div className="flex justify-center gap-3">
                        {otp.map((digit, index) => (
                            <input
                                key={index}
                                ref={(el: HTMLInputElement | null) => { otpRefs.current[index] = el }}
                                type="text"
                                inputMode="numeric"
                                maxLength={1}
                                value={digit}
                                onChange={(e) => handleOTPChange(index, e.target.value)}
                                onKeyDown={(e) => handleOTPKeyDown(index, e)}
                                onPaste={index === 0 ? handleOTPPaste : undefined}
                                className="w-12 h-14 text-center text-2xl font-bold text-black bg-white border-2 border-gray-300 rounded-lg focus:border-black focus:outline-none focus:ring-2 focus:ring-black/10 transition-all"
                                disabled={isLoading}
                            />
                        ))}
                    </div>

                    {errors.otp && (
                        <p className="text-sm text-red-600 text-center">{errors.otp}</p>
                    )}

                    {errors.submit && (
                        <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-sm text-red-600 text-center">{errors.submit}</p>
                        </div>
                    )}

                    <Button
                        type="submit"
                        variant="primary"
                        size="lg"
                        fullWidth
                        loading={isLoading}
                    >
                        Verify & Create Account
                    </Button>

                    <div className="text-center text-sm">
                        {countdown > 0 ? (
                            <span className="text-gray-600">
                                Resend OTP in {countdown}s
                            </span>
                        ) : (
                            <button
                                type="button"
                                onClick={handleResendOTP}
                                className="font-medium text-black hover:underline"
                            >
                                Resend OTP
                            </button>
                        )}
                    </div>

                    <div className="text-center text-sm">
                        <button
                            type="button"
                            onClick={() => setStep("email")}
                            className="text-gray-600 hover:text-black"
                        >
                            ← Change email
                        </button>
                    </div>
                </form>
            </div>
        );
    }

    return (
        <div className="w-full max-w-md space-y-8">
            <div className="text-center space-y-2">
                <h2 className="text-4xl font-bold text-black">Create Account</h2>
                <p className="text-gray-600">
                    Start creating amazing content with AI
                </p>
            </div>

            <form className="space-y-6 mt-8" onSubmit={handleSendOTP}>
                <Input
                    label="Full Name"
                    type="text"
                    value={formData.name}
                    onChange={(e) => handleChange("name", e.target.value)}
                    placeholder="John Doe"
                    error={errors.name}
                    disabled={isLoading}
                />

                <Input
                    label="Email Address"
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleChange("email", e.target.value)}
                    placeholder="john@example.com"
                    error={errors.email}
                    disabled={isLoading}
                />

                {errors.submit && (
                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-sm text-red-600">{errors.submit}</p>
                    </div>
                )}

                <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    fullWidth
                    loading={isLoading}
                >
                    Send OTP
                </Button>
            </form>

            <div className="text-center text-sm">
                <span className="text-gray-600">Already have an account? </span>
                <Link href="/sign-in" className="font-medium text-black hover:underline">
                    Sign In
                </Link>
            </div>
        </div>
    );
}
