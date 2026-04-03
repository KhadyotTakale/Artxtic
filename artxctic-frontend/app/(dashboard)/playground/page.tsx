"use client";

import Link from "next/link";
import { usePlayground } from "@/contexts/playground-context";
import { GenerationCard } from "@/components/dashboard/generation-card";
import { PromptInput } from "@/components/dashboard/prompt-input";
import { Spinner } from "@/components/ui/spinner";

export default function PlaygroundPage() {
    const { generations, isGenerating } = usePlayground();

    return (
        <>
            {/* Top header */}
            <header className="fixed top-6 left-24 right-6 lg:left-32 lg:right-10 flex flex-wrap items-center justify-between gap-4 z-40 pointer-events-none">
                <Link href="/playground" className="pointer-events-auto">
                    <div className="bg-surface-light dark:bg-surface-dark backdrop-blur-md border border-border-light dark:border-white/10 rounded-full pl-2 pr-6 py-2 flex items-center gap-3 shadow-lg cursor-pointer hover:border-gray-300 dark:hover:border-white/20 transition-colors">
                        <div className="h-8 w-8 rounded-full bg-gradient-to-br from-gray-200 to-gray-400 dark:from-gray-700 dark:to-gray-900 flex items-center justify-center border border-white/10">
                            <span className="material-icons-round text-sm text-gray-700 dark:text-gray-300">donut_large</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                            <span className="font-semibold text-gray-900 dark:text-white">Artxtic</span>
                            <span className="text-gray-400 dark:text-gray-600">/</span>
                            <span className="text-gray-600 dark:text-gray-300">My Playground</span>
                        </div>
                    </div>
                </Link>

                <div className="pointer-events-auto flex items-center gap-3">
                    <Link href="/pricing">
                        <button className="flex items-center gap-2 px-4 py-2 rounded-full border border-gray-300 dark:border-white/20 text-sm font-medium hover:bg-gray-100 dark:hover:bg-white/5 transition-colors bg-surface-light dark:bg-surface-dark backdrop-blur-md shadow-lg text-gray-800 dark:text-gray-200">
                            <span className="material-icons-round text-base">verified</span>
                            Upgrade Pro
                        </button>
                    </Link>
                    <button className="flex items-center gap-2 px-4 py-2 rounded-full border border-gray-300 dark:border-white/20 text-sm font-medium hover:bg-gray-100 dark:hover:bg-white/5 transition-colors bg-surface-light dark:bg-surface-dark backdrop-blur-md shadow-lg text-gray-800 dark:text-gray-200">
                        <span className="material-icons-outlined text-base">ios_share</span>
                        Share
                    </button>
                </div>
            </header>

            {/* Main generation area */}
            <main className="relative h-screen overflow-y-auto no-scrollbar pt-28 pb-40 px-4 w-full max-w-7xl mx-auto z-10">
                {generations.length === 0 && !isGenerating ? (
                    <div className="h-full flex flex-col items-center justify-center">
                        <div className="text-center space-y-4 max-w-md">
                            <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mx-auto">
                                <span className="material-icons-round text-3xl text-white">auto_awesome</span>
                            </div>
                            <h3 className="text-2xl font-serif text-gray-900 dark:text-white">Start Creating</h3>
                            <p className="text-gray-600 dark:text-gray-400">
                                Describe what you want to create and let AI bring your vision to life
                            </p>
                        </div>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 pb-8">
                        {/* Show loading skeleton/spinner as first item if generating */}
                        {isGenerating && (
                            <div className="aspect-square rounded-xl bg-gray-100 dark:bg-gray-800 animate-pulse flex flex-col items-center justify-center border border-gray-200 dark:border-white/10 p-4 text-center">
                                <Spinner size="lg" className="mb-4" />
                                <p className="text-sm text-gray-500">Creating masterpiece...</p>
                            </div>
                        )}

                        {generations.map((generation) => (
                            <GenerationCard key={generation.id} generation={generation} />
                        ))}
                    </div>
                )}
            </main>

            {/* Bottom prompt input */}
            <PromptInput />
        </>
    );
}
