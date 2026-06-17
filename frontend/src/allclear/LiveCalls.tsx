import { useEffect, useRef } from "react";
import { useTranscriptStream } from "../hooks/useTranscriptStream";
import type { TranscriptEvent } from "../types/demo";
import { Waveform } from "./components";

const PHONE_DISPLAY = "+1 (844) 207-0169";

function clock(iso: string): string {
  try {
    return new Date(iso).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return "";
  }
}

function duration(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

function StatusBadge({
  status,
  durationSeconds,
}: {
  status: string;
  durationSeconds: number | null;
}) {
  if (status === "active") {
    return (
      <span className="inline-flex items-center gap-2 rounded-tag border border-clear/50 bg-clear/10 px-2.5 py-1 font-mono text-[11px] text-clear">
        <span className="h-1.5 w-1.5 animate-blink rounded-full bg-clear" />
        live · on the line
      </span>
    );
  }
  if (status === "ended") {
    return (
      <span className="inline-flex items-center gap-2 rounded-tag border border-nline/70 bg-panel/70 px-2.5 py-1 font-mono text-[11px] text-ndim">
        <span className="h-1.5 w-1.5 rounded-full bg-ndim/60" />
        call ended{durationSeconds != null ? ` · ${duration(durationSeconds)}` : ""}
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-2 rounded-tag border border-nline/70 bg-panel/70 px-2.5 py-1 font-mono text-[11px] text-ndim">
      <span className="h-1.5 w-1.5 animate-blink rounded-full bg-voice/70" />
      standing by
    </span>
  );
}

function Bubble({ event }: { event: TranscriptEvent }) {
  if (event.type === "call_started") {
    return (
      <div className="my-4 flex justify-center">
        <span className="inline-flex items-center gap-2 rounded-chip border border-clear/40 bg-clear/10 px-4 py-1.5 font-mono text-[11px] text-clear">
          📞 call connected · {clock(event.timestamp)}
        </span>
      </div>
    );
  }

  if (event.type === "call_ended") {
    return (
      <div className="my-4 flex justify-center">
        <span className="inline-flex items-center gap-2 rounded-chip border border-nline/70 bg-panel/70 px-4 py-1.5 font-mono text-[11px] text-ndim">
          call ended · {duration(event.duration_seconds)}
        </span>
      </div>
    );
  }

  if (event.type === "tool_call") {
    return (
      <div className="my-3 flex justify-center">
        <span className="inline-flex items-center gap-2 rounded-tag border border-voice/40 bg-voice/10 px-3 py-1 font-mono text-[10px] text-voice">
          ⚙ {event.tool}
          {event.summary ? <span className="text-ndim">· {event.summary}</span> : null}
        </span>
      </div>
    );
  }

  const isCaller = event.type === "user_speech";
  return (
    <div className={`my-3 flex ${isCaller ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[78%] rounded-card border px-5 py-3.5 shadow-dark-glass backdrop-blur ${
          isCaller
            ? "rounded-br-[6px] border-nline/70 bg-panel/80"
            : "rounded-bl-[6px] border-voice/30 bg-voice/10"
        }`}
      >
        <div
          className={`mb-1 font-mono text-[10px] uppercase tracking-wider ${
            isCaller ? "text-ndim" : "text-voice"
          }`}
        >
          {isCaller ? "📱 caller" : "✦ all clear"}
        </div>
        <p className="whitespace-pre-wrap text-[17px] leading-relaxed text-nink">
          {(event as { text: string }).text}
        </p>
        <div className="mt-2 font-mono text-[10px] text-ndim/70">
          {clock(event.timestamp)}
        </div>
      </div>
    </div>
  );
}

export default function LiveCalls({ onExit }: { onExit: () => void }) {
  const { callState } = useTranscriptStream();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onExit();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onExit]);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [callState.events]);

  return (
    <div
      data-testid="live-calls"
      className="fixed inset-0 z-50 flex flex-col overflow-hidden bg-antimetal-hero text-nink"
    >
      {/* atmosphere — match the night-world canvas */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_8px_8px,rgba(255,255,255,.34)_1px,transparent_1.5px)] bg-[length:24px_24px] opacity-10 [mask-image:linear-gradient(180deg,#000,transparent_72%)]" />
      <div className="pointer-events-none absolute -right-28 -top-36 h-[620px] w-[620px] rounded-full bg-[radial-gradient(50%_50%,rgba(0,128,248,.28)_0%,rgba(95,189,247,.28)_20%,rgba(211,239,252,.24)_60%,rgba(248,249,252,0)_100%)]" />

      {/* top bar */}
      <header className="relative z-10 flex flex-shrink-0 items-center justify-between border-b border-nline/70 bg-night/40 px-6 py-4 backdrop-blur">
        <div className="flex items-center gap-3.5">
          <button
            onClick={onExit}
            aria-label="Back to briefing room (Esc)"
            title="Back (Esc)"
            className="rounded-chip border border-nline/70 px-2.5 py-1 font-mono text-[11px] text-ndim transition-colors hover:border-voice/50 hover:text-nink"
          >
            ← back
          </button>
          <img src="/allclear-mark.svg" alt="" className="h-6 w-6 flex-none" />
          <span className="font-display text-[19px] font-medium tracking-tight text-nink">
            All Clear
          </span>
          <span className="text-nline">|</span>
          <div className="flex items-center gap-2 text-ndim">
            <Waveform live={callState.status === "active"} />
            <span className="font-mono text-[13px] text-nink">{PHONE_DISPLAY}</span>
          </div>
        </div>
        <StatusBadge status={callState.status} durationSeconds={callState.durationSeconds} />
      </header>

      {/* transcript */}
      <div
        ref={scrollRef}
        className="relative z-10 flex-1 overflow-y-auto px-6 py-8 md:px-[12%]"
        role="log"
        aria-live="polite"
        aria-label="Live phone transcript"
      >
        {callState.events.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="mb-6">
              <Waveform live={false} />
            </div>
            <p className="mb-2 font-display text-2xl font-light text-ndim">
              Pane of glass — waiting for a call
            </p>
            <p className="font-mono text-[13px] text-ndim/70">
              dial{" "}
              <span className="font-semibold text-nink">{PHONE_DISPLAY}</span> to watch
              the conversation live
            </p>
          </div>
        ) : (
          callState.events.map((evt, i) => (
            <Bubble key={`${evt.call_id}-${i}`} event={evt} />
          ))
        )}
      </div>

      {/* footer */}
      <div className="relative z-10 flex-shrink-0 border-t border-nline/50 bg-night/30 px-6 py-2">
        <p className="text-center font-mono text-[10px] text-ndim/60">
          All Clear — live phone triage monitor · transcripts stream in real time
        </p>
      </div>
    </div>
  );
}
