import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'

const incidents = [
  { id: 'AC-1042', title: 'Downed line near Cedar Ave', sev: 'SEV1', queue: 'field-operations', magnitude: 18, sla: '08:42' },
  { id: 'AC-1045', title: 'Water pressure loss', sev: 'SEV2', queue: 'engineering', magnitude: 7, sla: '42:10' },
  { id: 'AC-1048', title: 'Billing portal notice', sev: 'SEV4', queue: 'customer-comms', magnitude: 2, sla: 'Next day' },
]

export default function ClearBoard() {
  return (
    <div role="tabpanel" id="clearboard-panel" aria-labelledby="clearboard-tab">
      <div className="max-w-5xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Shared operating picture</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">ClearBoard shows events, not inbox volume</h2>
        <p className="text-xl text-ink/70 mb-10">Pins gain visual weight as reports attach, breached SLA clocks stand out, and resolution moves the board toward all clear.</p>

        <div className="card mb-10">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-border pb-4 mb-5">
            <div>
              <p className="mono-label text-ink/60">Live incident view</p>
              <h3 className="text-2xl font-semibold">3 open incidents / magnitude 27</h3>
            </div>
            <span className="px-3 py-2 border border-red-200 bg-red-50 font-mono text-sm">1 SLA at risk</span>
          </div>
          <div className="space-y-3">
            {incidents.map((incident) => (
              <div className="grid grid-cols-[90px_1fr] md:grid-cols-[90px_1fr_150px_90px_90px] gap-3 items-center border border-border p-4" key={incident.id}>
                <strong className="font-mono">{incident.id}</strong>
                <span>{incident.title}</span>
                <span className="text-sm">{incident.queue}</span>
                <span className="font-mono font-semibold">{incident.sev}</span>
                <span className="font-mono">x{incident.magnitude} / {incident.sla}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <article className="card"><h3 className="font-semibold mb-2">Pins merge</h3><p>Dedup attaches new reports instead of creating duplicate incident markers.</p></article>
          <article className="card"><h3 className="font-semibold mb-2">Magnitude grows</h3><p>Visual weight reflects how many preserved reports describe the event.</p></article>
          <article className="card"><h3 className="font-semibold mb-2">Clocks surface risk</h3><p>Approaching or breached SLA deadlines become operationally prominent.</p></article>
        </div>

        <CalloutCard title="Terminal state">
          When every incident is resolved and every SLA obligation is satisfied, ClearBoard flips to the green all-clear state.
        </CalloutCard>

        <CollapsibleNotes>
          <p>ClearBoard is not an inbox. It is the live consequence of the domain model: incident identity, magnitude, severity, queue, status, and clock in one operating picture.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
