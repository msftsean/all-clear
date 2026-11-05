import SectionHeader from './SectionHeader'
export default function StartCommandsSection() {
  return <section id="start-commands" className="scroll-mt-24 reveal reveal-delay-1"><SectionHeader icon="🚀" title="Start the Operations Lab" id="start-commands-heading" /><pre className="text-mercury-blue/80 text-xs mb-8">{`┌──────────────────────────────────────────────────────┐
│  🚀  START HERE — CHOOSE YOUR OPERATING PATH          │
├──────────────────────────────────────────────────────┤
│  A  ── 🧪  Local rehearsal with synthetic signals     │
│  B  ── ☁️  Hosted demo workspace                       │
│  C  ── 📞  Voice / phone intake drill                  │
└──────────────────────────────────────────────────────┘`}</pre><div className="grid md:grid-cols-3 gap-4 mb-6"><article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover"><h3 className="text-mercury-blue font-medium text-lg mb-3">🧪 Local rehearsal</h3><p className="text-silver text-sm mb-4">Use synthetic signals to rehearse grouping, severity, and operator handoff without paging anyone.</p><pre>{`npm install
npm run dev
# open the local ClearBoard
# inject the demo signal set`}</pre></article><article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover"><h3 className="text-mercury-blue font-medium text-lg mb-3">☁️ Hosted workspace</h3><p className="text-silver text-sm mb-4">Open the authenticated environment, confirm the board is current, then use the walkthrough below.</p><pre>{`# verify the host responds
curl -I https://demo.example/health
# confirm queues and SLA clocks
# do not paste customer payloads`}</pre></article><article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover"><h3 className="text-mercury-blue font-medium text-lg mb-3">📞 Voice / phone drill</h3><p className="text-silver text-sm mb-4">Test a caller transcript, callback consent, and the human escalation path before using a live line.</p><pre>{`# test microphone permissions
# place a synthetic call
# confirm transcript + handoff
# keep text intake available`}</pre></article></div><div className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover"><h3 className="text-mercury-blue font-medium text-lg mb-3">🩺 Readiness checks</h3><div className="space-y-3">{['Signal intake: email · webhook · chat · phone', 'Incident grouping: fingerprint + surge window', 'Queues: SEV1–SEV4 with SLA timers', 'Safety: human escalation, redaction, audit trail'].map((row) => <div key={row} className="flex items-center gap-3 text-sm"><span className="text-emerald-400">●</span><span className="text-silver">{row}</span></div>)}</div></div></section>
}
