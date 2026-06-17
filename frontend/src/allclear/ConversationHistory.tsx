/**
 * ConversationHistory — "My Conversations" panel (019-conversation-persistence).
 *
 * Shows the list of past sessions for the current anonymous student identity.
 * Each row shows topic, date, and incident IDs. Clicking a row expands the
 * full turn-by-turn transcript inline.
 */

import { useEffect, useState } from "react";
import { listSessions } from "./api";
import type { ConversationSession, ConversationTurn } from "./types";

function relativeDate(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60_000);
  if (mins < 2) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

function TurnRow({ turn }: { turn: ConversationTurn }) {
  return (
    <div className="border-l-2 border-zinc-700 pl-3 py-1 space-y-1">
      <p className="text-xs text-zinc-400 uppercase tracking-wide">
        {turn.input_modality} · {relativeDate(turn.timestamp)}
        {turn.escalated && (
          <span className="ml-2 text-red-400">⚠ escalated</span>
        )}
      </p>
      {turn.signal_text && (
        <p className="text-sm text-zinc-200">
          <span className="text-zinc-500">You: </span>
          {turn.signal_text}
        </p>
      )}
      {turn.agent_response && (
        <p className="text-sm text-emerald-400">
          <span className="text-zinc-500">Agent: </span>
          {turn.agent_response}
        </p>
      )}
      {turn.incident_id && (
        <p className="text-xs text-zinc-500">Incident: {turn.incident_id}</p>
      )}
    </div>
  );
}

function SessionRow({ session }: { session: ConversationSession }) {
  const [expanded, setExpanded] = useState(false);
  const isVoice = session.conversation_history.some(
    (t) => t.input_modality === "voice",
  );

  return (
    <div className="rounded-lg bg-zinc-800/60 border border-zinc-700 overflow-hidden">
      <button
        className="w-full text-left px-4 py-3 flex items-center gap-3 hover:bg-zinc-700/40 transition-colors"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        <span className="text-base leading-none">{isVoice ? "📞" : "💬"}</span>
        <span className="flex-1 min-w-0">
          <span className="block text-sm font-medium text-zinc-100 truncate">
            {session.topic_summary ?? "Conversation"}
          </span>
          <span className="text-xs text-zinc-400">
            {relativeDate(session.last_active)} ·{" "}
            {session.conversation_history.length} turn
            {session.conversation_history.length !== 1 ? "s" : ""}
            {session.incident_ids.length > 0 && (
              <> · Incidents: {session.incident_ids.join(", ")}</>
            )}
          </span>
        </span>
        <span className="text-zinc-500 text-xs">{expanded ? "▲" : "▼"}</span>
      </button>

      {expanded && session.conversation_history.length > 0 && (
        <div className="px-4 pb-4 space-y-2 border-t border-zinc-700 pt-3">
          {session.conversation_history.map((turn) => (
            <TurnRow key={turn.turn_number} turn={turn} />
          ))}
        </div>
      )}

      {expanded && session.conversation_history.length === 0 && (
        <p className="px-4 pb-4 text-xs text-zinc-500 border-t border-zinc-700 pt-3">
          No messages recorded in this session.
        </p>
      )}
    </div>
  );
}

interface ConversationHistoryProps {
  studentIdHash: string | null;
  /** Called when user wants to continue a specific session */
  onResume?: (sessionId: string) => void;
}

// Voice and phone call sessions are persisted under this fixed hash
// (sha256("demo_student") — must match _DEFAULT_STUDENT_HASH in backend/app/api/realtime.py).
const VOICE_SESSION_HASH =
  "dc52f8b08ee024ef41618bfcd26d3e6c437c5177d24a779f46867d646264304b";

export default function ConversationHistory({
  studentIdHash,
  onResume,
}: ConversationHistoryProps) {
  const [sessions, setSessions] = useState<ConversationSession[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    if (!studentIdHash) return;
    let cancelled = false;
    setLoading(true);
    setError(null);

    // Fetch both the user's text-chat sessions AND voice/phone sessions
    // (stored under the shared demo hash). Deduplicate and sort by last_active.
    const userFetch = listSessions(studentIdHash, 20);
    const voiceFetch =
      studentIdHash !== VOICE_SESSION_HASH
        ? listSessions(VOICE_SESSION_HASH, 20)
        : Promise.resolve([] as typeof sessions);

    Promise.all([userFetch, voiceFetch])
      .then(([userSessions, voiceSessions]) => {
        if (cancelled) return;
        const seen = new Set<string>();
        const merged = [...userSessions, ...voiceSessions]
          .filter((s) => {
            if (seen.has(s.session_id)) return false;
            seen.add(s.session_id);
            return true;
          })
          .sort(
            (a, b) =>
              new Date(b.last_active).getTime() -
              new Date(a.last_active).getTime(),
          );
        setSessions(merged);
      })
      .catch((err) => {
        if (!cancelled)
          setError(err instanceof Error ? err.message : "Failed to load history.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [studentIdHash, refreshKey]);

  if (!studentIdHash) {
    return (
      <p className="text-sm text-zinc-500 p-4">
        No identity found. Submit a signal to start tracking history.
      </p>
    );
  }

  if (loading) {
    return (
      <div className="p-4 space-y-2">
        {[1, 2, 3].map((n) => (
          <div
            key={n}
            className="h-14 rounded-lg bg-zinc-800/60 border border-zinc-700 animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-center space-y-2">
        <p className="text-sm text-red-400">
          Could not load history: {error}
        </p>
        <button
          className="text-xs text-zinc-400 hover:text-zinc-200 underline"
          onClick={() => setRefreshKey((k) => k + 1)}
        >
          Retry
        </button>
      </div>
    );
  }

  if (sessions.length === 0) {
    return (
      <div className="p-4 text-center space-y-2">
        <p className="text-sm text-zinc-500">No past conversations.</p>
        <p className="text-xs text-zinc-600">
          Submit a signal to start a conversation.
        </p>
        <button
          className="text-xs text-zinc-500 hover:text-zinc-300 underline"
          onClick={() => setRefreshKey((k) => k + 1)}
        >
          Refresh
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-2 p-2">
      <div className="flex justify-end px-1">
        <button
          className="text-xs text-zinc-500 hover:text-zinc-300 underline"
          onClick={() => setRefreshKey((k) => k + 1)}
          disabled={loading}
        >
          {loading ? "Loading…" : "Refresh"}
        </button>
      </div>
      {sessions.map((s) => (
        <div key={s.session_id}>
          <SessionRow session={s} />
          {onResume && (
            <button
              className="mt-1 ml-4 text-xs text-emerald-500 hover:text-emerald-400 transition-colors"
              onClick={() => onResume(s.session_id)}
            >
              Continue this session →
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
