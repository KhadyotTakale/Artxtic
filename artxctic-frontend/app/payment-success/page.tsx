"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { Loader2 } from "lucide-react";

function PaymentSuccessContent() {
    const searchParams = useSearchParams();
    const plan = searchParams.get("plan");

    return (
        <div className="text-center max-w-md mx-auto">
            <div className="w-20 h-20 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                <Check className="w-10 h-10 text-green-600 dark:text-green-400" />
            </div>

            <h1 className="text-3xl font-serif text-gray-900 dark:text-white mb-4">
                Payment Successful!
            </h1>

            <p className="text-gray-600 dark:text-gray-400 mb-8">
                Thank you for your purchase. Your subscription {plan ? `to ${plan} plan` : ""} is now active.
                You can now access all premium features.
            </p>

            <div className="flex flex-col gap-3">
                <Link href="/playground">
                    <Button size="lg" fullWidth>
                        Start Creating
                    </Button>
                </Link>
                <Link href="/profile">
                    <Button variant="outline" fullWidth>
                        View Profile
                    </Button>
                </Link>
            </div>
        </div>
    );
}

export default function PaymentSuccessPage() {
    return (
        <main className="min-h-screen flex items-center justify-center px-4">
            <Suspense fallback={<Loader2 className="w-8 h-8 animate-spin" />}>
                <PaymentSuccessContent />
            </Suspense>
        </main>
    );
}
