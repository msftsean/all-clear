import SectionHeader from './SectionHeader'

export default function OverviewSection() {
  return (
    <section id="overview" className="scroll-mt-24 reveal">
      <SectionHeader icon="🎯" title="Demo Overview" id="overview-heading" />
      <p className="text-silver text-lg leading-relaxed mb-6 max-w-3xl">
        The <strong className="text-starlight font-semibold">47 Doors Universal Front Door Support Agent</strong> now speaks. Students can click a single microphone button and have a natural spoken conversation with the same AI pipeline that powers text chat — getting ticket confirmations, knowledge article summaries, and escalation notices, all by voice. This demo shows how a university can replace dozens of disconnected support portals with <strong className="text-starlight font-semibold">one trusted digital colleague</strong> that works whether you type or talk.
      </p>
      <div className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover">
        <pre className="text-mercury-blue/80 text-xs leading-relaxed overflow-x-auto">{`┌─────────────────────────────────────────────────────────────┐
│  🎓 Student speaks  →  🧠 3-Agent Pipeline  →  🔊 AI replies │
│                                                             │
│  QueryAgent ──► RouterAgent ──► ActionAgent                 │
│      │               │               │                      │
│   🔍 Intent       🗺️ Route        🎫 Ticket                 │
│   Detection      Selection        Creation                  │
└─────────────────────────────────────────────────────────────┘`}</pre>
      </div>
    </section>
  )
}
