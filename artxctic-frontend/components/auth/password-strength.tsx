"use client";

import { calculatePasswordStrength } from "@/lib/validations";
import { cn } from "@/lib/utils";
import { Check } from "lucide-react";

interface PasswordStrengthProps {
    password: string;
    showRequirements?: boolean;
}

export function PasswordStrength({ password, showRequirements = true }: PasswordStrengthProps) {
    const { strength, score } = calculatePasswordStrength(password);

    const strengthColors = {
        weak: "bg-error",
        medium: "bg-warning",
        strong: "bg-success",
    };

    const strengthText = {
        weak: "Weak",
        medium: "Medium",
        strong: "Strong",
    };

    const requirements = [
        { text: "At least 8 characters", met: password.length >= 8 },
        { text: "Contains uppercase letter", met: /[A-Z]/.test(password) },
        { text: "Contains number", met: /[0-9]/.test(password) },
    ];

    if (!password) return null;

    return (
        <div className="space-y-2">
            <div className="flex items-center gap-2">
                <div className="flex-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div
                        className={cn(
                            "h-full transition-all duration-300",
                            strengthColors[strength]
                        )}
                        style={{ width: `${(score / 6) * 100}%` }}
                    />
                </div>
                <span className={cn(
                    "text-xs font-medium",
                    strength === "weak" && "text-error",
                    strength === "medium" && "text-warning",
                    strength === "strong" && "text-success"
                )}>
                    {strengthText[strength]}
                </span>
            </div>

            {showRequirements && (
                <div className="space-y-1">
                    {requirements.map((req, index) => (
                        <div key={index} className="flex items-center gap-2 text-xs">
                            <div
                                className={cn(
                                    "w-4 h-4 rounded-full flex items-center justify-center transition-colors",
                                    req.met
                                        ? "bg-success text-white"
                                        : "bg-gray-200 dark:bg-gray-700 text-gray-400"
                                )}
                            >
                                {req.met && <Check className="w-3 h-3" />}
                            </div>
                            <span className={cn(
                                req.met ? "text-success" : "text-gray-500 dark:text-gray-400"
                            )}>
                                {req.text}
                            </span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
