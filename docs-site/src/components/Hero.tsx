import { ShieldCheckmarkRegular } from '@fluentui/react-icons'

export default function Hero() {
  return (
    <section className="relative min-h-[70vh] flex items-center justify-center overflow-hidden pt-16" aria-label="Hero">
      <div className="absolute inset-0 bg-deep-space"><div className="hero-starfield absolute inset-0 opacity-40" aria-hidden="true" /><div className="glow-a absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] rounded-full opacity-20 blur-3xl" style={{ background: 'radial-gradient(ellipse, #20c997 0%, transparent 70%)' }} aria-hidden="true" /><div className="glow-b absolute bottom-1/4 right-1/4 w-[300px] h-[300px] rounded-full opacity-10 blur-3xl" style={{ background: 'radial-gradient(ellipse, #f5b942 0%, transparent 70%)' }} aria-hidden="true" /></div>
      <div className="relative z-10 text-center px-6 max-w-4xl mx-auto">
        <div className="hero-enter hero-enter-delay-1 opacity-0"><div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-mercury-blue/30 bg-mercury-blue/10 text-mercury-blue text-sm font-medium mb-8"><ShieldCheckmarkRegular aria-hidden="true" /><span>Incident triage demo</span><span className="w-2 h-2 rounded-full bg-emerald-400" /><span className="text-emerald-400 font-semibold">OPS READY</span></div></div>
        <h1 className="hero-enter hero-enter-delay-2 opacity-0 text-5xl md:text-7xl font-light tracking-tight text-starlight mb-6 leading-none">All Clear<br /><span className="text-mercury-blue">Triage Companion</span></h1>
        <p className="hero-enter hero-enter-delay-3 opacity-0 text-xl md:text-2xl font-light text-silver max-w-2xl mx-auto mb-10 leading-relaxed">see the signal · shape the incident · restore service</p>
        <div className="hero-enter hero-enter-delay-4 opacity-0 flex flex-wrap justify-center gap-3 mb-12">{[{ icon: '🛰️', label: 'Audience', value: 'Incident commanders & responders' }, { icon: '📅', label: 'Edition', value: 'September 2026' }, { icon: '⏱️', label: 'Walkthrough', value: '10–12 min' }].map((badge) => <div key={badge.label} className="flex items-center gap-2 px-4 py-2 rounded-full border border-lead/50 bg-midnight-slate/60 text-sm text-silver"><span>{badge.icon}</span><span className="text-lead">{badge.label}:</span><span className="text-starlight font-medium">{badge.value}</span></div>)}</div>
        <div className="hero-enter hero-enter-delay-4 opacity-0 max-w-xl mx-auto bg-midnight-slate/80 border border-lead/50 rounded-2xl p-6 backdrop-blur-sm text-left space-y-4"><StatusBar label="Signal intake" pct={100} color="success" status="Email, webhook, chat, phone" /><StatusBar label="ClearBoard" pct={92} color="success" status="Queues and SLA timers visible" /><StatusBar label="Safety posture" pct={100} color="success" status="Human escalation and audit trail on" /></div>
        <div className="mt-12 flex flex-col items-center gap-2 text-lead text-sm" aria-hidden="true"><span>scroll to explore</span><div className="scroll-cue w-px h-8 bg-gradient-to-b from-lead to-transparent" /></div>
      </div>
    </section>
  )
}
function StatusBar({ label, pct, color, status }: { label: string; pct: number; color: 'success' | 'warning' | 'danger'; status: string }) {
  const colors = { success: { bar: 'bg-emerald-500', text: 'text-emerald-400' }, warning: { bar: 'bg-amber-500', text: 'text-amber-400' }, danger: { bar: 'bg-red-500', text: 'text-red-400' } }
  return <div className="flex items-center gap-3"><span className="text-xs text-silver min-w-32 font-mono">{label}</span><div className="flex-1 h-1.5 bg-white/5 rounded-full overflow-hidden"><div className={`h-full rounded-full progress-animate ${colors[color].bar}`} style={{ width: `${pct}%` }} /></div><span className={`text-xs font-bold min-w-10 text-right ${colors[color].text}`}>{pct}%</span><span className="text-xs text-lead hidden md:block">{status}</span></div>
}
