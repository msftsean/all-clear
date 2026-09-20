import { Link } from 'react-router-dom';

const rules = [
  { title: 'Deduplicate before dispatch', body: 'Use a stable fingerprint of service, symptom, time window, and scope. Preserve every contributing signal as evidence; do not create competing incident threads.' },
  { title: 'Severity follows impact and urgency', body: 'P1 means active critical harm or material service risk and starts a 15-minute acknowledgement clock. P2 needs timely coordinated mitigation. P3 is monitored work with a defined re-evaluation trigger.' },
  { title: 'One accountable queue', body: 'Every active incident has one lead queue and an explicit incident lead. Supporting teams may contribute, but ownership must stay unambiguous.' },
  { title: 'SLA clocks are visible', body: 'Track acknowledgement, mitigation, and update deadlines. A missed clock should escalate the response—not silently change the target.' },
  { title: 'Safety and privacy constrain communication', body: 'Minimize sensitive details, restrict case records when needed, and never expose personal or investigative information through ClearBoard.' },
  { title: 'Sitreps state facts and next steps', body: 'Publish scope, current impact, owner, actions underway, and the next update time. Mark uncertainty instead of filling gaps with speculation.' },
];

export default function Rules() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <p className="font-mono text-sm uppercase tracking-[0.2em] text-gold">Guardrails</p>
      <h1 className="mt-2 text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">Severity, SLA & safety policy</h1>
      <div className="space-y-5">{rules.map((rule) => <article key={rule.title} className="bg-white rounded-xl border border-deep-cream p-5 shadow-sm"><h2 className="font-serif font-bold text-maroon text-lg mb-2">{rule.title}</h2><p className="text-ink/80 leading-relaxed">{rule.body}</p></article>)}</div>
      <div className="text-center mt-8"><Link to="/" className="text-maroon hover:text-gold transition-colors font-medium">← Back to ClearBoard</Link></div>
    </div>
  );
}
