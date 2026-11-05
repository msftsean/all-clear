import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'

const levels = [
  { sev: 'SEV1', clock: '15 minutes', meaning: 'Life safety, total outage, or statutory clock', action: 'Immediate escalation' },
  { sev: 'SEV2', clock: '1 hour', meaning: 'Major impairment, public impact, or spreading event', action: 'Priority response' },
  { sev: 'SEV3', clock: '4 hours', meaning: 'Contained event with single-party impact', action: 'Standard response' },
  { sev: 'SEV4', clock: 'Next business day', meaning: 'Informational or routine request', action: 'Planned response' },
]

export default function SeveritySla() {
  return (
    <div role="tabpanel" id="severity-panel" aria-labelledby="severity-tab">
      <div className="max-w-5xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Deterministic service policy</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Severity starts the clock</h2>
        <p className="text-xl text-ink/70 mb-10">RouterExecutor maps observed indicators to a queue and response SLA. The model does not improvise urgency.</p>

        <div className="severity-strip mb-10" aria-label="Severity scale">
          {levels.map((level) => (
            <div className="severity-chip" key={level.sev}>
              <strong>{level.sev}</strong>
              <span className="text-sm">{level.clock}</span>
            </div>
          ))}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left p-4">Level</th>
                <th className="text-left p-4">Rule meaning</th>
                <th className="text-left p-4">Response SLA</th>
                <th className="text-left p-4">Operational action</th>
              </tr>
            </thead>
            <tbody>
              {levels.map((level) => (
                <tr key={level.sev}>
                  <td className="p-4 font-mono font-semibold">{level.sev}</td>
                  <td className="p-4">{level.meaning}</td>
                  <td className="p-4 font-semibold">{level.clock}</td>
                  <td className="p-4">{level.action}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <CalloutCard variant="accent" title="Statutory clocks override ordinary scoring">
          A legally mandated deadline forces SEV1 handling regardless of softer indicators. The rule is explicit, logged, and reviewable.
        </CalloutCard>

        <CollapsibleNotes>
          <p>Ask participants to separate impact from volume. A single life-safety signal can be SEV1 at magnitude 1; a high-magnitude informational event can remain SEV4.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
