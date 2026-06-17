import { useRef } from "react";
import { ChevronUpRegular, ChevronDownRegular } from "@fluentui/react-icons";

interface HeroBannerProps {
  onSectionSelect: (id: string) => void;
  activeSectionId: string;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

// Pre-computed star positions for a deterministic starfield
const STARS = Array.from({ length: 120 }, (_, i) => {
  // Deterministic pseudo-random using index
  const x = (i * 137.508 + 17) % 100;
  const y = (i * 97.3 + 31) % 100;
  const r = 0.5 + (i % 4) * 0.4;
  const delay = (i % 50) * 0.12;
  const duration = 2 + (i % 5) * 0.8;
  const opacity = 0.3 + (i % 7) * 0.1;
  return { x, y, r, delay, duration, opacity };
});

export default function HeroBanner({
  onSectionSelect,
  collapsed,
  onToggleCollapse,
}: HeroBannerProps) {
  const prefersReduced = useRef(
    typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  );

  // Collapsed: a slim night-sky strip that stays out of the way so the
  // active section is visible above the fold. Expandable on demand.
  if (collapsed) {
    return (
      <div
        className="relative overflow-hidden border-b border-white/10"
        style={{ background: "#2B2622" }}
      >
        <div
          className="absolute inset-0 pointer-events-none"
          aria-hidden="true"
          style={{
            background:
              "radial-gradient(ellipse 60% 120% at 50% 0%, rgba(178,91,52,0.18) 0%, transparent 70%)",
          }}
        />
        <div className="relative max-w-5xl mx-auto px-6 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 min-w-0">
            <span
              className="w-2 h-2 rounded-full bg-cofounder flex-shrink-0"
              aria-hidden="true"
            />
            <span className="font-serif text-white text-lg sm:text-xl truncate">
              47 Doors <span className="text-white/55">Coach Prep</span>
            </span>
          </div>
          <button
            type="button"
            onClick={onToggleCollapse}
            aria-expanded={false}
            className="flex-shrink-0 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-pill border border-white/20 bg-white/8 hover:bg-white/15 text-white/80 text-xs font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-night"
          >
            <ChevronDownRegular
              style={{ width: 16, height: 16 }}
              aria-hidden="true"
            />
            Expand intro
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      className="relative overflow-hidden"
      style={{ background: "#2B2622" }}
      aria-hidden={false}
    >
      {/* Atmospheric gradients */}
      <div
        className="absolute inset-0 pointer-events-none"
        aria-hidden="true"
        style={{
          background:
            "radial-gradient(ellipse 80% 60% at 50% 100%, rgba(178,91,52,0.20) 0%, transparent 70%), " +
            "radial-gradient(ellipse 60% 40% at 20% 80%, rgba(63,126,110,0.14) 0%, transparent 60%)",
        }}
      />

      {/* Starfield SVG */}
      {!prefersReduced.current && (
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none"
          aria-hidden="true"
          preserveAspectRatio="xMidYMid slice"
          viewBox="0 0 100 100"
          style={{ opacity: 0.9 }}
        >
          {STARS.map((s, i) => (
            <circle
              key={i}
              cx={s.x}
              cy={s.y}
              r={s.r * 0.18}
              fill="white"
              opacity={s.opacity}
              style={{
                animation: `twinkle ${s.duration}s ${s.delay}s ease-in-out infinite`,
              }}
            />
          ))}
        </svg>
      )}

      {/* City horizon glow */}
      <div
        className="absolute bottom-0 left-0 right-0 pointer-events-none"
        aria-hidden="true"
        style={{
          height: "80px",
          background:
            "linear-gradient(to top, rgba(178,91,52,0.14), transparent)",
        }}
      />

      {/* Subtle city silhouette */}
      <svg
        className="absolute bottom-0 left-0 right-0 w-full pointer-events-none"
        aria-hidden="true"
        viewBox="0 0 1440 80"
        preserveAspectRatio="none"
        style={{ opacity: 0.15 }}
      >
        <path
          d="M0,80 L0,60 L40,60 L40,40 L60,40 L60,30 L80,30 L80,40 L120,40 L120,50 L160,50 L160,35 L180,35 L180,25 L200,25 L200,35 L220,35 L220,45 L260,45 L260,30 L280,30 L280,20 L300,20 L300,30 L320,30 L320,50 L360,50 L360,38 L380,38 L380,28 L400,28 L400,38 L440,38 L440,52 L480,52 L480,40 L500,40 L500,32 L520,32 L520,40 L560,40 L560,55 L600,55 L600,42 L620,42 L620,30 L640,30 L640,20 L660,20 L660,30 L680,30 L680,42 L720,42 L720,50 L760,50 L760,38 L780,38 L780,28 L800,28 L800,38 L840,38 L840,55 L880,55 L880,44 L900,44 L900,32 L920,32 L920,44 L960,44 L960,52 L1000,52 L1000,40 L1020,40 L1020,30 L1040,30 L1040,40 L1080,40 L1080,50 L1120,50 L1120,38 L1140,38 L1140,28 L1160,28 L1160,38 L1200,38 L1200,55 L1240,55 L1240,44 L1260,44 L1260,35 L1280,35 L1280,44 L1320,44 L1320,60 L1360,60 L1360,48 L1400,48 L1400,60 L1440,60 L1440,80 Z"
          fill="rgba(178,91,52,1)"
        />
      </svg>

      {/* Collapse control */}
      <div className="relative max-w-5xl mx-auto px-6 pt-4 flex justify-end">
        <button
          type="button"
          onClick={onToggleCollapse}
          aria-expanded={true}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-pill border border-white/20 bg-white/8 hover:bg-white/15 text-white/75 text-xs font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-night"
        >
          <ChevronUpRegular
            style={{ width: 16, height: 16 }}
            aria-hidden="true"
          />
          Collapse intro
        </button>
      </div>

      {/* Hero content */}
      <div className="relative max-w-5xl mx-auto px-6 pb-16 pt-4 sm:pb-24">
        <div
          style={
            !prefersReduced.current
              ? {
                  animation: "fade-slide-up 0.9s ease-out forwards",
                  opacity: 0,
                }
              : {}
          }
        >
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/20 bg-white/8 mb-6">
            <span
              className="w-2 h-2 rounded-full bg-cofounder animate-pulse"
              aria-hidden="true"
            />
            <span className="text-white/70 text-xs font-medium tracking-wide uppercase">
              AJCU Hackathon · Coach Guide
            </span>
          </div>

          <h1 className="font-serif text-4xl sm:text-5xl md:text-6xl text-white leading-tight tracking-tight">
            47 Doors
            <br />
            <span className="text-white/60">Coach Prep</span>
          </h1>

          <p
            className="mt-4 text-white/55 text-base sm:text-lg max-w-lg leading-relaxed"
            style={
              !prefersReduced.current
                ? {
                    animation: "fade-slide-up 0.9s 0.2s ease-out forwards",
                    opacity: 0,
                  }
                : {}
            }
          >
            How to prepare for and help participants during the 47 Doors AJCU
            hackathon.
          </p>

          <button
            type="button"
            onClick={() => onSectionSelect("prepare")}
            className="mt-8 inline-flex items-center gap-2 px-6 py-3 rounded-pill bg-cofounder hover:bg-cofounder-dark text-white font-medium text-sm transition-all duration-200 shadow-elevated focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-night"
            style={
              !prefersReduced.current
                ? {
                    animation: "fade-slide-up 0.9s 0.4s ease-out forwards",
                    opacity: 0,
                  }
                : {}
            }
          >
            Start with Prepare →
          </button>
        </div>
      </div>
    </div>
  );
}
