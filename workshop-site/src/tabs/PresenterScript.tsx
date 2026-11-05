import CollapsibleNotes from '../components/CollapsibleNotes'

const beats = [
  {
    title: 'Open with the noise',
    script: '"An inbox shows how many messages arrived. An incident system shows what is actually happening. All Clear turns the first into the second without erasing any reporter."',
  },
  {
    title: 'Name the contract',
    script: '"A signal is what arrives. An incident is the real-world event. A report connects the two. Magnitude counts those reports and gives the event operational weight."',
  },
  {
    title: 'Draw the authority line',
    script: '"The model classifies. Code decides dedup, severity, queue, SLA, and escalation. The ActionAgent can use only three approved tools."',
  },
  {
    title: 'Explain the surge',
    script: '"Forty calls about one downed line are not forty incidents. They are forty preserved signals, forty reports, one incident, and magnitude forty."',
  },
  {
    title: 'Land on the board',
    script: '"ClearBoard is where the contract becomes visible: one event pin grows, its clock stays legible, its queue owns the work, and resolution moves the system toward all clear."',
  },
  {
    title: 'Close on trust',
    script: '"Trust is not that the system sounds confident. Trust is that the consequential decision is bounded, repeatable, inspectable, and safe under load."',
  },
]

export default function PresenterScript() {
  return (
    <div role="tabpanel" id="presenter-script-panel" aria-labelledby="presenter-script-tab">
      <div className="max-w-4xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Talk track</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Presenter script</h2>
        <p className="text-xl text-ink/70 mb-10">Six beats that keep the story anchored to the All Clear contract.</p>

        <div className="space-y-5">
          {beats.map((beat, index) => (
            <article className="card" key={beat.title}>
              <div className="flex gap-4">
                <span className="mono-label text-ink/60">0{index + 1}</span>
                <div>
                  <h3 className="font-semibold text-xl mb-3">{beat.title}</h3>
                  <blockquote className="border-l-2 border-brand pl-4 text-lg italic">{beat.script}</blockquote>
                </div>
              </div>
            </article>
          ))}
        </div>

        <CollapsibleNotes>
          <ul className="space-y-2">
            <li><strong>If the demo is slow:</strong> point to the decision receipt and continue the explanation.</li>
            <li><strong>If voice is unavailable:</strong> identify graceful degradation and use text.</li>
            <li><strong>If asked about AI routing:</strong> repeat that RouterExecutor makes zero LLM calls.</li>
            <li><strong>If asked what success means:</strong> every open incident resolved and every SLA obligation satisfied.</li>
          </ul>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
