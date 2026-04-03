"use client";

import { useState, FormEvent, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "@/contexts/auth-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { SubscriptionModal } from "@/components/dashboard/subscription-modal";
import { Camera } from "lucide-react";
import { api } from "@/lib/api";
import { toast } from "sonner";

export default function ProfilePage() {
    const { user, logout } = useAuth();
    const [showSubscriptionModal, setShowSubscriptionModal] = useState(false);
    const [formData, setFormData] = useState({
        displayName: "",
        email: "",
        instructions: "",
    });
    const [hasChanges, setHasChanges] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadProfile();
    }, []);

    const loadProfile = async () => {
        try {
            const response = await api.user.getProfile();
            const userData = response.data ?? response as any;
            setFormData({
                displayName: userData?.name || "",
                email: userData?.email || "",
                instructions: userData?.customInstructions || userData?.custom_instructions || "",
            });
        } catch (error) {
            console.error("Failed to load profile", error);
            // Fallback to context user if API fails?
            if (user) {
                setFormData({
                    displayName: user.name || "",
                    email: user.email || "",
                    instructions: user.customInstructions || "",
                });
            }
        } finally {
            setIsLoading(false);
        }
    };

    const handleChange = (field: string, value: string) => {
        setFormData(prev => ({ ...prev, [field]: value }));
        setHasChanges(true);
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setIsSaving(true);

        try {
            await api.user.updateProfile({
                name: formData.displayName,
                customInstructions: formData.instructions,
            });
            toast.success("Profile updated successfully");
            setHasChanges(false);
        } catch (error) {
            console.error("Failed to update profile", error);
            toast.error("Failed to update profile");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <main className="relative min-h-screen py-16 px-4 ml-24 lg:ml-32 w-auto max-w-4xl mx-auto z-10 flex flex-col justify-center">
            <div className="mb-12">
                <h1 className="text-4xl lg:text-5xl font-serif text-gray-900 dark:text-white mb-3">User Profile</h1>
                <p className="text-gray-500 dark:text-gray-400 text-sm font-light">
                    Manage your personal information and subscription settings.
                </p>
            </div>

            <form onSubmit={handleSubmit} className="flex flex-col lg:flex-row gap-12 items-start">
                {/* Avatar section */}
                <div className="flex flex-col items-center gap-4 lg:w-48 flex-shrink-0">
                    <div className="group relative w-32 h-32 rounded-full overflow-hidden border border-gray-200 dark:border-white/10 shadow-lg cursor-pointer">
                        <img
                            alt="User"
                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                            src={user?.avatar || "https://i.pravatar.cc/150?img=68"}
                        />
                        <div className="absolute inset-0 bg-black/60 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                            <div className="text-center">
                                <Camera className="w-6 h-6 text-white mx-auto mb-1" />
                                <span className="text-xs text-white font-medium">Change</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Form section */}
                <div className="flex-grow w-full space-y-8">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <Input
                            label="Display Name"
                            type="text"
                            value={formData.displayName}
                            onChange={(e) => handleChange("displayName", e.target.value)}
                        />

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                Email Address
                            </label>
                            <div className="relative">
                                <input
                                    className="w-full h-11 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-800 px-4 py-2 text-sm text-gray-500 cursor-not-allowed"
                                    disabled
                                    type="email"
                                    value={formData.email}
                                />
                                <span className="material-icons-outlined absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 text-sm">
                                    lock
                                </span>
                            </div>
                        </div>
                    </div>

                    <Textarea
                        label="Global Prompt Instructions"
                        value={formData.instructions}
                        onChange={(e) => handleChange("instructions", e.target.value)}
                        placeholder="Enter instructions that apply to all your generations (e.g., 'Always use cinematic lighting' or 'Avoid text in images')..."
                        className="min-h-[160px]"
                        showCount
                        maxCount={500}
                        maxLength={500}
                    />

                    {/* Subscription card */}
                    <div className="bg-surface-light/50 dark:bg-surface-dark/50 border border-gray-200 dark:border-white/10 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-6 relative overflow-hidden group">
                        <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />
                        <div className="flex items-center gap-4 relative z-10">
                            <div className="w-12 h-12 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-black flex items-center justify-center shadow-lg">
                                <span className="material-icons-round text-2xl">auto_awesome</span>
                            </div>
                            <div>
                                <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
                                    Current Plan: <span className="bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent">
                                        {user?.plan === "pro" ? "Pro" : "Free"}
                                    </span>
                                </h3>
                                <p className="text-xs text-gray-500 mt-1">Renews on Jan 25, 2026</p>
                            </div>
                        </div>
                        <button
                            type="button"
                            onClick={() => setShowSubscriptionModal(true)}
                            className="w-full sm:w-auto px-5 py-2.5 text-xs font-medium border border-gray-300 dark:border-white/20 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5 transition-colors text-gray-700 dark:text-white relative z-10"
                        >
                            Manage Subscription
                        </button>
                    </div>

                    {/* Actions */}
                    <div className="pt-8 flex flex-col items-center gap-6">
                        <Button
                            type="submit"
                            variant="primary"
                            size="lg"
                            className="w-full max-w-xs"
                            disabled={!hasChanges}
                            loading={isSaving}
                        >
                            Save Changes
                        </Button>

                        <button
                            type="button"
                            onClick={logout}
                            className="text-xs text-gray-400 hover:text-red-500 transition-colors flex items-center gap-1 group"
                        >
                            <span className="material-icons-outlined text-sm group-hover:-translate-x-0.5 transition-transform">
                                logout
                            </span>
                            Log out
                        </button>
                    </div>
                </div>
            </form>

            {/* Subscription Modal */}
            <SubscriptionModal
                isOpen={showSubscriptionModal}
                onClose={() => setShowSubscriptionModal(false)}
            />
        </main>
    );
}
