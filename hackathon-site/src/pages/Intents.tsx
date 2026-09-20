import { Link } from 'react-router-dom';

const queues = [
  { name: 'Identity Security', key: 'identity_security', owner: 'Security on-call', topics: 'Credential attacks, access anomalies, account containment' },
  { name: 'Payments Reliability', key: 'payments_reliability', owner: 'Payments incident lead', topics: 'Checkout, transaction errors, release regressions' },
  { name: 'Privacy & Security', key: 'privacy_security', owner: 'Privacy response lead', topics: 'Possible exposure, sensitive evidence, external notifications' },
  { name: 'Network Operations', key: 'network_operations', owner: 'Network on-call', topics: 'Connectivity, policy rollouts, site telemetry gaps' },
  { name: 'Safety Response', key: 'safety_response', owner: 'Safety on-call', topics: 'Credible threats, immediate risk, restricted case handling' },
  { name: 'Platform Observability', key: 'platform_observability', owner: 'Platform on-call', topics: 'Alert noise, dependency health, error-budget signals' },
];

export default function Intents() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <p className="font-mono text-sm uppercase tracking-[0.2em] text-gold">Ownership map</p>
      <h1 className="mt-2 text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">Response queues</h1>
      <p className="mb-7 max-w-2xl text-ink/75">A queue is an accountable response team—not a mailbox. Triage selects one lead queue and records supporting responders when needed.</p>
      <div className="hidden sm:block overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead><tr className="border-b-2 border-gold"><th className="py-3 pr-4 font-serif text-maroon">Queue</th><th className="py-3 pr-4 font-mono text-sm text-gold">Key</th><th className="py-3 pr-4 font-serif text-maroon">Primary owner</th><th className="py-3 font-serif text-maroon">Typical signals</th></tr></thead>
          <tbody>{queues.map((queue) => <tr key={queue.key} className="border-b border-deep-cream"><td className="py-3 pr-4 font-semibold">{queue.name}</td><td className="py-3 pr-4 font-mono text-sm text-ink/60">{queue.key}</td><td className="py-3 pr-4 text-ink/80">{queue.owner}</td><td className="py-3 text-sm text-ink/70">{queue.topics}</td></tr>)}</tbody>
        </table>
      </div>
      <div className="sm:hidden space-y-4">{queues.map((queue) => <article key={queue.key} className="bg-white rounded-xl border border-deep-cream p-4 shadow-sm"><h2 className="font-serif font-bold text-maroon">{queue.name}</h2><p className="font-mono text-xs text-gold mt-0.5">{queue.key}</p><p className="text-sm text-ink/80 mt-1">{queue.owner}</p><p className="text-xs text-ink/60 mt-2">{queue.topics}</p></article>)}</div>
      <div className="text-center mt-8"><Link to="/" className="text-maroon hover:text-gold transition-colors font-medium">← Back to ClearBoard</Link></div>
    </div>
  );
}
