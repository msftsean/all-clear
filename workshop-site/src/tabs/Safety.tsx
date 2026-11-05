import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'

const controls = [
  ['Intent-independent safety', 'Crisis and life-safety language triggers the safety path even when ordinary intent classification points elsewhere.'],
  ['PII discipline', 'Sensitive content is redacted before logs and responses; raw audio is not stored.'],
  ['Mandatory escalation', 'Protected conditions hand off to a human queue and cannot be weakened by a model response.'],
  ['Grounded sitreps', 'Situation reports cite source records so operators can verify every factual claim.'],
  ['Graceful degradation', 'Unavailable voice or phone channels are hidden or reported honestly while text remains usable.'],
  ['Auditability', 'Signals, reports, decisions, tool calls, and SLA changes remain traceable.'],
]

export default function Safety() {
  return (
    <div role="tabpanel" id="safety-panel" aria-labelledby="safety-tab">
      <div className="max-w-5xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Operational safety</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Safety is a runtime path</h2>
        <p className="text-xl text-ink/70 mb-10">Controls are useful only when they execute under pressure and leave evidence.</p>

        <div className="grid md:grid-cols-2 gap-6">
          {controls.map(([title, copy]) => (
            <article className="card" key={title}>
              <h3 className="font-semibold text-xl mb-3">{title}</h3>
              <p>{copy}</p>
            </article>
          ))}
        </div>

        <CalloutCard variant="accent" title="Escalation cannot be optimized away">
          Latency, cost, and convenience never justify skipping a required human handoff. Safety rules are part of the contract.
        </CalloutCard>

        <CollapsibleNotes>
          <p>Frame safety as observable behavior: what input triggered it, which rule fired, where the incident was routed, what was redacted, and what the operator sees next.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
