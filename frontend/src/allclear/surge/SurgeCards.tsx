import Qr from "./Qr";
import { SURGE_CARDS, reportUrl } from "./cards";
import { SurgeModeNotice } from "./SurgeMode";
import { useSurgeMode } from "./useSurgeMode";

// Printable table cards (024-room-surge). /surge/cards?copies=2&only=ABCDR
// Each card's QR opens the report page with that card preselected.

export default function SurgeCards() {
  const mode = useSurgeMode();
  const params = new URLSearchParams(window.location.search);
  const copies = Math.min(10, Math.max(1, Number(params.get("copies")) || 1));
  const only = (params.get("only") || "").toUpperCase();
  const origin = params.get("origin") || window.location.origin;
  const cards = SURGE_CARDS.filter((c) => !only || only.includes(c.id));
  const sheet = cards.flatMap((c) => Array.from({ length: copies }, (_, i) => ({ card: c, n: i })));

  return (
    <main className="mx-auto max-w-[8.5in] bg-white p-6 text-inkwarm print:p-0" data-testid="surge-cards">
      <SurgeModeNotice mode={mode} />
      <p className="mb-4 text-sm text-midwarm print:hidden">
        Print this page (two cards per row). Use ?copies=N for more of each, ?only=ABCD to filter, and
        ?origin=https://your-host if you're printing from another environment.
      </p>
      <div className="grid grid-cols-2 gap-4">
        {(mode === "mock" || mode === "live") && sheet.map(({ card, n }) => (
          <section
            key={`${card.id}-${n}`}
            data-testid="surge-print-card"
            className={`flex break-inside-avoid flex-col gap-3 rounded-card border-2 p-5 ${
              card.tone === "red" ? "border-sev1" : card.tone === "own" ? "border-clear" : "border-voice"
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-sm">ALL CLEAR · CARD {card.id}</span>
              <span className="text-xs text-midwarm">Azure Days Arlington</span>
            </div>
            <h2 className="text-2xl font-semibold">{card.title}</h2>
            <p className="text-base leading-snug">{card.scene}</p>
            <p className="text-sm text-midwarm">
              {mode === "mock"
                ? card.tone === "event"
                  ? "Mock rehearsal: select Use sample report on your phone. Matching wording illustrates grouping without live AI."
                  : "Mock rehearsal: follow this scenario to exercise offline processing, not live AI."
                : `${card.prompt} Don't copy this card. Say it your way.`}
            </p>
            <div className="mt-auto flex items-end justify-between gap-3">
              <span className="text-sm">
                Wait for the <strong>OPEN</strong> signal on screen,
                <br />
                then scan and report.
              </span>
              <Qr value={reportUrl(origin, card.id)} size={120} label={`Report card ${card.id}`} />
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
