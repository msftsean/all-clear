import React from "react";
import type { DemoClearBoard, DemoClearBoardIncident, PipelineResult, Severity } from "./types";
import { Card, Eyebrow, MonoPill, SeverityBadge } from "./components";

const MODEL = "gpt-5.1";

function pct(n: number): string {
  return `${Math.round(n * 100)}%`;
}

// --- Deterministic geometry helpers --------------------------------------
// The map is intentionally tile-free (offline, no network dependency) but it
// must not look hardcoded: the street outline is *derived* from the location
// string (stable per place, distinct between places) and the markers are
// driven by the pipeline's real dedup signal (routing.magnitude), so repeat
// reports at the same incident visibly accumulate instead of being faked.
function hashStr(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function mulberry32(seed: number): () => number {
  let a = seed || 1;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Stylized "street" polylines seeded by the location — same place renders the
// same outline every time, different places look different.
function streetPaths(seedKey: string): string[] {
  const rng = mulberry32(hashStr(seedKey + "|streets"));
  const paths: string[] = [];
  for (let i = 0; i < 3; i++) {
    const y = 18 + rng() * 110;
    const y2 = y + (rng() - 0.5) * 46;
    const ymid = (y + y2) / 2 + (rng() - 0.5) * 34;
    paths.push(`M0 ${y.toFixed(0)} Q160 ${ymid.toFixed(0)} 320 ${y2.toFixed(0)}`);
  }
  for (let i = 0; i < 2; i++) {
    const x = 36 + rng() * 248;
    const x2 = x + (rng() - 0.5) * 64;
    const xmid = (x + x2) / 2 + (rng() - 0.5) * 30;
    paths.push(`M${x.toFixed(0)} 0 Q${xmid.toFixed(0)} 75 ${x2.toFixed(0)} 150`);
  }
  return paths;
}

const clamp = (v: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, v));

// One marker per report, clustered around a location-seeded epicenter. Earlier
// markers are positionally stable as the count grows (new reports append).
function clusterPoints(
  seedKey: string,
  count: number,
): { x: number; y: number }[] {
  const epi = mulberry32(hashStr(seedKey + "|epicenter"));
  const cx = 70 + epi() * 180; // 70..250
  const cy = 42 + epi() * 64; // 42..106
  const rng = mulberry32(hashStr(seedKey + "|spread"));
  const pts: { x: number; y: number }[] = [];
  for (let k = 0; k < count; k++) {
    const ang = rng() * Math.PI * 2;
    const jit = rng();
    const radius = k === 0 ? 0 : 7 + Math.sqrt(k) * 7 * (0.55 + jit * 0.7);
    pts.push({
      x: clamp(cx + Math.cos(ang) * radius, 12, 308),
      y: clamp(cy + Math.sin(ang) * radius, 12, 138),
    });
  }
  return pts;
}

// ---------------------------------------------------------------------------
// Incident card
// ---------------------------------------------------------------------------
function IncidentCard({
  r,
  onOpenReceipt,
}: {
  r: PipelineResult;
  onOpenReceipt: () => void;
}) {
  const a = r.action;
  const rd = r.routing;
  const attached = rd.outcome === "ATTACH_TO_INCIDENT";
  return (
    <Card title={`incident ${a.incident_id}`} testid="incident-card" span>
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <SeverityBadge sev={a.severity} />
            <span className="font-mono text-[11px] text-ndim">{a.queue}</span>
          </div>
          <div className="mt-2 font-sans text-[15px] font-medium text-nink">
            {a.escalated ? "Escalated to a human" : attached ? "Attached to open incident" : "Incident opened"}
          </div>
          <div className="mt-1 text-[12px] text-ndim">{a.estimated_response_time}</div>
        </div>
        <div className="flex flex-col items-end gap-1.5">
          <MonoPill testid="sla-pill">SLA {rd.sla_minutes}m</MonoPill>
          {rd.escalate && rd.escalation_reason ? (
            <MonoPill tone="voice" title="Escalation reason">
              {rd.escalation_reason}
            </MonoPill>
          ) : null}
          {attached && rd.dedup_similarity != null ? (
            <MonoPill title="Dedup cosine similarity">
              sim {rd.dedup_similarity.toFixed(3)}
            </MonoPill>
          ) : null}
        </div>
      </div>
      <button
        data-testid="open-receipt"
        onClick={onOpenReceipt}
        className="mt-3 w-full rounded-chip border border-nline/80 bg-night/20 px-3 py-1.5 text-[12px] text-nink shadow-dark-glass transition-colors hover:bg-night/40"
      >
        Show decision receipt
      </button>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Classification card
// ---------------------------------------------------------------------------
function ClassificationCard({ r }: { r: PipelineResult }) {
  const c = r.classification;
  const ents = c.entities || {};
  return (
    <Card title="classification" testid="classification-card">
      <div className="flex flex-wrap items-center gap-1.5">
        <MonoPill testid="intent-pill">{c.intent_category}</MonoPill>
        <MonoPill title="QueryAgent confidence">conf {pct(c.confidence)}</MonoPill>
        <MonoPill>{c.sentiment}</MonoPill>
        {c.pii_detected ? (
          <MonoPill tone="voice" testid="pii-pill" title="PII detected & redacted">
            pii: {c.pii_types.join(", ") || "yes"}
          </MonoPill>
        ) : null}
      </div>
      <dl className="mt-3 space-y-1.5 text-[12px]">
        {ents.location ? (
          <div className="flex gap-2">
            <dt className="w-16 text-ndim">location</dt>
            <dd className="text-nink">{ents.location}</dd>
          </div>
        ) : null}
        {ents.system ? (
          <div className="flex gap-2">
            <dt className="w-16 text-ndim">system</dt>
            <dd className="text-nink">{ents.system}</dd>
          </div>
        ) : null}
        {ents.severity_indicators && ents.severity_indicators.length ? (
          <div className="flex gap-2">
            <dt className="w-16 text-ndim">cues</dt>
            <dd className="flex flex-wrap gap-1">
              {ents.severity_indicators.map((s, i) => (
                <MonoPill key={i}>{s}</MonoPill>
              ))}
            </dd>
          </div>
        ) : null}
      </dl>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Map card — offline, location-derived outline with magnitude-driven cluster
// ---------------------------------------------------------------------------
function MapCard({ r, locationReports = 1 }: { r: PipelineResult; locationReports?: number }) {
  const loc = r.classification.entities?.location || "Location not specified";
  const hasLoc = Boolean(r.classification.entities?.location);
  const sevVar = `var(--${r.action.severity.toLowerCase()})`;
  // Visible cluster reflects the most corroboration we can see: the server's
  // dedup magnitude OR the number of reports about this place this session.
  const magnitude = Math.max(1, r.routing.magnitude || 1, locationReports || 1);

  // Seed off the location so the same place keeps a stable map and the cluster
  // grows around one epicenter; fall back to the incident id when unknown.
  const seedKey = hasLoc ? loc.trim().toLowerCase() : r.action.incident_id;
  const streets = React.useMemo(() => streetPaths(seedKey), [seedKey]);
  const MAX_DOTS = 14;
  const shown = Math.min(magnitude, MAX_DOTS);
  const points = React.useMemo(
    () => clusterPoints(seedKey, shown),
    [seedKey, shown],
  );

  return (
    <Card title="map" testid="map-card">
      <div className="relative overflow-hidden rounded-[16px] border border-nline bg-night shadow-dark-glass">
        <svg
          viewBox="0 0 320 150"
          className="h-[150px] w-full"
          role="img"
          aria-label={`Map: ${loc} — ${magnitude} report${magnitude === 1 ? "" : "s"}`}
        >
          <rect width="320" height="150" fill="#070b1a" />
          {/* faint reference grid */}
          {Array.from({ length: 7 }).map((_, i) => (
            <line key={`h${i}`} x1="0" y1={i * 22 + 8} x2="320" y2={i * 22 + 8} stroke="#1c2447" strokeWidth="1" />
          ))}
          {Array.from({ length: 11 }).map((_, i) => (
            <line key={`v${i}`} x1={i * 30 + 6} y1="0" x2={i * 30 + 6} y2="150" stroke="#1c2447" strokeWidth="1" />
          ))}
          {/* location-derived streets */}
          {streets.map((d, i) => (
            <path
              key={`s${i}`}
              d={d}
              fill="none"
              stroke="#7b5cff"
              strokeWidth={i < 3 ? 2 : 1.4}
              strokeLinecap="round"
              opacity={i < 3 ? 0.4 : 0.28}
            />
          ))}
          {/* accumulated report markers (oldest first, newest pulses) */}
          {hasLoc &&
            points.map((p, i) => {
              const isNewest = i === points.length - 1;
              return (
                <g key={`m${i}`}>
                  <circle cx={p.x} cy={p.y} r={isNewest ? 13 : 9} fill={sevVar} opacity={isNewest ? 0.18 : 0.1} />
                  <circle cx={p.x} cy={p.y} r={isNewest ? 4.5 : 3.5} fill={sevVar} opacity={isNewest ? 1 : 0.8}>
                    {isNewest ? (
                      <>
                        <animate attributeName="r" values="4.5;7;4.5" dur="1.8s" repeatCount="indefinite" />
                        <animate attributeName="opacity" values="1;0.45;1" dur="1.8s" repeatCount="indefinite" />
                      </>
                    ) : null}
                  </circle>
                </g>
              );
            })}
        </svg>
        {/* magnitude badge */}
        {magnitude > 1 ? (
          <div
            data-testid="map-magnitude"
            className="absolute right-2 top-2 rounded-tag border border-nline/80 bg-night/70 px-2 py-0.5 font-mono text-[10px] text-nink backdrop-blur"
          >
            ×{magnitude} report{magnitude === 1 ? "" : "s"}
          </div>
        ) : null}
        <div className="absolute bottom-2 left-2 right-2">
          <span className="font-mono text-[11px] text-nink">{loc}</span>
        </div>
      </div>
      <div data-testid="map-caption" className="mt-2 eyebrow text-ndim/70">
        {!hasLoc
          ? "offline outline · no location given"
          : magnitude > 1
          ? `offline outline · ${magnitude} reports clustered near ${loc}`
          : `offline outline · 1 report · awaiting corroboration`}
      </div>
    </Card>
  );
}

function severityVar(sev: Severity): string {
  return `var(--${sev.toLowerCase()})`;
}

function countsForSignals(board: DemoClearBoard, signalsReceived?: number): number[] {
  if (signalsReceived == null) return board.incidents.map((i) => i.report_count);
  const received = clamp(Math.floor(signalsReceived), 0, board.total_signals);
  const raw = board.incidents.map((incident) => (received * incident.report_count) / board.total_signals);
  const counts = raw.map((n, i) => Math.min(board.incidents[i].report_count, Math.floor(n)));
  let remainder = received - counts.reduce((sum, n) => sum + n, 0);
  const order = raw
    .map((n, i) => ({ i, frac: n - Math.floor(n) }))
    .sort((a, b) => b.frac - a.frac);
  for (const { i } of order) {
    if (remainder <= 0) break;
    if (counts[i] < board.incidents[i].report_count) {
      counts[i] += 1;
      remainder -= 1;
    }
  }
  return counts;
}

function boardAtSignalCount(board: DemoClearBoard, signalsReceived?: number): DemoClearBoard {
  if (signalsReceived == null) return board;
  const counts = countsForSignals(board, signalsReceived);
  return {
    ...board,
    total_signals: Math.min(Math.floor(signalsReceived), board.total_signals),
    incidents: board.incidents
      .map((incident, i) => ({ ...incident, report_count: counts[i] }))
      .filter((incident) => incident.report_count > 0),
  };
}

function CompactClusterMap({ incidents }: { incidents: DemoClearBoardIncident[] }) {
  return (
    <Card title="ClearBoard · pins merge on dedup" testid="hero-map-card" span>
      <div className="relative overflow-hidden rounded-[16px] border border-nline bg-night shadow-dark-glass">
        <svg
          viewBox="0 0 320 170"
          className="h-[170px] w-full"
          role="img"
          aria-label={`${incidents.length} incident clusters on the ClearBoard map`}
        >
          <rect width="320" height="170" fill="#070b1a" />
          {Array.from({ length: 8 }).map((_, i) => (
            <line key={`h${i}`} x1="0" y1={i * 22 + 8} x2="320" y2={i * 22 + 8} stroke="#1c2447" strokeWidth="1" />
          ))}
          {Array.from({ length: 11 }).map((_, i) => (
            <line key={`v${i}`} x1={i * 30 + 6} y1="0" x2={i * 30 + 6} y2="170" stroke="#1c2447" strokeWidth="1" />
          ))}
          {incidents.flatMap((incident, incidentIndex) =>
            streetPaths(incident.location).map((d, i) => (
              <path
                key={`${incident.incident_id}-s${i}`}
                d={d}
                transform={`translate(0 ${incidentIndex * 8})`}
                fill="none"
                stroke="#7b5cff"
                strokeWidth={i < 3 ? 1.8 : 1.2}
                strokeLinecap="round"
                opacity={0.16}
              />
            )),
          )}
          {incidents.map((incident) => {
            const points = clusterPoints(incident.location, Math.min(incident.report_count, 18));
            const color = severityVar(incident.severity);
            const anchor = points[0] || { x: 160, y: 75 };
            const pinRadius = 9 + Math.min(26, Math.sqrt(incident.report_count) * 1.25);
            return (
              <g key={incident.incident_id}>
                {points.map((p, i) => (
                  <circle
                    key={`${incident.incident_id}-p${i}`}
                    cx={p.x}
                    cy={p.y + 10}
                    r={i === points.length - 1 ? 5.2 : 3.4}
                    fill={color}
                    opacity={i === points.length - 1 ? 1 : 0.62}
                  />
                ))}
                <circle cx={anchor.x} cy={anchor.y + 10} r={pinRadius} fill={color} opacity="0.16" />
                <circle cx={anchor.x} cy={anchor.y + 10} r="7" fill={color} opacity="0.95" />
                <text
                  x={anchor.x}
                  y={anchor.y + 13}
                  textAnchor="middle"
                  className="fill-white font-mono text-[8px]"
                >
                  {incident.report_count}
                </text>
              </g>
            );
          })}
        </svg>
        <div className="absolute bottom-2 left-2 right-2 flex flex-wrap gap-1.5">
          {incidents.map((incident) => (
            <span
              key={incident.incident_id}
              className="rounded-tag border border-nline/80 bg-night/70 px-2 py-0.5 font-mono text-[10px] text-nink backdrop-blur"
            >
              {incident.location} · Magnitude {incident.report_count}
            </span>
          ))}
        </div>
      </div>
      <div className="mt-2 eyebrow text-ndim/70">
        ClearBoard map · inbound Signals become Reports; duplicate pins merge into weighted Incident pins
      </div>
    </Card>
  );
}

function HeroRatioCard({
  board,
  finalSignals,
  finalIncidents,
}: {
  board: DemoClearBoard;
  finalSignals: number;
  finalIncidents: number;
}) {
  const incidentCount = board.incidents.length;
  const duplicateSignals = Math.max(0, board.total_signals - incidentCount);
  const progress = finalSignals ? Math.min(100, (board.total_signals / finalSignals) * 100) : 0;
  return (
    <Card title="Surge · triage by deduplication" testid="hero-ratio-card" span accent="text-clear">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="font-display text-[36px] font-medium leading-none tracking-tight text-nink" aria-label={`${board.total_signals} Signals to ${incidentCount} Incidents`}>
            {board.total_signals.toLocaleString()} SIGNALS
            <span className="mx-3 text-clear">→</span>
            {incidentCount} INCIDENTS
          </div>
          <p className="mt-2 text-[13px] text-ndim">
            {board.subhead} Final target: {finalSignals.toLocaleString()} Signals → {finalIncidents} Incidents.
          </p>
          <div className="mt-3 h-2 overflow-hidden rounded-full border border-nline bg-night">
            <div className="h-full bg-clear transition-all duration-100" style={{ width: `${progress}%` }} />
          </div>
        </div>
        <div className="rounded-card border border-clear/30 bg-clear/10 px-4 py-3 text-right">
          <div className="font-mono text-[24px] text-clear">{duplicateSignals.toLocaleString()}</div>
          <div className="eyebrow text-clear/80">Signals attached as Reports</div>
          <div className="mt-1 font-mono text-[10px] text-clear/70">0 Signals discarded</div>
        </div>
      </div>
    </Card>
  );
}

function HeroIncidentCard({ incident }: { incident: DemoClearBoardIncident }) {
  return (
    <Card title={`incident ${incident.incident_id}`} testid="hero-incident-card">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <SeverityBadge sev={incident.severity} />
            <span className="font-mono text-[11px] text-ndim">Queue: {incident.queue}</span>
          </div>
          <div className="mt-2 font-sans text-[15px] font-medium text-nink">{incident.title}</div>
          <div className="mt-1 text-[12px] text-ndim">{incident.location}</div>
        </div>
        <div className="text-right">
          <div className="font-mono text-[28px] leading-none text-clear">
            {incident.report_count.toLocaleString()}
          </div>
          <div className="eyebrow text-clear/80">Magnitude · Reports</div>
        </div>
      </div>
      <p className="mt-3 text-[12px] text-nink">{incident.summary}</p>
      <div className="mt-3 flex flex-wrap gap-1.5">
        <MonoPill>{incident.status}</MonoPill>
        <MonoPill>SLA {incident.sla_minutes}m</MonoPill>
        <MonoPill>sim {incident.dedup_similarity.toFixed(2)}</MonoPill>
        <MonoPill>Sitrep ready</MonoPill>
      </div>
    </Card>
  );
}

function HeroClearBoard({ board, signalsReceived }: { board: DemoClearBoard; signalsReceived?: number }) {
  const projected = boardAtSignalCount(board, signalsReceived);
  const finalIncidentCount = board.incidents.length;
  return (
    <div data-testid="hero-clearboard" className="grid grid-cols-2 gap-[14px] p-5">
      <HeroRatioCard board={projected} finalSignals={board.total_signals} finalIncidents={finalIncidentCount} />
      <CompactClusterMap incidents={projected.incidents} />
      {projected.incidents.map((incident) => (
        <HeroIncidentCard key={incident.incident_id} incident={incident} />
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Decision receipt slide-over (DESIGN signature #3)
// ---------------------------------------------------------------------------
export function DecisionReceipt({
  r,
  published,
  onApprove,
  onClose,
}: {
  r: PipelineResult;
  published: boolean;
  onApprove: () => void;
  onClose: () => void;
}) {
  const c = r.classification;
  const rd = r.routing;
  const a = r.action;
  const Row = ({
    who,
    engine,
    children,
  }: {
    who: string;
    engine: string;
    children: React.ReactNode;
  }) => (
    <div className="border-b border-dashed border-nline py-3">
      <div className="flex items-center justify-between">
        <span className="font-display text-[13px] text-nink">{who}</span>
        <MonoPill tone={engine.includes("deterministic") ? "default" : "default"}>{engine}</MonoPill>
      </div>
      <div className="mt-2 space-y-1.5">{children}</div>
    </div>
  );

  return (
    <div className="fixed inset-0 z-40" data-testid="decision-receipt">
      <div className="absolute inset-0 bg-night/70 backdrop-blur-sm" onClick={onClose} />
      <aside className="absolute right-0 top-0 h-full w-full max-w-[440px] overflow-y-auto border-l border-nline/80 bg-panel/95 p-5 shadow-dark-glass backdrop-blur">
        <div className="flex items-center justify-between">
          <div>
            <Eyebrow>decision receipt</Eyebrow>
            <div className="mt-1 font-display text-[22px] font-medium tracking-tight text-nink">{a.incident_id}</div>
          </div>
          <button
            data-testid="receipt-close"
            onClick={onClose}
            className="rounded-chip border border-nline bg-night/20 px-3 py-1.5 text-[12px] text-ndim shadow-dark-glass hover:bg-night/50"
          >
            Close
          </button>
        </div>

        <div className="mt-3">
          <Row who="QueryAgent" engine={`model · ${MODEL}`}>
            <div className="flex flex-wrap gap-1.5">
              <MonoPill>{c.intent_category}</MonoPill>
              <MonoPill>conf {pct(c.confidence)}</MonoPill>
              {c.pii_detected ? <MonoPill tone="voice">pii redacted</MonoPill> : null}
            </div>
            <p className="text-[12px] text-ndim">Classified intent “{c.intent}”.</p>
          </Row>

          <Row who="RouterExecutor" engine="deterministic · no LLM">
            <div className="flex flex-wrap gap-1.5">
              <MonoPill>{rd.outcome}</MonoPill>
              <MonoPill>{rd.severity}</MonoPill>
              <MonoPill>SLA {rd.sla_minutes}m</MonoPill>
              {rd.dedup_similarity != null ? <MonoPill>sim {rd.dedup_similarity.toFixed(3)}</MonoPill> : null}
            </div>
            <div className="flex flex-wrap gap-1">
              {rd.routing_rules_applied.map((rule, i) => (
                <MonoPill key={i}>{rule}</MonoPill>
              ))}
            </div>
          </Row>

          <Row who="ActionAgent" engine={`model · ${MODEL}`}>
            <p className="text-[12px] text-nink">{a.user_message}</p>
            {a.citations.length ? (
              <div className="flex flex-wrap gap-1">
                {a.citations.map((cit, i) => (
                  <MonoPill key={i} title={cit.quote}>
                    [{cit.source_id}]
                  </MonoPill>
                ))}
              </div>
            ) : null}
          </Row>
        </div>

        {a.sitrep ? (
          <ApprovalGate r={r} published={published} onApprove={onApprove} />
        ) : null}
      </aside>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Approval gate (DESIGN signature #4) — the only --clear button
// ---------------------------------------------------------------------------
export function ApprovalGate({
  r,
  published,
  onApprove,
}: {
  r: PipelineResult;
  published: boolean;
  onApprove: () => void;
}) {
  const s = r.action.sitrep!;
  return (
    <div
      data-testid="approval-gate"
      className="mt-4 rounded-card border border-dashed border-nline bg-night/40 p-4"
    >
      <Eyebrow>{published ? "all clear · published" : "awaiting approval"}</Eyebrow>
      <p className="mt-2 text-[13px] text-nink">{s.summary}</p>
      {s.citations.length ? (
        <div className="mt-2 flex flex-wrap gap-1">
          {s.citations.map((c, i) => (
            <MonoPill key={i} title={c.quote}>
              [{c.source_id}]
            </MonoPill>
          ))}
        </div>
      ) : null}
      {published ? (
        <div className="mt-3 flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-clear" />
          <span className="font-mono text-[11px] text-clear">Published · undo within 15 minutes</span>
        </div>
      ) : (
        <>
          <p className="mt-3 text-[12px] text-ndim">
            It needs your approval before it goes out — that&apos;s the boundary, not a bug.
          </p>
          <button
            data-testid="approve-publish"
            onClick={onApprove}
            className="mt-3 w-full rounded-chip bg-clear px-5 py-2.5 font-sans text-[13px] font-semibold text-white shadow-[0_10px_26px_-6px_rgba(55,194,129,0.55)] transition hover:brightness-105"
          >
            Approve &amp; publish
          </button>
          <div className="mt-1 text-center eyebrow text-ndim/70">15-minute undo window</div>
        </>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Canvas grid
// ---------------------------------------------------------------------------
export function Canvas({
  result,
  onOpenReceipt,
  locationReports = 1,
  demoBoard,
  demoBlank = false,
  demoSignalsReceived,
}: {
  result: PipelineResult | null;
  onOpenReceipt: () => void;
  locationReports?: number;
  demoBoard?: DemoClearBoard | null;
  demoBlank?: boolean;
  demoSignalsReceived?: number;
}) {
  if (demoBoard) {
    return <HeroClearBoard board={demoBoard} signalsReceived={demoSignalsReceived} />;
  }
  if (!result || demoBlank) {
    return (
      <div
        data-testid="canvas-empty"
        className="flex h-full items-center justify-center p-8 text-center"
      >
        <div>
          <div className="mx-auto mb-3 h-px w-24 bg-nline" />
          <p className="font-display text-[40px] font-medium leading-tight tracking-tight text-nink">The board is quiet.</p>
          <p className="mt-1 text-[12px] text-ndim/70">
            {demoBlank
              ? "Demo blank state: a clean slate before the signal surge."
              : "Submit a signal on the left. Classification, routing, and the incident appear here."}
          </p>
        </div>
      </div>
    );
  }
  return (
    <div data-testid="canvas" className="grid grid-cols-2 gap-[14px] p-5">
      <IncidentCard r={result} onOpenReceipt={onOpenReceipt} />
      <ClassificationCard r={result} />
      <MapCard r={result} locationReports={locationReports} />
    </div>
  );
}
