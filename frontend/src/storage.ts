export function getOrCreateUserId(): string {
    const key = "mental_user_id";
    let v = localStorage.getItem(key);
    if (!v) {
        v = `u_${crypto.randomUUID()}`;
        localStorage.setItem(key, v);
    }
    return v;
}

export function getSessionId(): string | null {
    return localStorage.getItem("mental_session_id");
}

export function setSessionId(id: string) {
    localStorage.setItem("mental_session_id", id);
}

export function clearSession() {
    localStorage.removeItem("mental_session_id");
}