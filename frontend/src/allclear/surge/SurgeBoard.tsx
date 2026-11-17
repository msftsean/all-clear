import { useEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import { SEV } from "../components";
import Qr from "./Qr";
import { reportUrl } from "./cards";
import { SurgeError, controlSurge, getSurgeState, type SurgeState, type SurgeTile } from "./surgeApi";
import { SurgeModeNotice } from "./SurgeMode";
import { useSurgeMode } from "./useSurgeMode";

// Room display for the audience surge (024-room-surge). Shows counts and
// machine-derived tiles only; raw attendee text is never on screen.

const POLL_MS = 1000;
const KEY_STORE = "allclear.surge.key";

export const EMPTY_STATE: SurgeState = {
  open: false,
  opened_at: null,
  closed_at: null,
  signals: 0,
  incidents: 0,
  ratio: null,
  devices: 0,
  blocked: 0,
  escalated_to_person: 0,
  rate_limited: 0,
  failed: 0,
  by_card: {},
  replica: "",
  tiles: [],
};

// Read ?key= once, keep it in sessionStorage, and strip it from the URL so it is
// never visible on the projector.
function takeCoachKey(): string | null {
  try {
    const url = new URL(window.location.href);
    const fromUrl = url.searchParams.get("key");
    if (fromUrl) {
      url.searchParams.delete("key");
      window.history.replaceState(null, "", url.toString());
      try {
        sessionStorage.setItem(KEY_STORE, fromUrl);
      } catch {
        // Keep the key in memory when tab storage is unavailable.
      }
      return fromUrl;
    }
    return sessionStorage.getItem(KEY_STORE);
  } catch {
    return null;
  }
}

export function prettyCategory(category: string): string {
  return category
    .toLowerCase()
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

function Counter({ label, value, testid }: { label: string; value: number; testid: string }) {
  return (
    <div className="flex flex-col">
      <span className="eyebrow text-ndim">{label}</span>
      <span
        key={value}
        data-testid={testid}
        className="animate-rise font-display text-[96px] font-semibold leading-none text-nink tabular-nums"
      >
        {value}
      </span>
    </div>
  );
}

function Stat({ label, value, tone = "text-nink", testid }: { label: string; value: number; tone?: string; testid: string }) {
  return (
    <div className="flex items-baseline gap-2">
      <span data-testid={testid} className={`font-display text-3xl font-semibold tabular-nums ${tone}`}>
        {value}
      </span>
      <span className="text-sm text-ndim">{label}</span>
    </div>
  );
}

export function Tile({ tile }: { tile: SurgeTile }) {
  const s = SEV[tile.severity] ?? SEV.SEV4;
  return (
    <article
      data-testid="surge-tile"
      style={{ flexGrow: Math.max(1, tile.room_reports), flexBasis: 220 }}
      className={`min-w-[220px] rounded-card border-2 ${s.border} bg-panel/80 p-4 shadow-dark-glass`}
    >
      <div className="flex items-center justify-between gap-2">
        <span className="font-mono text-sm text-ndim">{tile.incident_id}</span>
        <span className={`rounded-tag border ${s.border} ${s.soft} px-2 py-0.5 font-mono text-xs ${s.text}`}>
          {tile.severity}
        </span>
      </div>
      <div className="mt-2 text-xl font-semibold text-nink">{prettyCategory(tile.category)}</div>
      {tile.location && <div className="text-base text-ndim">{tile.location}</div>}
      <div className="mt-3 flex items-baseline gap-2">
        <span key={tile.room_reports} className="animate-rise font-display text-5xl font-semibold tabular-nums text-nink">
          {tile.room_reports}
        </span>
        <span className="text-sm text-ndim">report{tile.room_reports === 1 ? "" : "s"} from this room</span>
      </div>
      {tile.escalated && <div className="mt-2 text-sm text-sev2">Escalated to a person</div>}
    </article>
  );
}

export function SurgeBoardView({
  state,
  joinUrl,
  stale,
  controls,
  notice,
}: {
  state: SurgeState;
  joinUrl: string;
  stale: boolean;
  controls?: ReactNode;
  notice?: ReactNode;
}) {
  const quiet = state.signals === 0 && state.blocked === 0;
  return (
    <main className="min-h-full bg-antimetal-hero p-8 text-nink" data-testid="surge-board">
      <header className="flex items-center justify-between">
        <div>
          <div className="eyebrow text-ndim">ALL CLEAR · ROOM SURGE</div>
          <h1 className="font-display text-4xl font-semibold">Many signals. Few incidents.</h1>
        </div>
        <div className="flex items-center gap-3">
          {stale && <span className="text-sm text-sev2">reconnecting…</span>}
          <span
            data-testid="surge-status"
            className={`rounded-chip border px-3 py-1 font-mono text-sm ${
              state.open ? "border-clear/60 bg-clear/10 text-clear" : "border-nline text-ndim"
            }`}
          >
            {state.open ? "● OPEN, REPORT NOW" : "CLOSED"}
          </span>
        </div>
      </header>
      {notice && <div className="mt-4">{notice}</div>}

      <section className="mt-8 grid grid-cols-[auto_1fr] gap-10">
        <div className="flex flex-col items-center gap-3">
          <Qr value={joinUrl} size={260} label="Scan to report" />
          <div className="max-w-[260px] break-all text-center font-mono text-lg text-nink">
            {joinUrl.replace(/^https?:\/\//, "")}
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="flex items-end gap-8">
            <Counter label="SIGNALS IN" value={state.signals} testid="surge-signals" />
            <span className="pb-6 font-display text-6xl text-ndim">→</span>
            <Counter label="INCIDENTS OUT" value={state.incidents} testid="surge-incidents" />
            {state.ratio !== null && (
              <span className="pb-6 font-mono text-2xl text-clear" data-testid="surge-ratio">
                {state.ratio}× collapse
              </span>
            )}
          </div>
          <div className="flex flex-wrap gap-8">
            <Stat label="phones in the room" value={state.devices} testid="surge-devices" />
            <Stat label="blocked by safety" value={state.blocked} tone="text-sev1" testid="surge-blocked" />
            <Stat
              label="escalated to a person"
              value={state.escalated_to_person}
              tone="text-sev2"
              testid="surge-escalated"
            />
          </div>
        </div>
      </section>

      <section className="mt-10">
        {quiet ? (
          <div className="rounded-card border border-nline/60 p-10 text-center text-2xl text-ndim">
            The board is quiet. Scan the code and report what's on your card.
          </div>
        ) : (
          <div className="flex flex-wrap gap-4">
            {state.tiles.map((t) => (
              <Tile key={t.incident_id} tile={t} />
            ))}
          </div>
        )}
      </section>

      {controls}
    </main>
  );
}

export default function SurgeBoard() {
  const mode = useSurgeMode();
  const [state, setState] = useState<SurgeState>(EMPTY_STATE);
  const [stale, setStale] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const keyRef = useRef<string | null>(null);
  const [coach, setCoach] = useState(false);
  const [keyInput, setKeyInput] = useState("");

  const params = new URLSearchParams(window.location.search);
  const joinUrl = params.get("join") || reportUrl(window.location.origin);

  useEffect(() => {
    keyRef.current = takeCoachKey();
    setCoach(Boolean(keyRef.current));
    let alive = true;
    const tick = async () => {
      try {
        const s = await getSurgeState();
        if (!alive) return;
        setState(s);
        setStale(false);
      } catch {
        if (alive) setStale(true);
      }
    };
    tick();
    const id = setInterval(tick, POLL_MS);
    return () => {
      alive = false;
      clearInterval(id);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function act(action: "open" | "close" | "reset") {
    if (action === "reset" && !window.confirm("Reset the room tally? Incidents and audit stay intact.")) return;
    try {
      setState(await controlSurge(action, keyRef.current));
      setMsg(null);
    } catch (e) {
      setMsg(e instanceof SurgeError ? e.message : "Control failed.");
    }
  }

  function saveCoachKey(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const key = keyInput.trim();
    keyRef.current = key || null;
    try {
      if (key) sessionStorage.setItem(KEY_STORE, key);
      else sessionStorage.removeItem(KEY_STORE);
    } catch {
      // The key remains available in memory if storage is unavailable.
    }
    setCoach(Boolean(key));
    setKeyInput("");
    setMsg(null);
  }

  const controls = (
    <footer className="fixed bottom-4 right-4 rounded-chip border border-nline bg-panel/90 px-3 py-2 text-sm">
      <details>
        <summary className="cursor-pointer text-ndim">Operator controls</summary>
        <form className="mt-2 flex items-end gap-2" onSubmit={saveCoachKey}>
          <label className="flex flex-col gap-1 text-ndim">
            Coach key
            <input
              type="password"
              autoComplete="off"
              value={keyInput}
              onChange={(event) => setKeyInput(event.target.value)}
              className="rounded-chip border border-nline bg-panel px-2 py-1 text-nink"
            />
          </label>
          <button type="submit" className="rounded-chip bg-nline px-3 py-1 text-nink">Set key</button>
        </form>
        {coach && (
          <div className="mt-2 flex items-center gap-2">
            <button className="rounded-chip bg-clear/20 px-3 py-1 text-clear" onClick={() => act("open")}>Open</button>
            <button className="rounded-chip bg-sev2/20 px-3 py-1 text-sev2" onClick={() => act("close")}>Close</button>
            <button className="rounded-chip bg-nline px-3 py-1 text-ndim" onClick={() => act("reset")}>Reset</button>
          </div>
        )}
        {msg && <span role="alert" className="text-sev2">{msg}</span>}
        <a className="mt-2 inline-block text-ndim underline" href="/?demo=loaded">Replay fallback</a>
      </details>
    </footer>
  );

  return (
    <SurgeBoardView
      state={state} joinUrl={joinUrl} stale={stale} controls={controls}
      notice={mode === "live" ? undefined : <SurgeModeNotice mode={mode} />}
    />
  );
}
