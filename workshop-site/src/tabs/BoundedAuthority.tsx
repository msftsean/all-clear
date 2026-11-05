import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'

const boundaries = [
  ['QueryAgent', 'May classify a signal.', 'Cannot route, create records, or search.'],
  ['RouterExecutor', 'May apply dedup, severity, queue, SLA, and escalation rules.', 'Cannot create incidents or generate content.'],
  ['ActionAgent', 'May create incidents, search approved knowledge, and generate cited sitreps.', 'Cannot approve waivers, mutate unrelated records, or bypass escalation.'],
]

export default function BoundedAuthority() {
  return (
    <div role="tabpanel" id="authority-panel" aria-labelledby="authority-tab">
      <div className="max-w-5xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Least privilege by construction</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Authority lives in interfaces, not promises</h2>
        <p className="text-xl text-ink/70 mb-10">Every stage has a narrow role. If a capability is not exposed, an agent cannot invent it.</p>

        <div className="space-y-5 mb-10">
          {boundaries.map(([name, can, cannot]) => (
            <article className="card grid md:grid-cols-[180px_1fr_1fr] gap-4" key={name}>
              <h3 className="font-semibold text-xl">{name}</h3>
              <p><strong>Can:</strong> {can}</p>
              <p><strong>Cannot:</strong> {cannot}</p>
            </article>
          ))}
        </div>

        <CalloutCard variant="accent" title="Escalation is a safety control">
          Handoffs triggered by safety, PII exposure, sentiment, or protected escalation intents are mandatory. Weakening that path is not a harmless refactor.
        </CalloutCard>

        <div className="card mt-8">
          <h3 className="font-semibold text-xl mb-4">Decision receipt checklist</h3>
          <ul className="grid md:grid-cols-2 gap-3">
            {['Source signal ID', 'Classification and indicators', 'Dedup score and outcome', 'Severity rule applied', 'Queue and SLA', 'Escalation reason', 'Tool calls and results', 'PII-redaction status'].map((item) => (
              <li key={item} className="border-l-2 border-brand pl-3">{item}</li>
            ))}
          </ul>
        </div>

        <CollapsibleNotes>
          <p>Use the phrase "bounded authority means bounded blast radius." The model can propose within a role, but code owns consequential routing and tool access.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
