import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'
import DiagramSVG from '../components/DiagramSVG'

export default function SignalToIncident() {
  return (
    <div role="tabpanel" id="contract-panel" aria-labelledby="contract-tab">
      <div className="max-w-5xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Core domain contract</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Signal, incident, report, magnitude</h2>
        <p className="text-xl text-ink/70 mb-10">Four words prevent the most expensive category error in surge response.</p>

        <DiagramSVG
          title="Signals become reports on incidents"
          description="Each signal remains attributable while dedup associates related signals as reports on one incident."
          viewBox="0 0 900 320"
        >
          {[70, 150, 230].map((y, index) => (
            <g key={y}>
              <rect x="35" y={y - 24} width="150" height="48" rx="4" fill="#F7F8FA" stroke="#1B1B1F" strokeWidth="2" />
              <text x="110" y={y + 5} textAnchor="middle" fontSize="13" fill="#1B1B1F">Signal {index + 1}</text>
              <path d={`M 190 ${y} L 350 160`} stroke="#0F6CBD" strokeWidth="2" />
            </g>
          ))}
          <rect x="350" y="105" width="200" height="110" rx="6" fill="#0F6CBD" stroke="#1B1B1F" strokeWidth="3" />
          <text x="450" y="150" textAnchor="middle" fontSize="18" fill="white" fontWeight="bold">Incident AC-1042</text>
          <text x="450" y="178" textAnchor="middle" fontSize="13" fill="white">Magnitude 3</text>
          <path d="M 555 160 L 705 160" stroke="#1B1B1F" strokeWidth="2" />
          <rect x="710" y="120" width="155" height="80" rx="4" fill="#F7F8FA" stroke="#1B1B1F" strokeWidth="2" />
          <text x="787" y="150" textAnchor="middle" fontSize="13" fill="#1B1B1F" fontWeight="bold">Queue</text>
          <text x="787" y="175" textAnchor="middle" fontSize="12" fill="#1B1B1F">field-operations</text>
        </DiagramSVG>

        <div className="grid md:grid-cols-2 gap-6 my-10">
          {[
            ['Signal', 'One inbound communication on chat, browser voice, phone, or a submitted form. Never discarded.'],
            ['Incident', 'The underlying event. It owns the AC identifier, severity, queue, SLA clock, magnitude, and status.'],
            ['Report', 'The preserved association between a signal and an incident after dedup decides they describe the same event.'],
            ['Magnitude', 'The number of reports attached to an incident. It signals scale and controls visual weight on ClearBoard.'],
          ].map(([title, copy]) => (
            <article className="card" key={title}>
              <h3 className="font-semibold text-xl mb-2">{title}</h3>
              <p>{copy}</p>
            </article>
          ))}
        </div>

        <CalloutCard variant="accent" title="Never say a signal was merged away">
          The incident is deduplicated; the signal is preserved. Each caller or reporter remains attributable through a report.
        </CalloutCard>

        <CollapsibleNotes>
          <p>Use a downed power line as the example: forty calls are forty signals, one physical hazard is one incident, and the incident has forty reports and magnitude 40.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
