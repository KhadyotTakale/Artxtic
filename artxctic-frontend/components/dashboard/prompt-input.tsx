"use client";

import { useState, FormEvent } from "react";
import { ArrowUp, Mic, ImagePlus, Image, Video } from "lucide-react";
import { usePlayground, MODELS, ASPECT_RATIOS } from "@/contexts/playground-context";
import { Button } from "@/components/ui/button";

interface PromptInputProps {
    onSubmit?: () => void;
}

export function PromptInput({ onSubmit }: PromptInputProps) {
    const { generate, isGenerating, currentModel, currentAspectRatio, mediaType, setCurrentModel, setCurrentAspectRatio, setMediaType } = usePlayground();
    const [prompt, setPrompt] = useState("");
    const [showModelMenu, setShowModelMenu] = useState(false);
    const [showRatioMenu, setShowRatioMenu] = useState(false);


    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (!prompt.trim() || isGenerating) return;

        await generate(prompt);
        setPrompt("");
        onSubmit?.();
    };

    return (
        <div className="fixed bottom-8 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none">
            <form
                onSubmit={handleSubmit}
                className="pointer-events-auto w-full max-w-3xl bg-white dark:bg-black border border-gray-200 dark:border-gray-800 rounded-2xl shadow-2xl overflow-hidden"
            >
                <div className="relative p-3">
                    <textarea
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder="Describe what you want to create..."
                        className="w-full bg-transparent border-0 focus:outline-none focus:ring-0 min-h-[60px] max-h-[120px] resize-none text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-600 text-sm"
                        disabled={isGenerating}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSubmit(e as any);
                            }
                        }}
                    />
                </div>

                <div className="flex items-center justify-between px-3 pb-3 pt-1 border-t border-gray-200 dark:border-gray-800">
                    <div className="flex items-center gap-2">
                        {/* Image/Video Toggle */}
                        <div className="flex items-center bg-gray-100 dark:bg-gray-900 rounded-lg p-1">
                            <button
                                type="button"
                                onClick={() => setMediaType("image")}
                                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${mediaType === "image"
                                    ? "bg-white dark:bg-gray-800 text-gray-900 dark:text-white shadow-sm"
                                    : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
                                    }`}
                                disabled={isGenerating}
                            >
                                <Image className="w-3.5 h-3.5" />
                                Image
                            </button>
                            <button
                                type="button"
                                onClick={() => setMediaType("video")}
                                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${mediaType === "video"
                                    ? "bg-white dark:bg-gray-800 text-gray-900 dark:text-white shadow-sm"
                                    : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
                                    }`}
                                disabled={isGenerating}
                            >
                                <Video className="w-3.5 h-3.5" />
                                Video
                            </button>
                        </div>

                        {/* Model Selector */}
                        <div className="relative">
                            <button
                                type="button"
                                onClick={() => setShowModelMenu(!showModelMenu)}
                                className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-gray-300 dark:hover:border-gray-700 transition-all text-sm"
                                disabled={isGenerating}
                            >
                                <div className="w-4 h-4 bg-gray-900 dark:bg-white rounded flex items-center justify-center text-[10px] font-bold text-white dark:text-black">
                                    {currentModel[0]}
                                </div>
                                <span className="font-medium text-gray-900 dark:text-white">
                                    {currentModel}
                                </span>
                            </button>

                            {showModelMenu && (
                                <div className="absolute bottom-full mb-2 left-0 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg shadow-xl py-1 min-w-[160px]">
                                    {MODELS.map((model) => (
                                        <button
                                            key={model}
                                            type="button"
                                            onClick={() => {
                                                setCurrentModel(model);
                                                setShowModelMenu(false);
                                            }}
                                            className="w-full px-3 py-2 text-left text-sm text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                                        >
                                            {model}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Aspect Ratio Selector */}
                        <div className="relative">
                            <button
                                type="button"
                                onClick={() => setShowRatioMenu(!showRatioMenu)}
                                className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-gray-300 dark:hover:border-gray-700 transition-all text-sm"
                                disabled={isGenerating}
                            >
                                <span className="material-icons-outlined text-base text-gray-600 dark:text-gray-400">
                                    crop_portrait
                                </span>
                                <span className="font-medium text-gray-900 dark:text-white">
                                    {currentAspectRatio}
                                </span>
                            </button>

                            {showRatioMenu && (
                                <div className="absolute bottom-full mb-2 left-0 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg shadow-xl py-1 min-w-[100px]">
                                    {ASPECT_RATIOS.map((ratio) => (
                                        <button
                                            key={ratio}
                                            type="button"
                                            onClick={() => {
                                                setCurrentAspectRatio(ratio);
                                                setShowRatioMenu(false);
                                            }}
                                            className="w-full px-3 py-2 text-left text-sm text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                                        >
                                            {ratio}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <button
                            type="button"
                            className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-900 transition-colors"
                            disabled={isGenerating}
                        >
                            <ImagePlus className="w-5 h-5" />
                        </button>

                        <button
                            type="button"
                            className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-900 transition-colors"
                            disabled={isGenerating}
                        >
                            <Mic className="w-5 h-5" />
                        </button>

                        <Button
                            type="submit"
                            variant="primary"
                            size="sm"
                            className="w-10 h-10 rounded-full p-0"
                            disabled={!prompt.trim() || isGenerating}
                            loading={isGenerating}
                        >
                            {!isGenerating && <ArrowUp className="w-5 h-5" />}
                        </Button>
                    </div>
                </div>
            </form>
        </div>
    );
}
