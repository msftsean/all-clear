import type { ReactNode } from 'react'
import SectionHeader from './SectionHeader'

interface SceneProps {
  number: number
  icon: string
  title: string
  duration: string
  status: string
  tone?: 'green' | 'yellow'
  children: ReactNode
}

const nextPhaseRows = [
  { label: 'Phase 1–3', pct: 100, status: 'Complete — MVP voice path, Azure live endpoints, and demo runbook' },
  { label: 'Phase 4–6', pct: 60, status: 'In progress — reliability, analytics, and administrator confidence loops' },
  { label: 'Phase 7–8', pct: 0, status: 'Planned — production governance, deployment automation, and accessibility signoff' },
]

export default function DemoSequenceSection() {
  return (
    <section id="demo-sequence" className="scroll-mt-24 reveal reveal-delay-2">
      <SectionHeader icon="🎬" title="Demo Sequence" id="demo-sequence-heading" />
      <p className="text-silver mb-8">Five scenes, 12–15 minutes total. Keep the story tight: the institution has many doors, students need one trusted entry point, and voice makes the front door feel human.</p>
      <div className="space-y-6">
        <Scene number={1} icon="🚪" title="The 47 Doors Problem" duration="~3 min" status="Opening act — set the context">
          <TalkTrack>
            “Every campus has 47 different front doors: IT, financial aid, registrar, advising, housing, accessibility, student life. Students do not know which door to pick — they just know they need help. 47 Doors gives them one trusted digital colleague.”
          </TalkTrack>
          <ol className="space-y-3 mt-5">
            <Step n={1}>Open the chat experience and type <code>I forgot my password and can&apos;t log into Canvas</code>.</Step>
            <Step n={2}>Show the created ticket ID, matched knowledge-base articles, and expected SLA in the response.</Step>
            <Step n={3}>Point out that the student did not choose a department; the system inferred the right path.</Step>
          </ol>
          <pre className="text-mercury-blue/80 text-xs">{`Student types  ──►  🧠 Intent Detection  ──►  🗺️ Router  ──►  🎫 Ticket + 📚 KB + ⏱️ SLA`}</pre>
        </Scene>

        <Scene number={2} icon="🎤" title="Voice Interaction" duration="~4 min" status="The money shot">
          <TalkTrack>
            “Let me show you what it looks like when a student just wants to talk. There is no form, no department dropdown, no portal hunt — just a microphone and a natural conversation.”
          </TalkTrack>
          <ol className="space-y-3 mt-5">
            <Step n={1}>Point to the mic button: <em>“One button. That&apos;s the entire voice interface.”</em></Step>
            <Step n={2}>Click the mic; it pulses green and the status changes to <strong>Listening...</strong>.</Step>
            <Step n={3}>Speak: <code>I forgot my password and can&apos;t log into Canvas.</code></Step>
            <Step n={4}>While processing, call out the spinner and the same 3-agent pipeline running behind the scenes.</Step>
            <Step n={5}>When the agent responds, show the 🔊 audio response and matching transcript.</Step>
            <Step n={6}>Ask a follow-up: <code>Can you check the status of that ticket?</code></Step>
            <Step n={7}>Click the mic again to stop and emphasize that voice is a layer on the same support memory.</Step>
          </ol>
        </Scene>

        <Scene number={3} icon="🛰️" title="Observability & Trust" duration="~3 min" status="Build confidence for IT administrators">
          <TalkTrack>
            “EDU buyers need more than wow. They need operational evidence: health checks, logs, session IDs, and a way for IT to understand what happened after a student interaction.”
          </TalkTrack>
          <ol className="space-y-3 mt-5">
            <Step n={1}>Open a tab to <code>/api/realtime/health</code> and show <code>{'{ "realtime_available": true, "mock_mode": false, "voice_enabled": true }'}</code>.</Step>
            <Step n={2}>Navigate to <code>/api/health</code> and show the backend services: ticketing, knowledge base, and session store.</Step>
            <Step n={3}>Scroll through conversation history and point at logs containing <code>input_modality: voice</code>.</Step>
            <Step n={4}>Highlight the shared session ID across voice and text so support teams can trace the full journey.</Step>
          </ol>
        </Scene>

        <Scene number={4} icon="🛟" title="Graceful Degradation" duration="~2 min" status="Show resilience — builds institutional trust" tone="yellow">
          <TalkTrack>
            “Campuses need technology that fails gracefully. If a microphone, browser, or Realtime service has a bad day, the student still has a way forward.”
          </TalkTrack>
          <ol className="space-y-3 mt-5">
            <Step n={1}>Disable voice with the operational switch: <code>az containerapp update --set-env-vars VOICE_ENABLED=false</code>.</Step>
            <Step n={2}>Refresh the UI and show that the mic button is gone rather than broken.</Step>
            <Step n={3}>Type a normal support message and show that text chat still works.</Step>
            <Step n={4}>Re-enable voice with <code>az containerapp update --set-env-vars VOICE_ENABLED=true</code>.</Step>
          </ol>
        </Scene>

        <Scene number={5} icon="✨" title="What&apos;s Next" duration="~2 min" status="Close strong — leave them excited">
          <TalkTrack>
            “This is already a working front door. The roadmap is about making it enterprise-grade: accessibility, lower latency, governance, analytics, and an operations story that scales across any university.”
          </TalkTrack>
          <div className="space-y-4 mt-5 mb-6">
            {nextPhaseRows.map((row) => (
              <div key={row.label}>
                <div className="flex justify-between text-xs mb-1"><span className="text-silver font-mono">{row.label}</span><span className="text-starlight">{row.pct}%</span></div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden"><div className="h-full bg-mercury-blue rounded-full progress-animate" style={{ width: `${row.pct}%` }} /></div>
                <p className="text-xs text-silver mt-1">{row.status}</p>
              </div>
            ))}
          </div>
          <ol className="space-y-3 mt-5">
            <Step n={1}>Production hardening, including WCAG 2.1 AA verification and deployment guardrails.</Step>
            <Step n={2}>Accessibility hardening for keyboard, screen reader, captioning, and reduced-motion users.</Step>
            <Step n={3}>Sub-2-second latency target for spoken turn-taking.</Step>
            <Step n={4}>Analytics for volume, routing accuracy, escalation rate, and student-success trend spotting.</Step>
          </ol>
        </Scene>
      </div>
    </section>
  )
}

function Scene({ number, icon, title, duration, status, tone = 'green', children }: SceneProps) {
  const badge = tone === 'yellow' ? 'border-amber-500/40 text-amber-400 bg-amber-500/10' : 'border-emerald-500/40 text-emerald-400 bg-emerald-500/10'
  return (
    <article className="bg-midnight-slate border border-lead/50 border-l-[3px] border-l-mercury-blue rounded-2xl p-6 card-hover">
      <div className="flex flex-wrap items-start justify-between gap-4 mb-4">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-lead font-mono">Scene {number} · {duration}</p>
          <h3 className="text-2xl font-light text-starlight mt-1" style={{ fontWeight: 300 }}>{icon} {title}</h3>
        </div>
        <span className={`px-3 py-1 rounded-full border text-xs font-medium ${badge}`}>{status}</span>
      </div>
      {children}
    </article>
  )
}

function TalkTrack({ children }: { children: ReactNode }) {
  return <div className="italic text-silver bg-interactive/70 border border-lead/40 rounded-xl p-4">{children}</div>
}

function Step({ n, children }: { n: number, children: ReactNode }) {
  return (
    <li className="flex gap-3 text-silver">
      <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-mercury-blue text-white text-xs font-bold">{n}</span>
      <span>{children}</span>
    </li>
  )
}
