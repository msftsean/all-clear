import { Link } from 'react-router-dom';

const steps = [
  {
    number: '01',
    title: 'Capture the signal',
    body: 'Record the source, first-seen time, affected service or location, observed symptom, and any confidence limit. Keep the original signal linked to the record.',
  },
  {
    number: '02',
    title: 'Find the incident fingerprint',
    body: 'Compare the service, symptom, time window, and scope against active work. Attach matching signals to the existing incident; open a new one only when the evidence differs.',
  },
  {
    number: '03',
    title: 'Set severity and SLA',
    body: 'Use measured impact and immediacy. P1 starts a 15-minute acknowledgement target, P2 a 30-minute target, and P3 a four-hour observation target.',
  },
  {
    number: '04',
    title: 'Assign one response queue',
    body: 'Select the accountable lead queue, page its on-call owner, and list supporting teams only when they have a defined action. Ownership should never be inferred.',
  },
  {
    number: '05',
    title: 'Publish a safe first sitrep',
    body: 'On ClearBoard, state verified impact, the owner, the current action, and the next update time. Put sensitive evidence and identifying details in the restricted case record instead.',
  },
  {
    number: '06',
    title: 'Reassess until resolved',
    body: 'Update at the promised cadence. Escalate missed SLA clocks, adjust severity as evidence changes, and close only after impact, recovery, and follow-up ownership are recorded.',
  },
];

export default function OperatorRunbook() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <p className="font-mono text-sm uppercase tracking-[0.2em] text-gold">Operator reference</p>
      <h1 className="mt-2 text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">All Clear triage runbook</h1>
      <p className="max-w-2xl text-ink/80 leading-relaxed">Use this sequence when a surge arrives. The goal is not to process every alert independently—it is to establish a safe, shared response record quickly.</p>

      <ol className="mt-8 space-y-4">
        {steps.map((step) => (
          <li key={step.number} className="bg-white rounded-xl border border-deep-cream p-5 shadow-sm">
            <div className="flex items-start gap-4">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gold text-maroon font-mono font-bold text-sm">{step.number}</span>
              <div><h2 className="font-serif font-bold text-maroon text-lg">{step.title}</h2><p className="mt-2 text-ink/80 leading-relaxed">{step.body}</p></div>
            </div>
          </li>
        ))}
      </ol>

      <section className="mt-10 rounded-xl border border-maroon/20 bg-maroon/5 p-6">
        <h2 className="font-serif text-xl font-bold text-maroon">Safety stop</h2>
        <p className="mt-2 text-ink/80 leading-relaxed">If a signal suggests immediate danger, credible threats, or possible sensitive-data exposure, page the dedicated response queue immediately. Limit access to details and follow the emergency protocol before routine triage.</p>
      </section>
      <section className="mt-6 rounded-xl border border-gold/40 bg-light-gold/15 p-6">
        <h2 className="font-serif text-xl font-bold text-maroon">Sitrep starter</h2>
        <p className="mt-2 font-mono text-sm text-ink/80">[SEVERITY] [SERVICE/SCOPE] — Verified impact: … Owner: … Action underway: … Next ClearBoard update: …</p>
      </section>
      <div className="text-center mt-10"><Link to="/" className="text-maroon hover:text-gold transition-colors font-medium">← Back to ClearBoard</Link></div>
    </div>
  );
}
