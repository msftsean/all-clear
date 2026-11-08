// Room Surge API client (024-room-surge).

const BASE = import.meta.env.VITE_API_BASE_URL || "";

export interface SurgeTile {
  incident_id: string;
  severity: "SEV1" | "SEV2" | "SEV3" | "SEV4";
  queue: string;
  category: string;
  location: string | null;
  escalated: boolean;
  room_reports: number;
  magnitude: number;
}

export interface SurgeState {
  open: boolean;
  opened_at: number | null;
  closed_at: number | null;
  signals: number;
  incidents: number;
  ratio: number | null;
  devices: number;
  blocked: number;
  escalated_to_person: number;
  rate_limited: number;
  failed: number;
  by_card: Record<string, number>;
  replica: string;
  tiles: SurgeTile[];
}

export type SurgeOutcome = "opened" | "joined" | "blocked" | "escalated" | "received";

export interface SurgeReportResult {
  accepted: boolean;
  outcome: SurgeOutcome;
  incident_id?: string | null;
  room_reports?: number;
  severity?: string;
  message: string;
}

export class SurgeError extends Error {
  constructor(message: string, public status: number) {
    super(message);
    this.name = "SurgeError";
  }
}

async function call<T>(path: string, init: RequestInit = {}, timeoutMs = 30000): Promise<T> {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(`${BASE}/api/surge${path}`, {
      ...init,
      signal: ctrl.signal,
      headers: { "Content-Type": "application/json", ...(init.headers || {}) },
    });
    if (!res.ok) {
      let detail = `Request failed (${res.status})`;
      try {
        const body = await res.json();
        if (typeof body.detail === "string") detail = body.detail;
      } catch {
        /* keep default */
      }
      throw new SurgeError(detail, res.status);
    }
    return (await res.json()) as T;
  } catch (e) {
    if (e instanceof SurgeError) throw e;
    if (e instanceof Error && e.name === "AbortError")
      throw new SurgeError("That took too long. Try again.", 408);
    throw new SurgeError("No connection. Check your Wi-Fi or data and try again.", 0);
  } finally {
    clearTimeout(t);
  }
}

export function getSurgeState(): Promise<SurgeState> {
  return call<SurgeState>("/state", {}, 5000);
}

export function submitSurgeReport(
  message: string,
  deviceId: string,
  card: string | null,
): Promise<SurgeReportResult> {
  return call<SurgeReportResult>("/report", {
    method: "POST",
    body: JSON.stringify({ message, device_id: deviceId, card }),
  });
}

export function controlSurge(
  action: "open" | "close" | "reset",
  key: string | null,
): Promise<SurgeState> {
  return call<SurgeState>("/control", {
    method: "POST",
    body: JSON.stringify({ action }),
    headers: key ? { "X-Surge-Key": key } : {},
  });
}

const DEVICE_KEY = "allclear.surge.device";

/** Random per-phone id for rate limiting. Not an identity; never displayed. */
export function deviceId(): string {
  try {
    const existing = localStorage.getItem(DEVICE_KEY);
    if (existing && /^[A-Za-z0-9-]{8,64}$/.test(existing)) return existing;
    const fresh =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? crypto.randomUUID()
        : `dev-${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`;
    localStorage.setItem(DEVICE_KEY, fresh);
    return fresh;
  } catch {
    return `dev-${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`;
  }
}
