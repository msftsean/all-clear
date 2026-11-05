import { Link } from 'react-router-dom';

const phases = [
  { time: '0–5m', block: 'Confirm the signal', owner: 'Triage lead', output: 'Evidence and scope recorded' },
  { time: '5–15m', block: 'Deduplicate & calibrate', owner: 'Incident engine', output: 'One incident, severity, queue' },
  { time: '15–30m', block: 'Acknowledge & contain', owner: 'Queue owner', output: 'First sitrep and safe action' },
  { time: '30–60m', block: 'Mitigate & coordinate', owner: 'Incident lead', output: 'Mitigation decision and update' },
  { time: 'Each hour', block: 'Reassess impact', owner: 'Incident lead', output: 'Adjusted severity or closure path' },
];

export default function RunOfShow() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <p className="font-mono text-sm uppercase tracking-[0.2em] text-gold">Operations cadence</p>
      <h1 className="mt-2 text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">The first-response shift plan</h1>
      <p className="max-w-2xl text-ink/75">This cadence protects attention during a surge: establish one shared record, meet the immediate SLA, then communicate with a reliable rhythm.</p>
      <div className="mt-8 bg-white rounded-2xl border border-deep-cream p-6 shadow-sm overflow-x-auto">
        <table className="w-full text-sm border-collapse"><thead><tr className="text-left text-maroon border-b-2 border-gold"><th className="py-2 pr-4 font-semibold">Window</th><th className="py-2 pr-4 font-semibold">Move</th><th className="py-2 pr-4 font-semibold">Owner</th><th className="py-2 font-semibold">Output</th></tr></thead>
          <tbody>{phases.map((phase) => <tr key={phase.time} className="border-b border-deep-cream last:border-0"><td className="py-3 pr-4 font-mono text-ink/70 whitespace-nowrap">{phase.time}</td><td className="py-3 pr-4 text-ink/90 font-medium">{phase.block}</td><td className="py-3 pr-4 text-ink/70">{phase.owner}</td><td className="py-3 text-ink/70">{phase.output}</td></tr>)}</tbody>
        </table>
      </div>
      <div className="mt-8 rounded-xl bg-deep-maroon p-6 text-cream"><h2 className="font-serif text-xl font-bold text-cream">ClearBoard rule</h2><p className="mt-2 text-cream/85">Every update answers: what is affected, who owns the response, what is happening now, and when will the board refresh?</p></div>
      <div className="text-center mt-8"><Link to="/" className="text-maroon hover:text-gold transition-colors font-medium">← Back to ClearBoard</Link></div>
    </div>
  );
}
