export type ChatStyle = "gentle_friend" | "coach" | "practical" | "short";

export type ChatRequest = {
    user_id: string;
    session_id: string | null;
    message: string;
    style: ChatStyle;
    consent_store_text: boolean;
    consent_send_to_llm: boolean;
};

export type ChatResponse = {
    session_id: string;
    detected_language: string;
    translated_to_english: string;
    emotion: { label: string; confidence: number };
    risk_level: "low" | "medium" | "high";
    reply: string;
    follow_up_question: string | null;
    writer_source: string;
};

export type TrendPoint = { date: string; emotion: string; count: number };
export type TrendsResponse = { user_id: string; points: TrendPoint[] };

const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function sendChat(payload: ChatRequest): Promise<ChatResponse> {
    const res = await fetch(`${BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Chat failed (${res.status}): ${text}`);
    }
    return res.json();
}

export async function fetchTrends(userId: string, days = 14): Promise<TrendsResponse> {
    const res = await fetch(`${BASE}/analytics/emotions/${encodeURIComponent(userId)}?days=${days}`);
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Trends failed (${res.status}): ${text}`);
    }
    return res.json();
}