"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { Generation, GenerationResponse } from "@/types";

interface PlaygroundContextType {
    generations: Generation[];
    isGenerating: boolean;
    currentModel: string;
    currentAspectRatio: string;
    mediaType: "image" | "video";
    setCurrentModel: (model: string) => void;
    setCurrentAspectRatio: (ratio: string) => void;
    setMediaType: (type: "image" | "video") => void;
    generate: (prompt: string) => Promise<void>;
    likeGeneration: (id: string) => void;
    downloadImage: (url: string) => void;
}

const PlaygroundContext = createContext<PlaygroundContextType | undefined>(undefined);

const MODELS = ["Nano Banana", "Flux Pro", "DALL-E 3", "Midjourney"];
const ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3"];

export function PlaygroundProvider({ children }: { children: ReactNode }) {
    const [generations, setGenerations] = useState<Generation[]>([]);
    const [isGenerating, setIsGenerating] = useState(false);
    const [currentModel, setCurrentModel] = useState(MODELS[0]);
    const [currentAspectRatio, setCurrentAspectRatio] = useState(ASPECT_RATIOS[2]);
    const [mediaType, setMediaType] = useState<"image" | "video">("image");

    // History is no longer loaded on mount - Playground starts clean per user request
    // useEffect(() => {
    //     loadHistory();
    // }, []);

    const pollGenerationStatus = async (jobId: string) => {
        const pollInterval = setInterval(async () => {
            try {
                const response = await api.generation.getStatus(jobId);

                if (response.status === "completed" && response.media && response.media.length > 0) {
                    clearInterval(pollInterval);

                    // Map all backend media items to frontend Generation type
                    const newGenerations: Generation[] = response.media.map((item) => ({
                        id: item.id,
                        prompt: item.prompt,
                        type: item.type as "image" | "video",
                        url: item.url,
                        thumbnailUrl: item.thumbnail_url || item.url,
                        model: item.model_used || "",
                        aspectRatio: item.aspect_ratio || "1:1",
                        starred: item.is_starred || false,
                        createdAt: item.created_at,
                    }));

                    // Add unique new generations to state
                    setGenerations(prev => {
                        const existingIds = new Set(prev.map(g => g.id));
                        const uniqueNew = newGenerations.filter(g => !existingIds.has(g.id));
                        return [...uniqueNew, ...prev];
                    });

                    setIsGenerating(false);
                    toast.success("Generation complete!");
                } else if (response.status === "failed") {
                    clearInterval(pollInterval);
                    setIsGenerating(false);
                    toast.error(response.error_message || "Generation failed");
                }
            } catch (error) {
                console.error("Polling failed", error);
                clearInterval(pollInterval);
                setIsGenerating(false);
                toast.error("Generation failed");
            }
        }, 2000);
    };

    const generate = async (prompt: string) => {
        setIsGenerating(true);

        try {
            const payload = {
                prompt,
                model: currentModel,
                aspect_ratio: currentAspectRatio,
            };

            const response = mediaType === "video"
                ? await api.generation.createVideo(payload)
                : await api.generation.createImage(payload);

            // Check if the job already failed (e.g. Fal.ai API key missing or balance exhausted)
            if (response.status === "failed") {
                setIsGenerating(false);
                toast.error(response.error_message || "Generation failed. Please check your API configuration.");
                return;
            }

            toast.info(`${mediaType === "video" ? "Video" : "Image"} generation started...`);
            pollGenerationStatus(response.job_id);

        } catch (error) {
            console.error("Generation failed:", error);
            setIsGenerating(false);
        }
    };

    const likeGeneration = async (id: string) => {
        try {
            const response = await api.library.toggleStar(id);
            setGenerations(generations.map(gen =>
                gen.id === id ? { ...gen, starred: response.starred } : gen
            ));
        } catch (error) {
            console.error("Failed to toggle star", error);
        }
    };

    const downloadImage = (url: string) => {
        // Create a temporary anchor to trigger download
        const link = document.createElement('a');
        link.href = url;
        link.target = "_blank"; // Open in new tab if download fails
        link.download = `artxtic-${Date.now()}.jpg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <PlaygroundContext.Provider
            value={{
                generations,
                isGenerating,
                currentModel,
                currentAspectRatio,
                mediaType,
                setCurrentModel,
                setCurrentAspectRatio,
                setMediaType,
                generate,
                likeGeneration,
                downloadImage,
            }}
        >
            {children}
        </PlaygroundContext.Provider>
    );
}

export function usePlayground() {
    const context = useContext(PlaygroundContext);
    if (context === undefined) {
        throw new Error("usePlayground must be used within a PlaygroundProvider");
    }
    return context;
}

export { MODELS, ASPECT_RATIOS };
