const agenda = [
  ['0:00-0:05', 'Frame the operating problem', 'Signals are not incidents.'],
  ['0:05-0:12', 'Teach the domain contract', 'Signal, report, incident, magnitude, queue.'],
  ['0:12-0:19', 'Trace the pipeline', 'QueryAgent, RouterExecutor, ActionAgent.'],
  ['0:19-0:25', 'Apply SEV and SLA', 'Deterministic rules, escalation, statutory clocks.'],
  ['0:25-0:32', 'Replay a surge', 'Attach reports, grow magnitude, keep latency flat.'],
  ['0:32-0:37', 'Inspect ClearBoard', 'Pins, clocks, queues, status, all-clear state.'],
  ['0:37-0:42', 'Run the exercise', 'Draft one signal, incident hypothesis, and boundary.'],
  ['0:42-0:45', 'Close', 'Name the evidence required for trust.'],
]

export default function RunOfShow() {
  return (
    <div role="tabpanel" id="run-of-show-panel" aria-labelledby="run-of-show-tab">
      <div className="max-w-4xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Facilitator timing</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">45-minute run of show</h2>
        <p className="text-xl text-ink/70 mb-10">Keep the room focused on decisions and evidence, not feature inventory.</p>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead><tr><th className="text-left p-4">Time</th><th className="text-left p-4">Block</th><th className="text-left p-4">Teaching point</th></tr></thead>
            <tbody>
              {agenda.map(([time, block, point]) => (
                <tr key={time}><td className="p-4 font-mono whitespace-nowrap">{time}</td><td className="p-4 font-semibold">{block}</td><td className="p-4">{point}</td></tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mt-8">
          <article className="card">
            <h3 className="font-semibold text-xl mb-3">Demo fallback</h3>
            <p>Use mock mode and the Demo Walkthrough tab. State the degraded dependency plainly and continue proving deterministic behavior.</p>
          </article>
          <article className="card">
            <h3 className="font-semibold text-xl mb-3">Do not skip</h3>
            <p>The report-versus-incident distinction, the SEV1 clock, the attach path, bounded tools, and the all-clear terminal state.</p>
          </article>
        </div>
      </div>
    </div>
  )
}
