import { useMemo, useState } from "react";
import { SURGE_CARDS, findCard, type SurgeCard } from "./cards";
import { SurgeError, deviceId, submitSurgeReport, type SurgeReportResult } from "./surgeApi";

// Mobile page an attendee opens from the QR code (024-room-surge).
// No sign-in. One textarea. The phone keyboard's mic handles dictation.

type Phase =
  | { kind: "idle" }
  | { kind: "sending" }
  | { kind: "done"; result: SurgeReportResult }
  | { kind: "error"; message: string };

const TONE: Record<SurgeCard["tone"], string> = {
  event: "border-voice/40 bg-voice/5",
  own: "border-clear/50 bg-clear/5",
  red: "border-sev1/50 bg-sev1/5",
};

export function resultHeadline(r: SurgeReportResult): string {
  switch (r.outcome) {
    case "joined":
      return `Your report joined ${r.incident_id}`;
    case "opened":
      return `You opened ${r.incident_id}`;
    case "blocked":
      return "Blocked by the safety filter";
    case "escalated":
      return "A person will review this";
    default:
      return "Report received";
  }
}

export function resultDetail(r: SurgeReportResult): string {
  if (r.outcome === "joined" && r.room_reports) {
    const others = r.room_reports - 1;
    return `${r.room_reports} people in this room reported the same thing${
      others > 0 ? "; you're not alone" : ""
    }. Watch the screen.`;
  }
  if (r.outcome === "opened") {
    return `You're the first in the room to report it${r.severity ? ` (${r.severity})` : ""}. Watch the screen.`;
  }
  return r.message;
}

export default function SurgeReport() {
  const params = new URLSearchParams(window.location.search);
  const [card, setCard] = useState<SurgeCard | null>(() => findCard(params.get("card")));
  const [text, setText] = useState("");
  const [phase, setPhase] = useState<Phase>({ kind: "idle" });
  const device = useMemo(() => deviceId(), []);

  async function send() {
    const message = text.trim();
    if (!message || phase.kind === "sending") return;
    setPhase({ kind: "sending" });
    try {
      const result = await submitSurgeReport(message, device, card?.id ?? null);
      setPhase({ kind: "done", result });
      setText("");
    } catch (e) {
      setPhase({
        kind: "error",
        message: e instanceof SurgeError ? e.message : "Something went wrong. Try again.",
      });
    }
  }

  return (
    <main className="mx-auto flex min-h-full max-w-md flex-col gap-4 px-4 py-6" data-testid="surge-report">
      <header>
        <div className="eyebrow text-midwarm">ALL CLEAR · ROOM SURGE</div>
        <h1 className="mt-1 font-display text-2xl font-semibold text-inkwarm">Report what you see</h1>
      </header>

      {card ? (
        <section className={`rounded-card border p-4 ${TONE[card.tone]}`} data-testid="surge-card">
          <div className="flex items-center justify-between">
            <span className="font-mono text-xs text-midwarm">CARD {card.id}</span>
            <button className="text-xs text-voice underline" onClick={() => setCard(null)}>
              change
            </button>
          </div>
          <h2 className="mt-1 text-lg font-semibold text-inkwarm">{card.title}</h2>
          <p className="mt-1 text-[15px] leading-snug text-inkwarm">{card.scene}</p>
          <p className="mt-2 text-sm text-midwarm">{card.prompt} Don't copy the card. Say it your way.</p>
        </section>
      ) : (
        <section aria-label="Pick your card" className="grid grid-cols-2 gap-2">
          {SURGE_CARDS.map((c) => (
            <button
              key={c.id}
              onClick={() => setCard(c)}
              className={`rounded-bubble border p-3 text-left ${TONE[c.tone]}`}
            >
              <div className="font-mono text-xs text-midwarm">CARD {c.id}</div>
              <div className="text-sm font-semibold text-inkwarm">{c.title}</div>
            </button>
          ))}
        </section>
      )}

      <label className="flex flex-col gap-2">
        <span className="text-sm text-midwarm">
          Type it, or tap the mic on your keyboard and say it.
        </span>
        <textarea
          data-testid="surge-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          maxLength={500}
          rows={4}
          placeholder="What's happening, and where?"
          className="rounded-bubble border border-paperline bg-paper2 p-3 text-base text-inkwarm shadow-antimetal-soft focus:outline-none focus:ring-2 focus:ring-voice"
        />
      </label>

      <button
        data-testid="surge-send"
        onClick={send}
        disabled={!text.trim() || phase.kind === "sending"}
        className="rounded-chip bg-cta px-5 py-3 text-base font-semibold text-ctaink shadow-antimetal-cta disabled:opacity-50"
      >
        {phase.kind === "sending" ? "Triaging…" : "Send report"}
      </button>

      <div aria-live="polite">
        {phase.kind === "done" && (
          <section
            data-testid="surge-result"
            className={`animate-rise rounded-card border p-4 ${
              phase.result.outcome === "blocked"
                ? "border-sev1/50 bg-sev1/5"
                : "border-clear/50 bg-clear/10"
            }`}
          >
            <h3 className="text-lg font-semibold text-inkwarm">{resultHeadline(phase.result)}</h3>
            <p className="mt-1 text-[15px] text-inkwarm">{resultDetail(phase.result)}</p>
          </section>
        )}
        {phase.kind === "error" && (
          <p data-testid="surge-error" className="rounded-bubble border border-sev2/50 bg-sev2/10 p-3 text-sm text-inkwarm">
            {phase.message}
          </p>
        )}
      </div>

      <footer className="mt-auto text-xs leading-snug text-midwarm">
        Demo at Azure Days Arlington. Don't include names, phone numbers or other personal details.
        Your words are processed by AI and are never shown on the big screen.
      </footer>
    </main>
  );
}
