"use client";

import { useState, useEffect } from "react";
import { Check, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { PricingPlan, PricingFeature } from "@/types";

export default function PricingPage() {
    const [isAnnual, setIsAnnual] = useState(false);
    const [plans, setPlans] = useState<PricingPlan[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadPlans();
    }, []);

    const loadPlans = async () => {
        try {
            const response = await api.subscription.getPlans();
            const rawPlans = response.data || [];

            // Transform backend plan format → frontend PricingPlan format
            const transformed: PricingPlan[] = rawPlans.map((p: any, idx: number) => {
                const featureMap = p.features || {};
                const features: PricingFeature[] = [];

                // Build feature list from limits + features dict
                features.push({ text: `${p.image_limit_monthly === -1 ? 'Unlimited' : p.image_limit_monthly} images/month`, included: true });
                features.push({ text: `${p.video_limit_monthly === -1 ? 'Unlimited' : p.video_limit_monthly} videos/month`, included: true });
                if (featureMap.quality) features.push({ text: `${featureMap.quality.charAt(0).toUpperCase() + featureMap.quality.slice(1)} quality`, included: true });
                features.push({ text: 'No watermark', included: featureMap.watermark === false });
                features.push({ text: 'Priority support', included: !!featureMap.priority_support });
                features.push({ text: 'API access', included: !!featureMap.api_access });

                return {
                    id: p.id,
                    name: p.name,
                    price: p.price_monthly ?? 0,
                    currency: '$',
                    billing: p.price_monthly ? `$${p.price_monthly}/month` : 'Free forever',
                    features,
                    cta: p.price_monthly ? 'Get Started' : 'Current Plan',
                    recommended: p.name === 'Pro',
                };
            });

            setPlans(transformed);
        } catch (error) {
            console.error("Failed to load plans", error);
            toast.error("Failed to load pricing plans");
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubscribe = async (planId: string) => {
        try {
            // If free plan, maybe just upgrade directly or show success
            if (planId === "free") {
                toast.success("You are already on the free plan");
                return;
            }

            const response = await api.subscription.createCheckout(planId);
            if (response.checkout_url) {
                window.location.href = response.checkout_url;
            } else {
                toast.success("Subscription updated!");
            }
        } catch (error) {
            console.error("Checkout failed", error);
            toast.error("Failed to initiate checkout");
        }
    };

    return (
        <main className="relative h-screen overflow-y-auto no-scrollbar pt-12 pb-10 px-6 ml-24 lg:ml-32 w-auto max-w-7xl mx-auto flex flex-col z-10">
            <div className="flex flex-col gap-6 mb-12 animate-fade-in text-center max-w-2xl mx-auto">
                <h1 className="text-3xl md:text-4xl font-serif text-gray-900 dark:text-white">
                    Simple, transparent pricing
                </h1>
                <p className="text-gray-600 dark:text-gray-400">
                    Choose the plan that's right for you. Create stunning AI art without limits.
                </p>

                <div className="flex items-center justify-center gap-4 mt-4">
                    <span className={`text-sm font-medium ${!isAnnual ? 'text-gray-900 dark:text-white' : 'text-gray-500'}`}>
                        Monthly
                    </span>
                    <Switch
                        checked={isAnnual}
                        onCheckedChange={setIsAnnual}
                    />
                    <span className={`text-sm font-medium ${isAnnual ? 'text-gray-900 dark:text-white' : 'text-gray-500'}`}>
                        Yearly <span className="text-green-500 text-xs ml-1 font-bold">SAVE 20%</span>
                    </span>
                </div>
            </div>

            {isLoading ? (
                <div className="flex justify-center py-20">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-white"></div>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pb-20 animate-fade-in">
                    {plans.map((plan) => (
                        <div
                            key={plan.id}
                            className={`relative rounded-2xl p-8 border ${plan.recommended
                                ? 'bg-gray-900 dark:bg-white text-white dark:text-gray-900 border-transparent shadow-xl scale-105 z-10'
                                : 'bg-white dark:bg-white/5 border-gray-200 dark:border-white/10 text-gray-900 dark:text-white'
                                } flex flex-col transition-transform duration-300 hover:-translate-y-1`}
                        >
                            {plan.recommended && (
                                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-gradient-to-r from-orange-500 to-pink-500 rounded-full text-white text-xs font-bold uppercase tracking-wider shadow-lg">
                                    Most Popular
                                </div>
                            )}

                            <div className="mb-6">
                                <h3 className="text-lg font-bold mb-2">{plan.name}</h3>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-4xl font-serif font-bold">
                                        {plan.currency}{isAnnual ? (plan.price * 12 * 0.8).toFixed(0) : plan.price}
                                    </span>
                                    <span className={`text-sm ${plan.recommended ? 'text-gray-300 dark:text-gray-600' : 'text-gray-500'}`}>
                                        /{isAnnual ? 'year' : 'month'}
                                    </span>
                                </div>
                                <p className={`text-sm mt-3 ${plan.recommended ? 'text-gray-300 dark:text-gray-600' : 'text-gray-500'}`}>
                                    {plan.billing}
                                </p>
                            </div>

                            <Button
                                onClick={() => handleSubscribe(plan.id)}
                                variant={plan.recommended ? "secondary" : "primary"}
                                className={`w-full mb-8 ${plan.recommended
                                    ? 'bg-white text-gray-900 hover:bg-gray-100 dark:bg-gray-900 dark:text-white dark:hover:bg-gray-800'
                                    : ''
                                    }`}
                            >
                                {plan.cta}
                            </Button>

                            <div className="space-y-4 flex-grow">
                                {plan.features.map((feature, i) => (
                                    <div key={i} className="flex items-start gap-3 text-sm">
                                        <div className={`mt-0.5 p-0.5 rounded-full ${feature.included
                                            ? 'bg-green-500/20 text-green-500'
                                            : 'bg-gray-200 dark:bg-gray-700 text-gray-400'
                                            }`}>
                                            <Check className="w-3 h-3" />
                                        </div>
                                        <span className={feature.included ? '' : 'text-gray-400 line-through'}>
                                            {feature.text}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </main>
    );
}
