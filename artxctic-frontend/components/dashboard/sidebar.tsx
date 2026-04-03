"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { SubscriptionModal } from "./subscription-modal";

interface SidebarProps {
    userAvatar?: string;
}

export function Sidebar({ userAvatar }: SidebarProps) {
    const pathname = usePathname();
    const [showSubscriptionModal, setShowSubscriptionModal] = useState(false);

    const navItems = [
        {
            icon: "home",
            label: "Playground",
            href: "/playground",
            action: null,
        },
        {
            icon: "folder",
            label: "Library",
            href: "/library",
            action: null,
        },
        {
            icon: "person",
            label: "Profile",
            href: "/profile",
            action: null,
        },
        {
            icon: "settings",
            label: "Subscription",
            href: null,
            action: () => setShowSubscriptionModal(true),
        },
    ];

    return (
        <>
            <aside className="fixed left-4 top-4 bottom-4 z-50 flex flex-col items-center">
                <nav className="bg-surface-light dark:bg-surface-dark backdrop-blur-xl border border-border-light dark:border-white/10 rounded-3xl p-3 flex flex-col items-center gap-2 shadow-2xl">
                    {navItems.map((item) => {
                        const isActive = item.href ? pathname === item.href : false;

                        if (item.action) {
                            return (
                                <button
                                    key={item.label}
                                    onClick={item.action}
                                    className={`group relative w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${isActive
                                            ? "bg-gray-900 dark:bg-white text-white dark:text-black shadow-lg"
                                            : "text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white"
                                        }`}
                                    title={item.label}
                                >
                                    <span className="material-icons-outlined text-xl">{item.icon}</span>
                                </button>
                            );
                        }

                        return (
                            <Link
                                key={item.label}
                                href={item.href!}
                                className={`group relative w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${isActive
                                        ? "bg-gray-900 dark:bg-white text-white dark:text-black shadow-lg"
                                        : "text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white"
                                    }`}
                                title={item.label}
                            >
                                <span className="material-icons-outlined text-xl">{item.icon}</span>
                            </Link>
                        );
                    })}

                    {/* User Avatar at bottom */}
                    <div className="mt-4 pt-4 border-t border-gray-200 dark:border-white/10">
                        <Link href="/profile">
                            <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-gray-200 dark:border-white/10 hover:border-gray-400 dark:hover:border-white/30 transition-colors cursor-pointer">
                                <img
                                    src={userAvatar || "https://i.pravatar.cc/150?img=68"}
                                    alt="User"
                                    className="w-full h-full object-cover"
                                />
                            </div>
                        </Link>
                    </div>
                </nav>
            </aside>

            {/* Subscription Modal */}
            <SubscriptionModal
                isOpen={showSubscriptionModal}
                onClose={() => setShowSubscriptionModal(false)}
            />
        </>
    );
}
