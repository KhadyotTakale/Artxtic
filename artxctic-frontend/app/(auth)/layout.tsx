"use client";

import { ReactNode } from "react";

interface AuthLayoutProps {
    children: ReactNode;
}

export default function AuthLayout({ children }: AuthLayoutProps) {
    return (
        <div className="min-h-screen flex w-full bg-white">
            {/* Left panel - gradient (hidden on mobile) */}
            <div className="hidden lg:flex lg:w-1/2 p-4 h-screen fixed left-0 top-0 bottom-0">
                <div className="relative w-full h-full rounded-3xl overflow-hidden shadow-2xl">
                    {/* Gradient background */}
                    <div className="absolute inset-0 bg-gradient-to-br from-pink-500 via-purple-600 to-blue-600" />

                    {/* Pattern overlay */}
                    <div className="absolute inset-0 opacity-20">
                        <div className="absolute inset-0" style={{
                            backgroundImage: `linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px),
                 linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px)`,
                            backgroundSize: '40px 40px'
                        }} />
                    </div>

                    {/* Gradient overlays */}
                    <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-transparent to-black/80" />

                    {/* Content */}
                    <div className="relative z-20 flex flex-col justify-between h-full p-12 text-white">
                        <div className="flex items-center space-x-4">
                            <span className="text-xs tracking-[0.2em] font-medium uppercase opacity-80">
                                Creativity Unleashed
                            </span>
                            <div className="h-[1px] w-12 bg-white/50" />
                        </div>

                        <div className="space-y-6 max-w-lg">
                            <h1 className="text-6xl leading-tight font-bold">
                                Create <br />
                                <span className="italic font-light">Amazing</span> <br />
                                Content
                            </h1>
                            <p className="text-white/80 font-light text-lg leading-relaxed max-w-md">
                                Transform your ideas into stunning visuals with the power of AI. Join thousands of creators bringing their imagination to life.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Right panel - WHITE BACKGROUND */}
            <div className="w-full lg:w-1/2 ml-auto flex flex-col min-h-screen bg-white">
                {/* Logo */}
                <div className="w-full p-8 lg:p-12 flex justify-center lg:justify-start">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
                            <span className="material-icons-round text-white text-lg">auto_awesome</span>
                        </div>
                        <span className="text-2xl font-bold text-black">
                            Artxtic
                        </span>
                    </div>
                </div>

                {/* Main content */}
                <div className="flex-grow flex flex-col justify-center items-center px-6 sm:px-12 md:px-24 xl:px-32 pb-20">
                    {children}
                </div>

                {/* Footer */}
                <div className="w-full p-6 text-center lg:text-left">
                    <p className="text-xs text-gray-500">
                        © 2026 Artxtic Inc. All rights reserved.
                    </p>
                </div>
            </div>
        </div>
    );
}
