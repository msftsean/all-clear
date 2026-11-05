import CollapsibleNotes from '../components/CollapsibleNotes'
import DiagramSVG from '../components/DiagramSVG'

const stages = [
  {
    name: 'QueryAgent',
    role: 'Classify only',
    input: 'One raw signal',
    output: 'Intent, entities, severity indicators, PII flags',
  },
  {
    name: 'RouterExecutor',
    role: 'Decide deterministically',
    input: 'Classification + open incidents',
    output: 'Dedup outcome, severity, queue, SLA, escalation',
  },
  {
    name: 'ActionAgent',
    role: 'Act through three tools',
    input: 'RoutingDecision',
    output: 'Incident, knowledge response, or cited sitrep',
  },
]

export default function Pipeline() {
  return (
    <div role="tabpanel" id="pipeline-panel" aria-labelledby="pipeline-tab">
      <div className="max-w-5xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Three-stage architecture</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Model judgment stops before routing</h2>
        <p className="text-xl text-ink/70 mb-10">Classification can be probabilistic. Operational policy is code.</p>

        <DiagramSVG
          title="All Clear three-stage pipeline"
          description="A signal is classified by QueryAgent, routed deterministically by RouterExecutor, and acted on by ActionAgent."
          viewBox="0 0 900 260"
        >
          {stages.map((stage, index) => {
            const x = 45 + index * 290
            return (
              <g key={stage.name}>
                <rect x={x} y="80" width="220" height="100" rx="5" fill={index === 1 ? '#0F6CBD' : '#F7F8FA'} stroke="#1B1B1F" strokeWidth="2" />
                <text x={x + 110} y="122" textAnchor="middle" fontSize="16" fontWeight="bold" fill={index === 1 ? 'white' : '#1B1B1F'}>{stage.name}</text>
                <text x={x + 110} y="150" textAnchor="middle" fontSize="12" fill={index === 1 ? 'white' : '#666'}>{stage.role}</text>
                {index < 2 && <path d={`M ${x + 225} 130 L ${x + 280} 130`} stroke="#1B1B1F" strokeWidth="3" />}
              </g>
            )
          })}
        </DiagramSVG>

        <div className="grid md:grid-cols-3 gap-6 my-10">
          {stages.map((stage, index) => (
            <article className="card" key={stage.name}>
              <span className="mono-label text-ink/60">Stage {index + 1}</span>
              <h3 className="font-semibold text-xl my-2">{stage.name}</h3>
              <p className="font-semibold text-brand mb-3">{stage.role}</p>
              <p className="text-sm"><strong>Input:</strong> {stage.input}</p>
              <p className="text-sm mt-2"><strong>Output:</strong> {stage.output}</p>
            </article>
          ))}
        </div>

        <div className="card">
          <h3 className="font-semibold text-xl mb-4">ActionAgent tool inventory</h3>
          <div className="grid md:grid-cols-3 gap-3 font-mono text-sm">
            <code>create_incident</code>
            <code>search_knowledge</code>
            <code>generate_sitrep</code>
          </div>
        </div>

        <CollapsibleNotes>
          <p>Stress that RouterExecutor makes zero LLM calls. Dedup, severity, SLA, and escalation must be reproducible from the same inputs and rules.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
