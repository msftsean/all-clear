import React from "react";
import type { PipelineResult } from "./types";
import { Card, Eyebrow, MonoPill, SeverityBadge } from "./components";

const MODEL = "gpt-5.1";

function pct(n: number): string {
  return `${Math.round(n * 100)}%`;
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
// Map card — GeoJSON-outline fallback (no external tiles, no network dep)
// ---------------------------------------------------------------------------
function MapCard({ r }: { r: PipelineResult }) {
  const loc = r.classification.entities?.location || "Location not specified";
  const sevVar = `var(--${r.action.severity.toLowerCase()})`;
  return (
    <Card title="map" testid="map-card">
      <div className="relative overflow-hidden rounded-[16px] border border-nline bg-night shadow-dark-glass">
        <svg viewBox="0 0 320 150" className="h-[150px] w-full" role="img" aria-label={`Map: ${loc}`}>
          <rect width="320" height="150" fill="#070b1a" />
          {Array.from({ length: 7 }).map((_, i) => (
            <line key={`h${i}`} x1="0" y1={i * 22 + 8} x2="320" y2={i * 22 + 8} stroke="#2a335f" strokeWidth="1" />
          ))}
          {Array.from({ length: 11 }).map((_, i) => (
            <line key={`v${i}`} x1={i * 30 + 6} y1="0" x2={i * 30 + 6} y2="150" stroke="#2a335f" strokeWidth="1" />
          ))}
          <path d="M0 96 L120 70 L210 92 L320 60" fill="none" stroke="#7b5cff" strokeWidth="2" opacity="0.6" />
          <g>
            <circle cx="166" cy="78" r="16" fill={sevVar} opacity="0.18" />
            <circle cx="166" cy="78" r="5" fill={sevVar} />
          </g>
        </svg>
        <div className="absolute bottom-2 left-2 right-2">
          <span className="font-mono text-[11px] text-nink">{loc}</span>
        </div>
      </div>
      <div className="mt-2 eyebrow text-ndim/70">offline outline · tiles unavailable</div>
    </Card>
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
}: {
  result: PipelineResult | null;
  onOpenReceipt: () => void;
}) {
  if (!result) {
    return (
      <div
        data-testid="canvas-empty"
        className="flex h-full items-center justify-center p-8 text-center"
      >
        <div>
          <div className="mx-auto mb-3 h-px w-24 bg-nline" />
          <p className="font-display text-[40px] font-medium leading-tight tracking-tight text-nink">The board is quiet.</p>
          <p className="mt-1 text-[12px] text-ndim/70">
            Submit a signal on the left. Classification, routing, and the incident appear here.
          </p>
        </div>
      </div>
    );
  }
  return (
    <div data-testid="canvas" className="grid grid-cols-2 gap-[14px] p-5">
      <IncidentCard r={result} onOpenReceipt={onOpenReceipt} />
      <ClassificationCard r={result} />
      <MapCard r={result} />
    </div>
  );
}
