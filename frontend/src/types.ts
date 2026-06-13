export type Message = {
    id: string;
    role: "user" | "assistant";
    text: string;
    ts: number;
    meta?: {
        emotion?: string;
        confidence?: number;
        risk?: string;
        writer_source?: string;
        detected_language?: string;
        translated_to_english?: string;
    };
};