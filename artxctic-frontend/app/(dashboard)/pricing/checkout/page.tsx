"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState, Suspense } from "react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { Check, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

function CheckoutContent() {
    const searchParams = useSearchParams();
    const planId = searchParams.get("plan");
    const [status, setStatus] = useState<"loading" | "success" | "error">("loading");

    useEffect(() => {
        if (!planId) {
            setStatus("error");
            return;
        }

        const initiateCheckout = async () => {
            try {
                // In a real app, we might verify the session_id here if redirecting back from Stripe
                // But for now, let's just simulate or show the plan we are buying
                // Actually, if we are HERE, it means we probably just want to show "Confirming..."
                // or if it's a redirect FROM stripe, we check status.

                // Let's assume this page is the "Thank you" page or "Processing" page
                // But wait, the URL is /pricing/checkout?plan=pro
                // Usually this page would immediately redirect to Stripe via API.

                const response = await api.subscription.createCheckout(planId);
                if (response.checkout_url) {
                    window.location.href = response.checkout_url;
                } else {
                    // Mock success for now if no URL
                    setStatus("success");
                    toast.success("Subscription updated successfully!");
                }
            } catch (error) {
                console.error("Checkout processing failed", error);
                setStatus("error");
            }
        };

        initiateCheckout();
    }, [planId]);

    if (status === "loading") {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
                <Loader2 className="w-12 h-12 animate-spin text-gray-900 dark:text-white" />
                <h2 className="text-xl font-medium">Processing your request...</h2>
                <p className="text-gray-500">Please wait while we redirect you to secure checkout.</p>
            </div>
        );
    }

    if (status === "error") {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 text-center">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center text-red-600 mb-4">
                    <span className="material-icons text-3xl">error_outline</span>
                </div>
                <h2 className="text-2xl font-serif text-gray-900 dark:text-white">Something went wrong</h2>
                <p className="text-gray-600 dark:text-gray-400 max-w-md">
                    We couldn't process your request. Please try again or contact support.
                </p>
                <div className="flex gap-4 mt-6">
                    <Link href="/pricing">
                        <Button variant="outline">Back to Pricing</Button>
                    </Link>
                    <Link href="/playground">
                        <Button>Go to Playground</Button>
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 text-center animate-fade-in">
            <div className="w-20 h-20 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center text-green-600 dark:text-green-400 mb-4 shadow-lg border-4 border-white dark:border-gray-800">
                <Check className="w-10 h-10 stroke-[3]" />
            </div>
            <h2 className="text-3xl font-serif text-gray-900 dark:text-white">Subscription Active!</h2>
            <p className="text-gray-600 dark:text-gray-400 max-w-md text-lg">
                Thank you for upgrading. Your account has been successfully updated to the <strong>{planId?.toUpperCase()}</strong> plan.
            </p>
            <div className="flex gap-4 mt-8">
                <Link href="/playground">
                    <Button size="lg" className="px-8">Start Creating</Button>
                </Link>
                <Link href="/profile">
                    <Button variant="outline" size="lg">View Profile</Button>
                </Link>
            </div>
        </div>
    );
}

export default function CheckoutPage() {
    return (
        <main className="relative h-screen overflow-y-auto no-scrollbar pt-12 pb-10 px-6 ml-24 lg:ml-32 w-auto max-w-7xl mx-auto flex flex-col z-10">
            <Suspense fallback={
                <div className="flex justify-center items-center py-20">
                    <Loader2 className="w-8 h-8 animate-spin" />
                </div>
            }>
                <CheckoutContent />
            </Suspense>
        </main>
    );
}
