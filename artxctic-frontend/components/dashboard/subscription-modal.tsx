"use client";

import { useState } from "react";
import { useAuth } from "@/contexts/auth-context";
import { Button } from "@/components/ui/button";
import { X, Check, CreditCard, Calendar } from "lucide-react";

interface SubscriptionModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export function SubscriptionModal({ isOpen, onClose }: SubscriptionModalProps) {
    const { user } = useAuth();
    const [isChangingPlan, setIsChangingPlan] = useState(false);
    const [isCanceling, setIsCanceling] = useState(false);

    if (!isOpen) return null;

    const currentPlan = user?.plan || "free";
    const nextBillingDate = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toLocaleDateString();

    const handleChangePlan = () => {
        setIsChangingPlan(true);
        setTimeout(() => {
            window.location.href = "/pricing";
        }, 500);
    };

    const handleCancelSubscription = async () => {
        if (!confirm("Are you sure you want to cancel your subscription? You'll lose access to Pro features at the end of your billing period.")) {
            return;
        }

        setIsCanceling(true);
        await new Promise(resolve => setTimeout(resolve, 1000));
        setIsCanceling(false);
        alert("Subscription canceled. You'll have access until " + nextBillingDate);
    };

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-200 shadow-2xl">
                {/* Header */}
                <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex items-center justify-between rounded-t-2xl">
                    <h2 className="text-2xl font-bold text-black">
                        Manage Subscription
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <X className="w-5 h-5 text-gray-500" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 space-y-6">
                    {/* Current Plan */}
                    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 text-white">
                        <div className="flex items-start justify-between mb-4">
                            <div>
                                <h3 className="text-lg font-semibold mb-1">
                                    Current Plan
                                </h3>
                                <p className="text-sm text-gray-300">
                                    {currentPlan === "pro" ? "Pro Plan" : currentPlan === "enterprise" ? "Enterprise Plan" : "Free Plan"}
                                </p>
                            </div>
                            <div className="px-3 py-1 bg-green-500 text-white rounded-full text-xs font-semibold">
                                Active
                            </div>
                        </div>

                        <div className="space-y-3">
                            <div className="flex items-center gap-3 text-sm">
                                <CreditCard className="w-4 h-4 text-gray-400" />
                                <span className="text-gray-200">
                                    {currentPlan === "free" ? "No payment method" : "•••• •••• •••• 4242"}
                                </span>
                            </div>

                            {currentPlan !== "free" && (
                                <div className="flex items-center gap-3 text-sm">
                                    <Calendar className="w-4 h-4 text-gray-400" />
                                    <span className="text-gray-200">
                                        Next billing: {nextBillingDate}
                                    </span>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Features */}
                    <div>
                        <h3 className="font-semibold text-black mb-4">
                            Your Features
                        </h3>
                        <div className="space-y-2">
                            {currentPlan === "free" ? (
                                <>
                                    <div className="flex items-center gap-3">
                                        <Check className="w-5 h-5 text-green-600" />
                                        <span className="text-sm text-gray-700">10 generations per month</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <Check className="w-5 h-5 text-green-600" />
                                        <span className="text-sm text-gray-700">Standard quality</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <X className="w-5 h-5 text-gray-400" />
                                        <span className="text-sm text-gray-500">Watermarked outputs</span>
                                    </div>
                                </>
                            ) : (
                                <>
                                    <div className="flex items-center gap-3">
                                        <Check className="w-5 h-5 text-green-600" />
                                        <span className="text-sm text-gray-700">Unlimited generations</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <Check className="w-5 h-5 text-green-600" />
                                        <span className="text-sm text-gray-700">HD & 4K quality</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <Check className="w-5 h-5 text-green-600" />
                                        <span className="text-sm text-gray-700">All premium models</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <Check className="w-5 h-5 text-green-600" />
                                        <span className="text-sm text-gray-700">No watermarks</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <Check className="w-5 h-5 text-green-600" />
                                        <span className="text-sm text-gray-700">Commercial license</span>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="space-y-3 pt-4 border-t border-gray-200">
                        <Button
                            variant="primary"
                            size="lg"
                            fullWidth
                            onClick={handleChangePlan}
                            loading={isChangingPlan}
                        >
                            {currentPlan === "free" ? "Upgrade Plan" : "Change Plan"}
                        </Button>

                        {currentPlan !== "free" && (
                            <Button
                                variant="outline"
                                size="lg"
                                fullWidth
                                onClick={handleCancelSubscription}
                                loading={isCanceling}
                            >
                                Cancel Subscription
                            </Button>
                        )}
                    </div>

                    {currentPlan !== "free" && (
                        <p className="text-xs text-gray-500 text-center">
                            You can cancel anytime. Your subscription will remain active until the end of your billing period.
                        </p>
                    )}
                </div>
            </div>
        </div>
    );
}
