import { Link } from 'react-router-dom';

const nodes = [
  { name: 'Signal intake', verb: 'Normalize', desc: 'Capture source, time, scope, and confidence without losing raw evidence.' },
  { name: 'Incident engine', verb: 'Correlate', desc: 'Fingerprint related signals, deduplicate them, and calibrate severity.' },
  { name: 'Response loop', verb: 'Coordinate', desc: 'Assign a queue, enforce the SLA, and keep ClearBoard current.' },
];

export default function Pattern() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <p className="font-mono text-sm uppercase tracking-[0.2em] text-gold">All Clear method</p>
      <h1 className="mt-2 text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">The triage workflow</h1>
      <p className="max-w-2xl text-ink/75 leading-relaxed">A dependable response begins with evidence, not a flood of tickets. All Clear turns a surge into a bounded incident with accountable next steps.</p>
      <div className="flex flex-col sm:flex-row items-stretch gap-4 my-10">
        {nodes.map((node, i) => (
          <div key={node.name} className="flex-1 flex flex-col items-center">
            <div className="bg-white rounded-2xl shadow-sm border border-deep-cream p-6 text-center w-full">
              <div className="w-14 h-14 rounded-full bg-gold/20 flex items-center justify-center mx-auto mb-3">
                <span className="text-gold text-2xl font-bold">{i + 1}</span>
              </div>
              <h2 className="font-mono text-sm font-semibold text-maroon mb-1">{node.name}</h2>
              <p className="font-serif text-lg font-bold text-deep-maroon">{node.verb}</p>
              <p className="text-sm text-ink/60 mt-2">{node.desc}</p>
            </div>
            {i < nodes.length - 1 && <div className="flex justify-center py-2 sm:hidden"><span className="text-gold text-2xl">↓</span></div>}
          </div>
        ))}
      </div>
      <div className="rounded-xl border border-gold/40 bg-light-gold/15 p-5">
        <h2 className="font-serif text-lg font-bold text-maroon">The response record</h2>
        <p className="mt-1 text-ink/80">Every incident carries a fingerprint, severity, queue owner, SLA clocks, evidence links, and a next-update promise. ClearBoard shows only the safe operational summary.</p>
      </div>
      <div className="text-center mt-8"><Link to="/" className="text-maroon hover:text-gold transition-colors font-medium">← Back to ClearBoard</Link></div>
    </div>
  );
}
