import SectionHeader from './SectionHeader'
export default function OverviewSection() {
  return <section id="overview" className="scroll-mt-24 reveal"><SectionHeader icon="🎯" title="Demo Overview" id="overview-heading" /><p className="text-silver text-lg leading-relaxed mb-6 max-w-3xl"><strong className="text-starlight font-semibold">All Clear</strong> turns noisy operational signals into a calm, shared incident picture. This companion demonstrates the path from email, webhook, chat, and phone intake to deduplication, surge grouping, severity assignment, SLA-aware queues, and a safe handoff to responders. The point is not another alert console; it is a reliable operating rhythm that helps a team decide what matters next.</p><div className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover"><pre className="text-mercury-blue/80 text-xs leading-relaxed overflow-x-auto">{`┌─────────────────────────────────────────────────────────────┐
│  📡 Signals arrive  →  🧠 Triage pipeline  →  🧭 ClearBoard │
│                                                             │
│  Normalize ──► Dedup + surge ──► Severity + queue          │
│      │               │               │                      │
│   🔍 Signal       🧱 Incident       ⏱️ SLA                   │
│   Context        Grouping          Response                 │
└─────────────────────────────────────────────────────────────┘`}</pre></div></section>
}
