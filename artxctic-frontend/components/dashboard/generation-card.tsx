"use client";

import { useState } from "react";
import { Generation } from "@/types";
import { Download, Star } from "lucide-react";
import { Button } from "@/components/ui/button";

interface GenerationCardProps {
    generation: Generation;
    type?: "user" | "ai";
}

export function GenerationCard({ generation, type = "user" }: GenerationCardProps) {
    const [isLoading, setIsLoading] = useState(true);
    const [hasError, setHasError] = useState(false);

    const aspectRatioClass = {
        "1:1": "aspect-square",
        "16:9": "aspect-video",
        "9:16": "aspect-[9/16]",
        "4:3": "aspect-[4/3]",
        "3:4": "aspect-[3/4]",
    }[generation.aspectRatio] || "aspect-square";

    const isVideo = generation.type === "video";

    return (
        <div className="group relative rounded-xl overflow-hidden bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-white/10">
            <div className={`${aspectRatioClass} relative`}>
                {/* Video badge */}
                {isVideo && (
                    <div className="absolute top-2 left-2 z-10 bg-black/60 backdrop-blur-sm text-white text-[10px] font-medium px-2 py-0.5 rounded-full flex items-center gap-1">
                        <span className="text-[8px]">▶</span>
                        Video
                    </div>
                )}

                {/* Loading spinner */}
                {isLoading && generation.url && (
                    <div className="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-gray-800 z-[1]">
                        <div className="animate-spin rounded-full h-6 w-6 border-2 border-gray-300 dark:border-white/30 border-t-gray-600 dark:border-t-white" />
                    </div>
                )}

                {/* Error state */}
                {hasError && (
                    <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-100 dark:bg-gray-800 text-gray-400 z-[1]">
                        <span className="text-2xl mb-1">{isVideo ? "🎥" : "🖼️"}</span>
                        <span className="text-[10px]">Failed to load</span>
                    </div>
                )}

                {/* Media element */}
                {generation.url && !hasError ? (
                    isVideo ? (
                        <video
                            src={generation.url}
                            className={`w-full h-full object-cover transition-opacity duration-300 ${isLoading ? "opacity-0" : "opacity-100"}`}
                            autoPlay
                            muted
                            loop
                            playsInline
                            poster={generation.thumbnailUrl || undefined}
                            onLoadedData={() => setIsLoading(false)}
                            onError={() => {
                                setIsLoading(false);
                                setHasError(true);
                                console.error("Video failed to load:", generation.url);
                            }}
                        />
                    ) : (
                        <img
                            src={generation.url}
                            alt={generation.prompt}
                            className={`w-full h-full object-cover transition-opacity duration-300 ${isLoading ? "opacity-0" : "opacity-100"}`}
                            onLoad={() => setIsLoading(false)}
                            onError={() => {
                                setIsLoading(false);
                                setHasError(true);
                                console.error("Image failed to load:", generation.url);
                            }}
                        />
                    )
                ) : !hasError ? (
                    <div className="w-full h-full flex items-center justify-center text-gray-400">
                        Pending...
                    </div>
                ) : null}

                {/* Hover overlay */}
                <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2 z-[2]">
                    <Button size="sm" variant="secondary" className="h-8 w-8 p-0 rounded-full">
                        <Download className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="secondary" className="h-8 w-8 p-0 rounded-full">
                        <Star className={`h-4 w-4 ${generation.starred ? "fill-yellow-400 text-yellow-400" : ""}`} />
                    </Button>
                </div>
            </div>
            <div className="p-3">
                <p className="text-sm font-medium truncate">{generation.prompt}</p>
                <p className="text-xs text-gray-500 mt-1">{formatDate(generation.createdAt)}</p>
            </div>
        </div>
    );
}

/** Safe date formatter — never shows "Invalid Date" */
function formatDate(dateStr: string | null | undefined): string {
    if (!dateStr) return "Unknown date";
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return "Unknown date";
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
    });
}
