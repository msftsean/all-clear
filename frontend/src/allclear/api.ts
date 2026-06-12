import type { DemoClearBoard, HealthStatus, PipelineResult } from "./types";

// In production the nginx sidecar proxies /api -> BACKEND_URL, so a relative
// base works everywhere. VITE_API_BASE_URL can override for local dev.
const BASE = import.meta.env.VITE_API_BASE_URL || "";
const TIMEOUT = 60000;

export class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
    this.name = "ApiError";
  }
}

async function req<T>(path: string, init: RequestInit = {}): Promise<T> {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), TIMEOUT);
  try {
    const res = await fetch(`${BASE}/api${path}`, {
      ...init,
      signal: ctrl.signal,
      headers: { "Content-Type": "application/json", ...(init.headers || {}) },
    });
    if (!res.ok) {
      let detail = `Request failed (${res.status})`;
      try {
        const body = await res.json();
        detail = body.detail || body.message || detail;
      } catch {
        /* keep default */
      }
      throw new ApiError(detail, res.status);
    }
    return (await res.json()) as T;
  } catch (e) {
    if (e instanceof ApiError) throw e;
    if (e instanceof Error && e.name === "AbortError")
      throw new ApiError("The signal timed out.", 408);
    throw new ApiError(e instanceof Error ? e.message : "Network error", 0);
  } finally {
    clearTimeout(t);
  }
}

export function submitSignal(
  message: string,
  sessionId: string | null,
  channel: string,
): Promise<PipelineResult> {
  return req<PipelineResult>("/signals", {
    method: "POST",
    body: JSON.stringify({ message, session_id: sessionId, channel }),
  });
}

export function getHealth(): Promise<HealthStatus> {
  return req<HealthStatus>("/health");
}

export function getDemoClearBoard(): Promise<DemoClearBoard> {
  return req<DemoClearBoard>("/demo/clearboard?mode=loaded");
}
