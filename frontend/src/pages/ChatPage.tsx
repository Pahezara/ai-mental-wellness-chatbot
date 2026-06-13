import React, { useMemo, useRef, useState, useEffect } from "react";
import { sendChat, pingHealth } from "../lib/api";
import { getOrCreateUserId, getSessionId, setSessionId, clearSession } from "../lib/storage";
import type { Message } from "../types";

function riskClass(r: string) {
    if (r === "high") return "badge danger";
    if (r === "medium") return "badge warn";
    return "badge ok";
}

export default function ChatPage() {
    const userId = useMemo(() => getOrCreateUserId(), []);
    const [sessionId, _setSessionId] = useState<string | null>(() => getSessionId());

    const [messages, setMessages] = useState<Message[]>([
        {
            id: crypto.randomUUID(),
            role: "assistant",
            text: "Hi — I’m here with you. You can type in Sinhala or English. What’s going on?",
            ts: Date.now(),
        },
    ]);

    const [input, setInput] = useState("");
    const [sending, setSending] = useState(false);
    const [online, setOnline] = useState<boolean | null>(null);
    const [error, setError] = useState<string | null>(null);

    const bottomRef = useRef<HTMLDivElement | null>(null);
    const lastAssistant = [...messages].reverse().find((m) => m.role === "assistant") ?? null;

    useEffect(() => {
        (async () => setOnline(await pingHealth()))();
    }, []);

    function scrollToBottom() {
        requestAnimationFrame(() => bottomRef.current?.scrollIntoView({ behavior: "smooth" }));
    }

    function newSession() {
        clearSession();
        _setSessionId(null);
        setMessages([
            {
                id: crypto.randomUUID(),
                role: "assistant",
                text: "New session started. I’m here with you — what would you like to talk about?",
                ts: Date.now(),
            },
        ]);
        scrollToBottom();
    }

    async function onSend() {
        const text = input.trim();
        if (!text || sending) return;

        setError(null);
        setMessages((p) => [...p, { id: crypto.randomUUID(), role: "user", text, ts: Date.now() }]);
        setInput("");
        setSending(true);
        scrollToBottom();

        try {
            const resp = await sendChat({
                user_id: userId,
                session_id: sessionId,
                message: text,

                //Always use gentle friend mode
                style: "gentle_friend",

                //Privacy-safe defaults
                consent_store_text: false,
                consent_send_to_llm: false,
            });

            setSessionId(resp.session_id);
            _setSessionId(resp.session_id);

            setMessages((p) => [
                ...p,
                {
                    id: crypto.randomUUID(),
                    role: "assistant",
                    text: resp.reply,
                    ts: Date.now(),
                    meta: {
                        emotion: resp.emotion.label,
                        confidence: resp.emotion.confidence,
                        risk: resp.risk_level,
                        writer_source: resp.writer_source,
                        detected_language: resp.detected_language,
                        translated_to_english: resp.translated_to_english,
                    },
                },
            ]);

            setOnline(true);
            scrollToBottom();
        } catch (e: any) {
            setOnline(false);
            setError(e?.message ?? "Failed to fetch");
            setMessages((p) => [
                ...p,
                {
                    id: crypto.randomUUID(),
                    role: "assistant",
                    text: "I couldn’t reach the server. Please check that the backend is running, then try again.",
                    ts: Date.now(),
                },
            ]);
            scrollToBottom();
        } finally {
            setSending(false);
        }
    }

    const risk = lastAssistant?.meta?.risk ?? "low";

    return (
        <>
            <div className="topbar">
                <div className="topbarRow container">
                    <div className="brand">
                        <div className="logo">❤</div>
                        <div className="brandTitle">
                            <h1>Mental Chat</h1>
                            <p>Supportive Sinhala & English mental wellness companion</p>
                        </div>
                    </div>

                    <div className="actions">
                        <span className={riskClass(online === false ? "high" : risk)}>
                            {online === false ? "Offline" : `Risk: ${risk}`}
                        </span>
                        <button className="btn" onClick={newSession}>
                            New
                        </button>
                    </div>
                </div>
            </div>

            <div className="container layout">
                <div className="card">
                    <div className="cardHeader">
                        <h2>About this chat</h2>
                        <p>
                            A gentle companion for difficult moments. Type naturally in Sinhala or English.
                        </p>
                    </div>

                    <div className="cardBody">
                        <div className="smallNote">
                            This tool is supportive and not a replacement for professional care.
                            <br />
                            If you feel unsafe or at risk, contact help immediately. Sri Lanka: <b>1926</b>.
                        </div>
                    </div>
                </div>

                <div className="card chatWrap">
                    <div className="cardHeader">
                        <h2>Chat</h2>
                        <p>Enter = send · Shift+Enter = new line</p>
                    </div>

                    {error ? (
                        <div className="cardBody" style={{ paddingBottom: 0 }}>
                            <div
                                className="smallNote"
                                style={{ borderColor: "rgba(255,107,107,.35)", color: "rgba(255,220,220,.95)" }}
                            >
                                <b>Connection error:</b> {error}
                            </div>
                        </div>
                    ) : null}

                    <div className="messages">
                        {messages.map((m) => (
                            <div key={m.id} className={`row ${m.role}`}>
                                <div className={`bubble ${m.role}`}>
                                    {m.text}
                                    <div className="meta">
                                        <span>{new Date(m.ts).toLocaleTimeString()}</span>
                                        <span />
                                    </div>
                                </div>
                            </div>
                        ))}

                        {sending ? (
                            <div style={{ color: "var(--muted)", fontSize: 12, paddingLeft: 6 }}>
                                Typing…
                            </div>
                        ) : null}

                        <div ref={bottomRef} />
                    </div>

                    <div className="composer">
                        <textarea
                            className="textarea"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type your message…"
                            onKeyDown={(e) => {
                                if (e.key === "Enter" && !e.shiftKey) {
                                    e.preventDefault();
                                    void onSend();
                                }
                            }}
                        />
                        <button className="btn btnPrimary" style={{ width: 140 }} onClick={() => void onSend()} disabled={sending}>
                            Send
                        </button>
                    </div>

                    <div className="helper">
                        <span>{online === false ? "Backend offline" : "Connected"}</span>
                        <span>Gentle friend mode</span>
                    </div>
                </div>
            </div>
        </>
    );
}