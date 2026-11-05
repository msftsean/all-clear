import { useState } from 'react'
import CollapsibleNotes from '../components/CollapsibleNotes'

export default function WorkshopExercise() {
  const [signal, setSignal] = useState('')
  const [incident, setIncident] = useState('')
  const [boundary, setBoundary] = useState('')

  return (
    <div role="tabpanel" id="exercise-panel" aria-labelledby="exercise-tab">
      <div className="max-w-4xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Five-minute exercise</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Design one triage decision</h2>
        <p className="text-xl text-ink/70 mb-10">Write the incoming observation, name the event it may describe, then set one non-negotiable boundary.</p>

        <div className="space-y-6">
          <label className="card block">
            <span className="mono-label text-ink/60">1 / Signal</span>
            <span className="block font-semibold text-xl my-2">What arrives?</span>
            <input className="w-full px-4 py-3 border-2 border-border" value={signal} onChange={(event) => setSignal(event.target.value)} placeholder="Example: Smoke is coming from a utility cabinet on Pine Street." />
          </label>
          <label className="card block">
            <span className="mono-label text-ink/60">2 / Incident hypothesis</span>
            <span className="block font-semibold text-xl my-2">What may be happening?</span>
            <input className="w-full px-4 py-3 border-2 border-border" value={incident} onChange={(event) => setIncident(event.target.value)} placeholder="Example: Electrical equipment fire" />
          </label>
          <label className="card block">
            <span className="mono-label text-ink/60">3 / Boundary</span>
            <span className="block font-semibold text-xl my-2">What must automation never do?</span>
            <input className="w-full px-4 py-3 border-2 border-border" value={boundary} onChange={(event) => setBoundary(event.target.value)} placeholder="Example: Never suppress a life-safety escalation." />
          </label>
        </div>

        {(signal || incident || boundary) && (
          <div className="card mt-8 border-2 border-brand" aria-live="polite">
            <p className="mono-label text-ink/60 mb-3">Draft triage card</p>
            <dl className="space-y-3">
              <div><dt className="font-semibold">Signal</dt><dd>{signal || '[Describe the inbound observation]'}</dd></div>
              <div><dt className="font-semibold">Incident hypothesis</dt><dd>{incident || '[Name the underlying event]'}</dd></div>
              <div><dt className="font-semibold">Hard boundary</dt><dd>{boundary || '[State a prohibited action]'}</dd></div>
            </dl>
          </div>
        )}

        <CollapsibleNotes>
          <p>After participants share, ask which fields should be model-derived and which must be rule-derived. Severity, SLA, queue, dedup, and escalation belong in deterministic routing.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
