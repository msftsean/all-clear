import { useEffect, useRef, useState } from "react";
import { ApiError, getDemoClearBoard, getHealth, submitSignal } from "./api";
import type { DemoClearBoard, PipelineResult } from "./types";
import { MonoPill, Waveform } from "./components";
import { Canvas, DecisionReceipt } from "./Canvas";
import LiveCalls from "./LiveCalls";
import { HERO_DEMO_BOARD } from "./demo";

type Role = "caller" | "agent" | "system";
interface Msg {
  id: string;
  role: Role;
  text: string;
  channel?: string;
  ts: number;
}

function uid(): string {
  return Math.random().toString(36).slice(2, 10);
}

function clock(ts: number): string {
  return new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function initialDemoMode(): "blank" | "loaded" | null {
  const mode = new URLSearchParams(window.location.search).get("demo");
  return mode === "blank" || mode === "loaded" || mode === "hero" ? (mode === "blank" ? "blank" : "loaded") : null;
}

// The agent's plain-spoken voice line, derived from the typed result.
function agentVoice(r: PipelineResult): string {
  const a = r.action;
  const rd = r.routing;
  const community =
    rd.outcome === "ATTACH_TO_INCIDENT"
      ? `You're not the only one — this joins ${a.incident_id}, now ${rd.magnitude} report${rd.magnitude === 1 ? "" : "s"}. `
      : "";
  const boundary = a.sitrep
    ? " I drafted the all-clear, but it needs your approval before it goes out — that's the boundary, not a bug."
    : "";
  return `${community}${a.user_message}${boundary}`;
}

const SUGGESTIONS = [
  "There's a downed power line sparking on Oak Street near the school.",
  "The whole neighborhood lost power about ten minutes ago.",
  "I just want to check the status of the outage on 5th Avenue.",
];

const SURGE_DURATION_MS = 7200;

export default function BriefingRoom() {
  const [messages, setMessages] = useState<Msg[]>([
    {
      id: uid(),
      role: "agent",
      text:
        "All Clear here. Tell me what's happening and I'll classify it, route it, and open or attach an incident. Anything public-facing waits for your approval.",
      ts: Date.now(),
    },
  ]);
  const [input, setInput] = useState("");
  const [channel, setChannel] = useState<"chat" | "phone">("chat");
  const [busy, setBusy] = useState(false);
  const [sessionId] = useState(() => `sess-${uid()}`);
  const [latest, setLatest] = useState<PipelineResult | null>(null);
  const [receiptOpen, setReceiptOpen] = useState(false);
  const [published, setPublished] = useState<Set<string>>(new Set());
  const [health, setHealth] = useState<{ ok: boolean; live: boolean } | null>(null);
  const [liveOpen, setLiveOpen] = useState(false);
  const [demoMode, setDemoMode] = useState<"blank" | "loaded" | null>(() => initialDemoMode());
  const [demoBoard, setDemoBoard] = useState<DemoClearBoard | null>(
    () => (initialDemoMode() === "loaded" ? HERO_DEMO_BOARD : null),
  );
  const [demoSignalsReceived, setDemoSignalsReceived] = useState(() =>
    initialDemoMode() === "loaded" ? 0 : HERO_DEMO_BOARD.total_signals,
  );
  const [demoSurgeRun, setDemoSurgeRun] = useState(0);
  const [signalCount, setSignalCount] = useState(0);
  const [clearBoardIncidents, setClearBoardIncidents] = useState<
    Record<string, DemoClearBoard["incidents"][number]>
  >({});
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getHealth()
      .then((h) => setHealth({ ok: h.status === "healthy", live: !h.mock_mode }))
      .catch(() => setHealth({ ok: false, live: false }));
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (demoMode === "loaded") {
      setDemoBoard(HERO_DEMO_BOARD);
      getDemoClearBoard()
        .then(setDemoBoard)
        .catch(() => setDemoBoard(HERO_DEMO_BOARD));
    } else {
      setDemoBoard(null);
    }
  }, [demoMode]);

  useEffect(() => {
    if (demoMode !== "loaded" || !demoBoard) return;

    const started = performance.now();
    const total = demoBoard.total_signals;
    setDemoSignalsReceived(0);
    const timer = window.setInterval(() => {
      const elapsed = performance.now() - started;
      const progress = Math.min(1, elapsed / SURGE_DURATION_MS);
      const eased = 1 - Math.pow(1 - progress, 2.6);
      const next = Math.min(total, Math.floor(eased * total));
      setDemoSignalsReceived(next);
      if (next >= total) {
        window.clearInterval(timer);
      }
    }, 80);

    return () => window.clearInterval(timer);
  }, [demoMode, demoBoard, demoSurgeRun]);

  function setDemo(mode: "blank" | "loaded" | null) {
    const url = new URL(window.location.href);
    if (mode) {
      url.searchParams.set("demo", mode);
    } else {
      url.searchParams.delete("demo");
    }
    window.history.replaceState({}, "", url);
    setDemoSignalsReceived(0);
    setDemoMode(mode);
  }

  function simulateSurge() {
    setDemo("loaded");
    setDemoSurgeRun((n) => n + 1);
  }

  function updateClearBoard(r: PipelineResult) {
    const incidentId = r.action.incident_id;
    const location = r.classification.entities?.location?.trim() || incidentId;
    setSignalCount((n) => n + 1);
    setClearBoardIncidents((prev) => {
      const existing = prev[incidentId];
      const magnitude = Math.max(existing?.report_count || 0, r.routing.magnitude || 1);
      return {
        ...prev,
        [incidentId]: {
          incident_id: incidentId,
          title: existing?.title || `${r.classification.intent_category.replace(/_/g, " ")} · ${location}`,
          location,
          queue: r.action.queue,
          severity: r.action.severity,
          report_count: magnitude,
          sla_minutes: r.routing.sla_minutes,
          dedup_similarity: r.routing.dedup_similarity ?? existing?.dedup_similarity ?? 0,
          status: r.action.status,
          summary: r.action.sitrep?.summary || r.action.user_message,
          sample_signals: [...(existing?.sample_signals || []), r.signal_text].slice(-3),
        },
      };
    });
  }

  async function send(text: string) {
    const trimmed = text.trim();
    if (!trimmed || busy) return;
    setBusy(true);
    setInput("");
    setMessages((m) => [...m, { id: uid(), role: "caller", text: trimmed, channel, ts: Date.now() }]);
    try {
      const r = await submitSignal(trimmed, sessionId, channel);
      setLatest(r);
      updateClearBoard(r);
      setMessages((m) => [...m, { id: uid(), role: "agent", text: agentVoice(r), ts: Date.now() }]);
    } catch (e) {
      const msg =
        e instanceof ApiError && e.status === 400
          ? "That signal was rejected by content safety and wasn't processed. Rephrase it without disallowed content."
          : e instanceof ApiError
          ? `I couldn't process that signal (${e.status}). Try again in a moment.`
          : "I couldn't reach the triage service. Check the connection and try again.";
      setMessages((m) => [...m, { id: uid(), role: "system", text: msg, ts: Date.now() }]);
    } finally {
      setBusy(false);
    }
  }

  function approve(incidentId: string) {
    setPublished((p) => new Set(p).add(incidentId));
  }

  const liveClearBoard: DemoClearBoard | null =
    signalCount > 0
      ? {
          mode: "loaded",
          total_signals: signalCount,
          headline: "Live ClearBoard",
          subhead:
            "Live Signals are preserved as Reports; dedup attaches Reports to the same Incident and raises Magnitude.",
          incidents: Object.values(clearBoardIncidents).sort((a, b) => b.report_count - a.report_count),
        }
      : null;

  return (
    <div className="flex h-full w-full flex-col bg-paper md:flex-row">
      {/* ---- Paper world: conversation column ---- */}
      <div className="z-10 flex h-full w-full flex-col border-r border-paperline bg-paper2 shadow-[rgba(0,39,80,0.04)_1px_0_0_0] md:w-[430px] md:flex-none">
        <header className="flex items-center justify-between border-b border-paperline px-5 py-4">
          <div className="flex items-center gap-2.5">
            <img src="/allclear-mark.svg" alt="" className="h-6 w-6 flex-none" />
            <span className="font-display text-[21px] font-medium tracking-tight text-inkwarm">
              All Clear
            </span>
          </div>
          <div className="flex items-center gap-2">
            {demoMode ? (
              <DemoToggle
                mode={demoMode}
                onSetMode={setDemo}
                onSimulateSurge={simulateSurge}
                signalsReceived={demoSignalsReceived}
                totalSignals={demoBoard?.total_signals || HERO_DEMO_BOARD.total_signals}
              />
            ) : null}
            <button
              data-testid="live-calls-toggle"
              onClick={() => setLiveOpen(true)}
              className="inline-flex items-center gap-1.5 rounded-chip border border-paperline bg-paper2 px-2.5 py-1 font-mono text-[10px] uppercase tracking-wider text-voice shadow-antimetal-soft transition-colors hover:border-voice/50"
              title="Watch live phone calls"
            >
              📞 live calls
            </button>
            {health ? (
              <span
                data-testid="health-pill"
                className="rounded-chip bg-paper px-2.5 py-1 font-mono text-[10px] text-midwarm shadow-antimetal-soft"
                title={health.live ? "Live model" : "Mock / offline"}
              >
                {health.ok ? (health.live ? "● live" : "● mock") : "○ offline"}
              </span>
            ) : null}
          </div>
        </header>

        {/* Live channel strip — voice orange, the only ambient motion */}
        <div className="flex items-center gap-3 border-b border-paperline/70 bg-paper px-5 py-3">
          <Waveform live={channel === "phone"} />
          <button
            data-testid="channel-toggle"
            onClick={() => setChannel((c) => (c === "phone" ? "chat" : "phone"))}
            className="ml-auto rounded-chip border border-paperline bg-paper2 px-3 py-1.5 font-mono text-[10px] uppercase tracking-wider text-voice shadow-antimetal-soft transition-colors hover:border-voice/50"
          >
            {channel === "phone" ? "● inbound · phone" : "chat"}
          </button>
        </div>

        <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto bg-paper px-5 py-5">
          {messages.map((m) => (
            <MessageBubble key={m.id} m={m} />
          ))}
          {/* Classification chips materialize under the transcript */}
          {latest ? <ChipStrip r={latest} /> : null}
          {busy ? (
            <div className="flex items-center gap-1.5 px-1 text-midwarm" data-testid="thinking">
              <span className="h-1.5 w-1.5 animate-blink rounded-full bg-midwarm" />
              <span className="text-[12px]">Classifying…</span>
            </div>
          ) : null}
        </div>

        {messages.length <= 1 ? (
          <div className="flex flex-wrap gap-1.5 px-4 pb-2">
            {SUGGESTIONS.map((s, i) => (
              <button
                key={i}
                data-testid={`suggestion-${i}`}
                onClick={() => send(s)}
                className="rounded-chip border border-paperline bg-paper2 px-3 py-1.5 text-left text-[11px] text-midwarm shadow-antimetal-soft transition-colors hover:border-voice/50 hover:text-inkwarm"
              >
                {s}
              </button>
            ))}
          </div>
        ) : null}

        <form
          className="border-t border-paperline bg-paper2 p-3"
          onSubmit={(e) => {
            e.preventDefault();
            send(input);
          }}
        >
          <div className="flex items-end gap-2">
            <textarea
              data-testid="signal-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  send(input);
                }
              }}
              rows={2}
              placeholder="Describe the signal…"
              className="flex-1 resize-none rounded-bubble border border-paperline bg-paper2 px-3 py-2 text-[13px] text-inkwarm shadow-antimetal-soft placeholder:text-midwarm/60 focus:border-voice"
            />
            <button
              data-testid="send-signal"
              type="submit"
              disabled={busy || !input.trim()}
              className="rounded-chip bg-grad px-5 py-2 font-sans text-[13px] font-semibold text-white shadow-antimetal-cta transition hover:brightness-105 disabled:opacity-40"
            >
              Send
            </button>
          </div>
        </form>
      </div>

      {/* ---- Night world: canvas ---- */}
      <main className="relative hidden flex-1 overflow-y-auto bg-antimetal-hero md:block">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_8px_8px,rgba(255,255,255,.34)_1px,transparent_1.5px)] bg-[length:24px_24px] opacity-15 [mask-image:linear-gradient(180deg,#000,transparent_72%)]" />
        <div className="pointer-events-none absolute -right-28 -top-36 h-[620px] w-[620px] rounded-full bg-[radial-gradient(50%_50%,rgba(0,128,248,.32)_0%,rgba(95,189,247,.32)_20%,rgba(211,239,252,.32)_60%,rgba(248,249,252,0)_100%)]" />
        <div className="relative z-10">
          <Canvas
            result={latest}
            onOpenReceipt={() => setReceiptOpen(true)}
            demoBoard={demoBoard}
            clearBoard={liveClearBoard}
            demoBlank={demoMode === "blank"}
            demoSignalsReceived={demoSignalsReceived}
          />
        </div>
      </main>

      {/* Mobile canvas summary (no split on phones per DESIGN) */}
      {latest ? (
        <div className="border-t border-nline bg-antimetal-hero p-3 md:hidden">
          <button
            data-testid="open-receipt-mobile"
            onClick={() => setReceiptOpen(true)}
            className="w-full rounded-chip border border-nline px-3 py-2 text-[12px] text-nink"
          >
            View {latest.action.incident_id} · {latest.action.severity}
          </button>
        </div>
      ) : null}

      {receiptOpen && latest ? (
        <DecisionReceipt
          r={latest}
          published={published.has(latest.action.incident_id)}
          onApprove={() => approve(latest.action.incident_id)}
          onClose={() => setReceiptOpen(false)}
        />
      ) : null}

      {liveOpen ? <LiveCalls onExit={() => setLiveOpen(false)} /> : null}
    </div>
  );
}

function DemoToggle({
  mode,
  onSetMode,
  onSimulateSurge,
  signalsReceived,
  totalSignals,
}: {
  mode: "blank" | "loaded";
  onSetMode: (mode: "blank" | "loaded" | null) => void;
  onSimulateSurge: () => void;
  signalsReceived: number;
  totalSignals: number;
}) {
  const surgeRunning = mode === "loaded" && signalsReceived < totalSignals;
  return (
    <div data-testid="demo-toggle" className="hidden items-center gap-1 sm:flex">
      <span className="font-mono text-[9px] uppercase tracking-wider text-midwarm/70">demo</span>
      <button
        data-testid="simulate-surge"
        onClick={onSimulateSurge}
        className="rounded-chip border border-voice/60 bg-voice/10 px-2.5 py-1 font-mono text-[10px] uppercase tracking-wider text-voice shadow-antimetal-soft"
      >
        {surgeRunning ? "surge running" : "simulate surge"}
      </button>
      <button
        onClick={() => onSetMode("blank")}
        className={`rounded-chip border px-2 py-1 font-mono text-[10px] uppercase tracking-wider shadow-antimetal-soft ${
          mode === "blank" ? "border-voice/60 text-voice" : "border-paperline text-midwarm"
        }`}
      >
        blank
      </button>
      <button
        onClick={() => onSetMode("loaded")}
        className={`rounded-chip border px-2 py-1 font-mono text-[10px] uppercase tracking-wider shadow-antimetal-soft ${
          mode === "loaded" ? "border-voice/60 text-voice" : "border-paperline text-midwarm"
        }`}
      >
        loaded
      </button>
      <button
        onClick={() => onSetMode(null)}
        className="rounded-chip border border-paperline px-2 py-1 font-mono text-[10px] uppercase tracking-wider text-midwarm shadow-antimetal-soft"
        title="Exit demo mode"
      >
        live
      </button>
    </div>
  );
}

function MessageBubble({ m }: { m: Msg }) {
  if (m.role === "system") {
    return (
      <div
        data-testid="system-message"
        className="rounded-bubble border border-dashed border-paperline bg-paper2 px-3 py-2 text-[12px] text-midwarm shadow-antimetal-soft"
      >
        {m.text}
      </div>
    );
  }
  const isAgent = m.role === "agent";
  return (
    <div
      data-testid={isAgent ? "agent-message" : "caller-message"}
      className={`flex flex-col ${isAgent ? "items-start" : "items-end"}`}
    >
      <div
        className={`max-w-[86%] rounded-bubble border px-3 py-2 shadow-antimetal-card ${
          isAgent
            ? "rounded-bl-[6px] border-paperline bg-paper2 font-sans text-[13.5px] font-medium text-inkwarm"
            : "rounded-br-[6px] border-paperline bg-paper2/90 font-sans text-[13px] text-inkwarm"
        }`}
        style={isAgent ? { letterSpacing: "-0.005em" } : undefined}
      >
        {m.text}
      </div>
      <div className="mt-0.5 flex items-center gap-1.5 px-1">
        {m.channel === "phone" ? (
          <span className="font-mono text-[9px] uppercase tracking-wider text-voice">phone</span>
        ) : null}
        <span className="font-mono text-[9px] text-midwarm/70">{clock(m.ts)}</span>
      </div>
    </div>
  );
}

// Waveform-to-chips: structured chips materialize under the transcript (DESIGN #1)
function ChipStrip({ r }: { r: PipelineResult }) {
  const c = r.classification;
  return (
    <div data-testid="chip-strip" className="animate-rise flex flex-wrap gap-1.5 pt-1">
      <MonoPill>{c.intent_category}</MonoPill>
      <MonoPill>{r.action.severity}</MonoPill>
      <MonoPill>conf {Math.round(c.confidence * 100)}%</MonoPill>
      {c.pii_detected ? <MonoPill tone="voice">pii redacted</MonoPill> : null}
      {r.routing.escalate ? <MonoPill tone="voice">escalated</MonoPill> : null}
    </div>
  );
}
