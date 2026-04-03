"use client";

import { useState, useRef, KeyboardEvent, ClipboardEvent, ChangeEvent } from "react";
import { cn } from "@/lib/utils";
import { OTP_LENGTH } from "@/lib/constants";

interface OTPInputProps {
    value: string[];
    onChange: (value: string[]) => void;
    error?: boolean;
    disabled?: boolean;
}

export function OTPInput({ value, onChange, error, disabled }: OTPInputProps) {
    const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

    const handleChange = (index: number, inputValue: string) => {
        if (disabled) return;

        // Only allow numbers
        const numericValue = inputValue.replace(/[^0-9]/g, "");

        if (numericValue.length > 1) {
            // If multiple digits pasted, take only the first one
            const newValue = [...value];
            newValue[index] = numericValue[0];
            onChange(newValue);

            // Move to next input
            if (index < OTP_LENGTH - 1) {
                inputRefs.current[index + 1]?.focus();
            }
            return;
        }

        const newValue = [...value];
        newValue[index] = numericValue;
        onChange(newValue);

        // Auto-advance to next input
        if (numericValue && index < OTP_LENGTH - 1) {
            inputRefs.current[index + 1]?.focus();
        }
    };

    const handleKeyDown = (index: number, e: KeyboardEvent<HTMLInputElement>) => {
        if (disabled) return;

        if (e.key === "Backspace" && !value[index] && index > 0) {
            // Move to previous input on backspace if current is empty
            inputRefs.current[index - 1]?.focus();
        } else if (e.key === "ArrowLeft" && index > 0) {
            inputRefs.current[index - 1]?.focus();
        } else if (e.key === "ArrowRight" && index < OTP_LENGTH - 1) {
            inputRefs.current[index + 1]?.focus();
        }
    };

    const handlePaste = (e: ClipboardEvent<HTMLInputElement>) => {
        if (disabled) return;

        e.preventDefault();
        const pastedData = e.clipboardData.getData("text/plain").replace(/[^0-9]/g, "");

        if (pastedData.length === OTP_LENGTH) {
            const newValue = pastedData.split("");
            onChange(newValue);
            // Focus last input
            inputRefs.current[OTP_LENGTH - 1]?.focus();
        }
    };

    return (
        <div className="flex justify-center gap-2 sm:gap-4">
            {Array.from({ length: OTP_LENGTH }).map((_, index) => (
                <input
                    key={index}
                    ref={(el) => {
                        inputRefs.current[index] = el;
                    }}
                    type="text"
                    inputMode="numeric"
                    maxLength={1}
                    value={value[index] || ""}
                    onChange={(e) => handleChange(index, e.target.value)}
                    onKeyDown={(e) => handleKeyDown(index, e)}
                    onPaste={handlePaste}
                    disabled={disabled}
                    autoFocus={index === 0}
                    className={cn(
                        "w-12 h-12 sm:w-14 sm:h-14 text-center text-xl font-semibold",
                        "bg-bg-light-secondary dark:bg-surface-dark",
                        "border-2 border-transparent rounded-lg",
                        "focus:border-primary focus:outline-none focus:ring-0",
                        "transition-all duration-200",
                        "disabled:opacity-50 disabled:cursor-not-allowed",
                        error && "border-error animate-shake"
                    )}
                />
            ))}
        </div>
    );
}
