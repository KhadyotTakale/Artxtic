"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { XCircle } from "lucide-react";

export default function PaymentFailurePage() {
    const router = useRouter();

    return (
        <div className="min-h-screen bg-white dark:bg-background-dark flex items-center justify-center px-4">
            <div className="max-w-md w-full text-center">
                <div className="mb-8">
                    <div className="w-24 h-24 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mx-auto">
                        <XCircle className="w-12 h-12 text-red-600 dark:text-red-400" />
                    </div>
                </div>

                <h1 className="text-4xl font-serif text-black dark:text-white mb-4">
                    Payment Failed
                </h1>

                <p className="text-lg text-gray-600 dark:text-gray-400 mb-8">
                    We couldn't process your payment. Please check your card details and try again.
                </p>

                <div className="bg-red-50 dark:bg-red-900/10 rounded-xl p-6 mb-8 border border-red-200 dark:border-red-900/20">
                    <h3 className="font-semibold text-black dark:text-white mb-2">
                        Common issues:
                    </h3>
                    <ul className="text-left text-sm text-gray-700 dark:text-gray-300 space-y-2">
                        <li>• Insufficient funds</li>
                        <li>• Incorrect card details</li>
                        <li>• Card expired</li>
                        <li>• Payment declined by bank</li>
                    </ul>
                </div>

                <div className="space-y-4">
                    <Button
                        variant="primary"
                        size="lg"
                        fullWidth
                        onClick={() => router.back()}
                    >
                        Try Again
                    </Button>

                    <Button
                        variant="outline"
                        size="lg"
                        fullWidth
                        onClick={() => router.push("/pricing")}
                    >
                        View Pricing
                    </Button>

                    <Button
                        variant="ghost"
                        size="lg"
                        fullWidth
                        onClick={() => router.push("/playground")}
                    >
                        Continue with Free Plan
                    </Button>
                </div>

                <p className="text-xs text-gray-500 dark:text-gray-400 mt-8">
                    Need help? Contact our support team at support@artxtic.com
                </p>
            </div>
        </div>
    );
}
