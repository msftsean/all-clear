import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'

const outcomes = [
  ['Name the objects', 'Distinguish the inbound signal, the real-world incident, and the report that links them.'],
  ['Explain the decision', 'Read severity, queue, SLA, escalation, and dedup outcomes as an auditable contract.'],
  ['Operate the surge', 'Use magnitude and ClearBoard to see many reports converge on fewer incidents.'],
]

export default function Overview() {
  return (
    <div role="tabpanel" id="overview-panel" aria-labelledby="overview-tab">
      <div className="max-w-4xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Workshop brief / 45 minutes</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Incident triage is a decision system</h2>
        <p className="text-xl text-ink/70 mb-10">
          All Clear preserves every incoming account, determines whether it describes a new or existing event, and gives operators a governed path from first signal to final resolution.
        </p>

        <CalloutCard title="The central idea">
          Many people can describe the same event. Preserve every signal, group reports around the correct incident, and let deterministic rules control operational consequences.
        </CalloutCard>

        <div className="grid md:grid-cols-3 gap-6 my-12">
          {outcomes.map(([title, description], index) => (
            <article className="card" key={title}>
              <span className="mono-label text-ink/60">0{index + 1}</span>
              <h3 className="font-semibold text-xl my-3 text-dark-text">{title}</h3>
              <p className="text-ink/75">{description}</p>
            </article>
          ))}
        </div>

        <div className="card">
          <h3 className="font-semibold text-xl mb-5 text-dark-text">The workshop arc</h3>
          <ol className="grid md:grid-cols-5 gap-4">
            {['Signal arrives', 'Classify', 'Route + dedup', 'Act safely', 'Reach all clear'].map((step, index) => (
              <li key={step} className="border-l-2 border-brand pl-3">
                <span className="mono-label text-ink/60">{index + 1}</span>
                <p className="font-semibold mt-1">{step}</p>
              </li>
            ))}
          </ol>
        </div>

        <CollapsibleNotes>
          <p>
            Open by separating observation from event. A chat thread, call, or submitted form is a signal. The outage, hazard, or compliance event it describes is the incident. That distinction makes dedup possible without deleting anyone's account.
          </p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
