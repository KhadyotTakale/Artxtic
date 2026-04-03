"use client";

import { useState, useEffect, useCallback } from "react";
import { Download, Star } from "lucide-react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { Generation } from "@/types";

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

/** Relative time formatter with safe fallback */
function formatTime(dateString: string | Date | null | undefined): string {
    if (!dateString) return "Unknown";
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return "Unknown";
    const now = new Date();
    const diff = Math.floor((now.getTime() - date.getTime()) / 1000 / 60);

    if (diff < 1) return "Just now";
    if (diff < 60) return `${diff} min${diff > 1 ? "s" : ""} ago`;
    if (diff < 1440) return `${Math.floor(diff / 60)} hour${Math.floor(diff / 60) > 1 ? "s" : ""} ago`;
    return formatDate(dateString as string);
}

/** Media card for library grid — handles both images and videos */
function LibraryMediaCard({
    item,
    onToggleStar,
    onDownload,
}: {
    item: Generation;
    onToggleStar: (id: string) => void;
    onDownload: (url: string, type: string) => void;
}) {
    const [isLoading, setIsLoading] = useState(true);
    const [hasError, setHasError] = useState(false);
    const isVideo = item.type === "video";

    return (
        <div className="group relative aspect-square rounded-2xl overflow-hidden bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/5 hover:border-gray-300 dark:hover:border-white/20 transition-all cursor-pointer shadow-sm">
            {/* Video badge */}
            {isVideo && (
                <div className="absolute top-2 left-2 z-10 bg-black/60 backdrop-blur-sm text-white text-[10px] font-medium px-2 py-0.5 rounded-full flex items-center gap-1">
                    <span className="text-[8px]">▶</span>
                    Video
                </div>
            )}

            {/* Loading spinner */}
            {isLoading && !hasError && (
                <div className="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-gray-800/50 z-[1]">
                    <div className="animate-spin rounded-full h-6 w-6 border-2 border-gray-300 dark:border-white/30 border-t-gray-600 dark:border-t-white" />
                </div>
            )}

            {/* Error state */}
            {hasError && (
                <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-100 dark:bg-gray-800/50 text-gray-400 z-[1]">
                    <span className="text-3xl mb-2">{isVideo ? "🎥" : "🖼️"}</span>
                    <span className="text-xs">Failed to load</span>
                </div>
            )}

            {/* Media element */}
            {!hasError && (
                isVideo ? (
                    <video
                        src={item.url}
                        className={`w-full h-full object-cover transition-all duration-700 group-hover:scale-105 ${isLoading ? "opacity-0" : "opacity-100"}`}
                        autoPlay
                        muted
                        loop
                        playsInline
                        poster={item.thumbnailUrl || undefined}
                        onLoadedData={() => setIsLoading(false)}
                        onError={() => {
                            setIsLoading(false);
                            setHasError(true);
                            console.error("Video failed to load:", item.url);
                        }}
                    />
                ) : (
                    <img
                        alt={item.prompt || "Generated Media"}
                        className={`w-full h-full object-cover transition-all duration-700 group-hover:scale-105 ${isLoading ? "opacity-0" : "opacity-100"}`}
                        src={item.url}
                        onLoad={() => setIsLoading(false)}
                        onError={() => {
                            setIsLoading(false);
                            setHasError(true);
                            console.error("Image failed to load:", item.url);
                        }}
                    />
                )
            )}

            {/* Hover overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-between p-4 z-[2]">
                {/* Top actions */}
                <div className="flex items-center justify-end gap-2">
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onToggleStar(item.id);
                        }}
                        className="p-2 bg-white/10 backdrop-blur-md rounded-lg hover:bg-white/20 transition-colors"
                    >
                        <Star
                            className={`w-4 h-4 ${item.starred ? 'fill-yellow-400 text-yellow-400' : 'text-white'}`}
                        />
                    </button>
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onDownload(item.url, item.type);
                        }}
                        className="p-2 bg-white/10 backdrop-blur-md rounded-lg hover:bg-white/20 transition-colors"
                    >
                        <Download className="w-4 h-4 text-white" />
                    </button>
                </div>

                {/* Bottom info */}
                <div className="flex items-center justify-between w-full">
                    <div className="flex items-center gap-1.5 bg-white/10 backdrop-blur-md px-2.5 py-1 rounded-lg text-[10px] font-medium text-white border border-white/10">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.5)]" />
                        {item.model}
                    </div>
                    <span className="text-[10px] font-medium text-gray-300">{formatTime(item.createdAt)}</span>
                </div>
            </div>
        </div>
    );
}

export default function LibraryPage() {
    const [activeTab, setActiveTab] = useState<"history" | "starred">("history");
    const [media, setMedia] = useState<Generation[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const loadMedia = useCallback(async () => {
        setIsLoading(true);
        try {
            const response = activeTab === "history"
                ? await api.library.getHistory()
                : await api.library.getStarred();

            setMedia(response.data ?? []);
        } catch (error) {
            console.error("Failed to load library", error);
            toast.error("Failed to load library");
        } finally {
            setIsLoading(false);
        }
    }, [activeTab]);

    useEffect(() => {
        loadMedia();
    }, [loadMedia]);

    const toggleStar = async (id: string) => {
        try {
            const response = await api.library.toggleStar(id);
            setMedia(media.map(item =>
                item.id === id ? { ...item, starred: response.starred } : item
            ));

            // If in starred tab and unstarred, remove it
            if (activeTab === "starred" && !response.starred) {
                setMedia(prev => prev.filter(item => item.id !== id));
            }
        } catch (error) {
            console.error("Failed to toggle star", error);
            toast.error("Failed to update star");
        }
    };

    const downloadMedia = (url: string, type: string) => {
        const extension = type === "video" ? "mp4" : "jpg";
        const link = document.createElement('a');
        link.href = url;
        link.target = "_blank";
        link.download = `artxtic-${Date.now()}.${extension}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <main className="relative h-screen overflow-y-auto no-scrollbar pt-12 pb-10 px-6 ml-24 lg:ml-32 w-auto max-w-7xl mx-auto flex flex-col z-10">
            <div className="flex flex-col gap-6 mb-8 animate-fade-in">
                <div className="flex items-center justify-between border-b border-gray-200 dark:border-white/10">
                    <div className="flex gap-8">
                        <button
                            className={`pb-3 border-b-2 text-sm font-medium transition-colors ${activeTab === "history"
                                ? "border-gray-900 dark:border-white text-gray-900 dark:text-white"
                                : "border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white"
                                }`}
                            onClick={() => setActiveTab("history")}
                        >
                            History
                        </button>
                        <button
                            className={`pb-3 border-b-2 text-sm font-medium transition-colors ${activeTab === "starred"
                                ? "border-gray-900 dark:border-white text-gray-900 dark:text-white"
                                : "border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white"
                                }`}
                            onClick={() => setActiveTab("starred")}
                        >
                            Starred
                        </button>
                    </div>
                </div>

                <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-orange-500/5 border border-orange-500/10 text-orange-600 dark:text-orange-400 text-xs w-fit">
                    <span className="material-icons-outlined text-sm">info</span>
                    <span className="font-medium">Items older than 15 days are automatically removed</span>
                </div>
            </div>

            {isLoading ? (
                <div className="flex justify-center py-20">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-white"></div>
                </div>
            ) : media.length === 0 ? (
                <div className="flex-grow flex items-center justify-center">
                    <div className="text-center space-y-4">
                        <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mx-auto">
                            <Star className="w-8 h-8 text-gray-400" />
                        </div>
                        <h3 className="text-xl font-serif text-gray-900 dark:text-white">No {activeTab} items</h3>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                            {activeTab === "starred"
                                ? "Star your favorite generations to see them here"
                                : "Your generation history will appear here"}
                        </p>
                    </div>
                </div>
            ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5 pb-20 animate-fade-in">
                    {media.map((item) => (
                        <LibraryMediaCard
                            key={item.id}
                            item={item}
                            onToggleStar={toggleStar}
                            onDownload={downloadMedia}
                        />
                    ))}
                </div>
            )}
        </main>
    );
}
