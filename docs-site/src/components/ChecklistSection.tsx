import { useState } from 'react'
import SectionHeader from './SectionHeader'

const CHECKS = [
  { label: '🌐 Browser open', detail: 'Chrome 90+, Firefox 85+, or Edge 90+' },
  { label: '🎙️ Microphone tested', detail: 'Settings → Privacy → Microphone → Allow' },
  { label: '☁️ Azure Container App deployed', detail: 'azd up completed · /api/health returns healthy' },
  { label: '🖼️ Frontend reachable', detail: 'Container App URL loads the UI (or Vite dev if running locally)' },
  { label: '🔑 Azure subscription active', detail: 'az account show confirms sub ME-MngEnvMCAP262307-segayle-1 · azd auth login completed' },
  { label: '🤖 Azure OpenAI connected', detail: 'MOCK_MODE=false · live gpt-4.1 + gpt-realtime on frontdoor-6wfum6gndxawy-openai' },
  { label: '🔊 Audio output working', detail: 'System volume up · headset or speakers confirmed' },
  { label: '🛡️ Fallback ready', detail: 'If voice fails → text chat always works · stay calm' },
]

export default function ChecklistSection() {
  const [checked, setChecked] = useState<boolean[]>(new Array(CHECKS.length).fill(false))
  const toggle = (index: number) => {
    const next = [...checked]
    next[index] = !next[index]
    setChecked(next)
  }
  const done = checked.filter(Boolean).length
  const total = CHECKS.length
  const pct = Math.round((done / total) * 100)
  const readiness = done === total
    ? { bar: 'bg-emerald-500', text: 'text-emerald-400', status: '🟢 Ready to demo!' }
    : done >= 4
      ? { bar: 'bg-amber-500', text: 'text-amber-400', status: done >= 6 ? '🟡 Proceed with caution' : '🟡 Keep going...' }
      : { bar: 'bg-red-500', text: 'text-red-400', status: '🔴 Stop — fix issues first' }

  return (
    <section id="checklist" className="scroll-mt-24 reveal reveal-delay-1">
      <SectionHeader icon="✅" title="Pre-Demo Checklist" id="checklist-heading" />
      <p className="text-silver text-sm mb-6">⏰ Run through this list <strong className="text-starlight">5 minutes before</strong> you start the demo.</p>
      <div className="bg-midnight-slate border border-lead/50 rounded-2xl p-5 mb-6">
        <div className="flex items-center gap-4">
          <span className="text-xs text-silver font-mono min-w-32">Overall Readiness</span>
          <div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden">
            <div className={`h-full rounded-full progress-animate transition-all duration-700 ${readiness.bar}`} style={{ width: `${pct}%` }} />
          </div>
          <span className={`text-sm font-bold min-w-10 text-right ${readiness.text}`}>{pct}%</span>
          <span className="text-xs text-silver">{readiness.status}</span>
        </div>
      </div>
      <div className="bg-midnight-slate border border-lead/50 rounded-2xl overflow-hidden divide-y divide-lead/30">
        {CHECKS.map((check, index) => (
          <label key={check.label} className="flex items-start gap-4 p-4 cursor-pointer hover:bg-interactive transition-colors duration-200 group">
            <input type="checkbox" checked={checked[index]} onChange={() => toggle(index)} className="mt-1 w-5 h-5 rounded accent-mercury-blue cursor-pointer flex-shrink-0" aria-label={check.label} />
            <div className="flex-1">
              <div className={`font-medium text-sm transition-colors duration-200 ${checked[index] ? 'text-emerald-400 line-through decoration-emerald-600' : 'text-starlight'}`}>{index + 1}. {check.label}</div>
              <div className="text-xs text-silver mt-0.5">{check.detail}</div>
            </div>
          </label>
        ))}
      </div>
      <blockquote className="mt-6 border-l-4 border-mercury-blue/50 pl-4 py-3 bg-mercury-blue/5 rounded-r-xl text-silver text-sm">
        <strong className="text-starlight">💡 Codespaces?</strong> Leave <code>VITE_API_BASE_URL</code> blank — Vite proxies <code>/api</code> to <code>127.0.0.1:8000</code> automatically. Both port <strong className="text-starlight">5173</strong> and port <strong className="text-starlight">8000</strong> must be forwarded.
      </blockquote>
    </section>
  )
}
