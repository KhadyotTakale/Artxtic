"use client";

import { ReactNode } from "react";
import { Sidebar } from "@/components/dashboard/sidebar";
import { PlaygroundProvider } from "@/contexts/playground-context";

interface DashboardLayoutProps {
    children: ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
    return (
        <PlaygroundProvider>
            <div className="bg-background-light dark:bg-background-dark text-gray-900 dark:text-gray-100 min-h-screen relative overflow-hidden transition-colors duration-300">
                {/* Grid pattern background */}
                <div className="absolute inset-0 bg-grid-pattern pointer-events-none z-0" />

                {/* Sidebar */}
                <Sidebar userAvatar="https://i.pravatar.cc/150?img=68" />

                {/* Main content */}
                <div className="relative z-10">
                    {children}
                </div>
            </div>
        </PlaygroundProvider>
    );
}
