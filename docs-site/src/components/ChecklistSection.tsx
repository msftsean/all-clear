import { useState } from 'react'
import SectionHeader from './SectionHeader'
const CHECKS = [
  { label: '🛰️ Signal sources exercised', detail: 'Webhook, email, chat, and phone intake have a known test signal.' },
  { label: '🧹 Dedup rules loaded', detail: 'Fingerprinting and surge windows are visible before the first incident is created.' },
  { label: '📋 ClearBoard reachable', detail: 'Queues, owners, severity, and SLA clocks render for the operator.' },
  { label: '🚦 Severity policy ready', detail: 'SEV1–SEV4 criteria and escalation contacts are current.' },
  { label: '📞 Voice / phone intake tested', detail: 'Transcript, caller context, consent, and callback path are available.' },
  { label: '🛡️ Safety controls visible', detail: 'Sensitive-content handling, human handoff, and audit trail are enabled.' },
  { label: '🔊 Notification path checked', detail: 'On-call route receives a test notification without paging a real escalation.' },
  { label: '🧭 Recovery story ready', detail: 'Acknowledge, mitigate, communicate, and close steps are rehearsed.' },
]
export default function ChecklistSection() {
  const [checked, setChecked] = useState<boolean[]>(new Array(CHECKS.length).fill(false))
  const done = checked.filter(Boolean).length; const pct = Math.round((done / CHECKS.length) * 100)
  const readiness = done === CHECKS.length ? ['bg-emerald-500', 'text-emerald-400', '🟢 Ready to demo!'] : done >= 4 ? ['bg-amber-500', 'text-amber-400', '🟡 Proceed with caution'] : ['bg-red-500', 'text-red-400', '🔴 Stop — fix issues first']
  return <section id="checklist" className="scroll-mt-24 reveal reveal-delay-1"><SectionHeader icon="✅" title="Pre-Demo Checklist" id="checklist-heading" /><p className="text-silver text-sm mb-6">⏰ Run through this list <strong className="text-starlight">5 minutes before</strong> the triage walkthrough.</p><div className="bg-midnight-slate border border-lead/50 rounded-2xl p-5 mb-6"><div className="flex items-center gap-4"><span className="text-xs text-silver font-mono min-w-32">Readiness</span><div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden"><div className={`h-full rounded-full progress-animate ${readiness[0]}`} style={{ width: `${pct}%` }} /></div><span className={`text-sm font-bold min-w-10 text-right ${readiness[1]}`}>{pct}%</span><span className="text-xs text-silver">{readiness[2]}</span></div></div><div className="bg-midnight-slate border border-lead/50 rounded-2xl overflow-hidden divide-y divide-lead/30">{CHECKS.map((check, index) => <label key={check.label} className="flex items-start gap-4 p-4 cursor-pointer hover:bg-interactive transition-colors group"><input type="checkbox" checked={checked[index]} onChange={() => setChecked((current) => current.map((value, i) => i === index ? !value : value))} className="mt-1 w-5 h-5 rounded accent-mercury-blue cursor-pointer flex-shrink-0" aria-label={check.label} /><div className="flex-1"><div className={`font-medium text-sm ${checked[index] ? 'text-emerald-400 line-through' : 'text-starlight'}`}>{index + 1}. {check.label}</div><div className="text-xs text-silver mt-0.5">{check.detail}</div></div></label>)}</div><blockquote className="mt-6 border-l-4 border-mercury-blue/50 pl-4 py-3 bg-mercury-blue/5 rounded-r-xl text-silver text-sm"><strong className="text-starlight">💡 Operator cue:</strong> Keep one clean test signal ready, one known surge example, and one safe voice/phone fallback. Never use live customer data in a rehearsal.</blockquote></section>
}
