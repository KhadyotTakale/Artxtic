import { forwardRef, TextareaHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
    label?: string;
    error?: string;
    helperText?: string;
    showCount?: boolean;
    maxCount?: number;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
    ({ className, label, error, helperText, showCount, maxCount, value, ...props }, ref) => {
        const currentLength = typeof value === 'string' ? value.length : 0;

        return (
            <div className="space-y-2 w-full">
                {label && (
                    <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            {label}
                        </label>
                        {showCount && maxCount && (
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                                {currentLength}/{maxCount}
                            </span>
                        )}
                    </div>
                )}
                <textarea
                    className={cn(
                        "flex w-full rounded-lg border bg-white dark:bg-gray-800 px-4 py-3 text-sm text-gray-900 dark:text-white transition-colors",
                        "placeholder:text-gray-500 dark:placeholder:text-gray-400",
                        "focus:outline-none focus:ring-2",
                        error
                            ? "border-red-500 focus:border-red-500 focus:ring-red-500/20"
                            : "border-gray-300 dark:border-gray-600 focus:border-black dark:focus:border-white focus:ring-black/10 dark:focus:ring-white/10",
                        "disabled:cursor-not-allowed disabled:opacity-50",
                        "resize-none",
                        className
                    )}
                    ref={ref}
                    value={value}
                    {...props}
                />
                {error && (
                    <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
                )}
                {helperText && !error && (
                    <p className="text-sm text-gray-500 dark:text-gray-400">{helperText}</p>
                )}
            </div>
        );
    }
);

Textarea.displayName = "Textarea";
