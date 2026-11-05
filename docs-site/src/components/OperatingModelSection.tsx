import SectionHeader from './SectionHeader'
const capabilities = [
  { capability: 'Understands signals', evidence: 'Normalizes reports from webhook, email, chat, and phone into context a responder can inspect.' },
  { capability: 'Reduces noise', evidence: 'Deduplicates repeats, detects surges, and preserves the evidence behind the grouping decision.' },
  { capability: 'Routes by impact', evidence: 'Maps SEV1–SEV4 to queues, owners, escalation paths, and measurable SLA clocks.' },
  { capability: 'Supports humans', evidence: 'ClearBoard keeps timeline, reports, voice transcripts, updates, and handoffs in one incident record.' },
  { capability: 'Protects safety', evidence: 'Sensitive signals pause automation, redact where needed, and route to a human reviewer with an audit trail.' },
]
export default function OperatingModelSection() {
  return <section id="operating-model" className="scroll-mt-24 reveal reveal-delay-3"><SectionHeader icon="🧭" title="Operating Model" id="operating-model-heading" /><div className="space-y-8"><article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover"><h3 className="text-mercury-blue font-medium text-lg mb-4">From noise to a shared picture</h3><p className="text-silver mb-4">All Clear is designed for the moments when an operations team is flooded with partial reports and still needs to act safely. The system narrows attention without pretending uncertainty is gone.</p><div className="grid md:grid-cols-2 gap-4"><div><p className="text-xs uppercase tracking-[.18em] text-lead font-mono mb-2">Before</p><pre className="text-xs text-silver">{`Signal stream
  ├─ duplicate alerts
  ├─ vague reports
  ├─ phone fragments
  ├─ rising volume
  └─ unclear ownership`}</pre></div><div><p className="text-xs uppercase tracking-[.18em] text-lead font-mono mb-2">After</p><pre className="text-xs text-mercury-blue/80">{`ClearBoard
  ├─ one incident
  ├─ evidence trail
  ├─ SEV + SLA
  ├─ named owner
  └─ safe next action`}</pre></div></div><blockquote className="mt-5 border-l-4 border-mercury-blue/50 pl-4 py-3 bg-mercury-blue/5 rounded-r-xl text-silver text-sm">“The win is not fewer alerts. It is fewer competing stories about what the team should do next.”</blockquote></article><article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover"><h3 className="text-mercury-blue font-medium text-lg mb-4">What to show in the demo</h3><div className="overflow-x-auto rounded-xl border border-lead/50"><table><thead><tr><th>Capability</th><th>Evidence</th></tr></thead><tbody>{capabilities.map((row) => <tr key={row.capability}><td className="font-medium text-starlight">{row.capability}</td><td className="text-silver">{row.evidence}</td></tr>)}</tbody></table></div></article><article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover"><h3 className="text-mercury-blue font-medium text-lg mb-4">The operator promise</h3><p className="text-silver mb-4">Use the smallest amount of automation that makes the next human decision clearer. Voice and phone intake are additional signal paths, not a replacement for written evidence or human judgment.</p><ul className="feature-list"><li><span className="text-mercury-blue">●</span><span>Dedup and surge grouping reduce noise without hiding a new impact.</span></li><li><span className="text-mercury-blue">●</span><span>SEV and SLA rules make urgency visible and ownership explicit.</span></li><li><span className="text-mercury-blue">●</span><span>Safety holds, redaction, and audit trails keep sensitive response work accountable.</span></li></ul><blockquote className="mt-5 border-l-4 border-mercury-blue/50 pl-4 py-3 bg-mercury-blue/5 rounded-r-xl text-silver text-sm">“ClearBoard gives the team one place to see the signal, name the incident, and choose the safest next move.”</blockquote></article></div></section>
}
