import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'

const steps = [
  ['1', 'Inject the signal', '"There is a downed power line sparking beside the Cedar Avenue bus stop."'],
  ['2', 'Inspect classification', 'Confirm field hazard intent, location entity, life-safety indicators, and PII flags.'],
  ['3', 'Read the routing receipt', 'Verify SEV1, field-operations, 15-minute SLA, and mandatory escalation.'],
  ['4', 'Replay the surge', 'Submit nearby descriptions and watch ATTACH_TO_INCIDENT increment magnitude.'],
  ['5', 'Open ClearBoard', 'Confirm one incident pin, preserved report count, visible SLA clock, and escalation state.'],
  ['6', 'Generate the sitrep', 'Require citations for every factual claim; identify unsupported content if any.'],
]

export default function DemoWalkthrough() {
  return (
    <div role="tabpanel" id="demo-panel" aria-labelledby="demo-tab">
      <div className="max-w-4xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Facilitated demo</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Prove the contract, not the prose</h2>
        <p className="text-xl text-ink/70 mb-10">A strong demo exposes the decision receipt and visible system state at every step.</p>

        <div className="space-y-5">
          {steps.map(([number, title, copy]) => (
            <article className="card grid grid-cols-[48px_1fr] gap-4" key={number}>
              <div className="w-12 h-12 bg-brand text-white flex items-center justify-center font-mono font-bold">{number}</div>
              <div>
                <h3 className="font-semibold text-xl mb-2">{title}</h3>
                <p>{copy}</p>
              </div>
            </article>
          ))}
        </div>

        <CalloutCard variant="accent" title="Boundary test">
          Ask the system to suppress the escalation or downgrade the hazard. The correct result is refusal because routing rules and tool authority do not permit that action.
        </CalloutCard>

        <div className="card mt-8">
          <h3 className="font-semibold text-xl mb-4">Optional channel repeat</h3>
          <p>Submit the same event by browser voice or phone. The channel changes; the signal record, safety handling, routing rules, dedup outcome, and ClearBoard result do not.</p>
        </div>

        <CollapsibleNotes>
          <p>If a live dependency is unavailable, use mock mode and say so. Deterministic fixtures are a valid proof of decision behavior; pretending a degraded service is live is not.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
