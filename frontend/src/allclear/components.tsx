import React from "react";
import type { Severity } from "./types";

// Literal class maps so Tailwind's purge keeps severity colors.
export const SEV: Record<
  Severity,
  { text: string; border: string; dot: string; soft: string }
> = {
  SEV1: { text: "text-sev1", border: "border-sev1", dot: "bg-sev1", soft: "bg-sev1/10" },
  SEV2: { text: "text-sev2", border: "border-sev2", dot: "bg-sev2", soft: "bg-sev2/10" },
  SEV3: { text: "text-sev3", border: "border-sev3", dot: "bg-sev3", soft: "bg-sev3/10" },
  SEV4: { text: "text-sev4", border: "border-sev4", dot: "bg-sev4", soft: "bg-sev4/10" },
};

export function Eyebrow({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <div className={`eyebrow text-ndim ${className}`}>{children}</div>;
}

// A mono pill for machine-produced facts (ids, scores, rules, citations).
export function MonoPill({
  children,
  tone = "default",
  title,
  testid,
}: {
  children: React.ReactNode;
  tone?: "default" | "clear" | "voice";
  title?: string;
  testid?: string;
}) {
  const tones: Record<string, string> = {
    default: "border-nline text-nink bg-night/40",
    clear: "border-clear/50 text-clear bg-clear/10",
    voice: "border-voice/50 text-voice bg-voice/10",
  };
  return (
    <span
      data-testid={testid}
      title={title}
      className={`inline-flex items-center gap-1 rounded-chip border px-1.5 py-0.5 font-mono text-[10px] ${tones[tone]}`}
    >
      {children}
    </span>
  );
}

export function SeverityBadge({ sev }: { sev: Severity }) {
  const s = SEV[sev];
  return (
    <span
      data-testid="severity-badge"
      className={`inline-flex items-center gap-1.5 rounded-chip border ${s.border} ${s.soft} px-2 py-0.5 font-mono text-[10px] ${s.text}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${s.dot}`} />
      {sev}
    </span>
  );
}

// Ambient live-audio waveform — the only looping motion (DESIGN). Voice orange.
export function Waveform({ live }: { live: boolean }) {
  const bars = [0.2, 0.45, 0.7, 0.95, 0.6, 0.85, 0.4, 0.65, 0.3];
  return (
    <div
      data-testid="waveform"
      aria-hidden="true"
      className="flex h-5 items-center gap-[3px]"
    >
      {bars.map((d, i) => (
        <span
          key={i}
          className={`w-[3px] rounded-full bg-voice ${live ? "animate-bar" : ""}`}
          style={{
            height: "100%",
            transformOrigin: "center",
            animationDelay: `${i * 90}ms`,
            transform: live ? undefined : "scaleY(0.4)",
          }}
        />
      ))}
    </div>
  );
}

// Night-world canvas card. Eyebrow carries title + provenance (DESIGN signature #2).
export function Card({
  title,
  provenance = "auto",
  accent,
  children,
  span = false,
  testid,
}: {
  title: string;
  provenance?: string;
  accent?: string;
  children: React.ReactNode;
  span?: boolean;
  testid?: string;
}) {
  return (
    <section
      data-testid={testid}
      className={`animate-rise rounded-card border border-nline bg-panel p-3.5 ${
        span ? "col-span-2" : ""
      }`}
    >
      <div className="mb-2.5 flex items-center justify-between">
        <Eyebrow className={accent}>{title}</Eyebrow>
        <span className="eyebrow text-ndim/70">pinned by: {provenance}</span>
      </div>
      {children}
    </section>
  );
}
