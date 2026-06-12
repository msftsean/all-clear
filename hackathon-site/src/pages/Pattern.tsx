import { Link } from 'react-router-dom';

const nodes = [
  {
    name: 'QueryAgent',
    verb: 'Understand',
    desc: 'Clean the message, classify it into exactly one intent.',
  },
  {
    name: 'RouterAgent',
    verb: 'Decide',
    desc: 'Pick the intent, set the priority, apply the escalation rules.',
  },
  {
    name: 'ActionAgent',
    verb: 'Act',
    desc: 'Answer, escalate, or open a ticket.',
  },
];

export default function Pattern() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <h1 className="text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">
        The Three-Agent Pattern
      </h1>

      {/* Pipeline diagram */}
      <div className="flex flex-col sm:flex-row items-stretch gap-4 my-10">
        {nodes.map((node, i) => (
          <div key={node.name} className="flex-1 flex flex-col items-center">
            <div className="bg-white rounded-2xl shadow-sm border border-deep-cream p-6 text-center w-full">
              <div className="w-14 h-14 rounded-full bg-gold/20 flex items-center justify-center mx-auto mb-3">
                <span className="text-gold text-2xl font-bold">{i + 1}</span>
              </div>
              <h3 className="font-mono text-sm font-semibold text-maroon mb-1">
                {node.name}
              </h3>
              <p className="font-serif text-lg font-bold text-deep-maroon">
                {node.verb}
              </p>
              <p className="text-sm text-ink/60 mt-2">{node.desc}</p>
            </div>
            {i < nodes.length - 1 && (
              <div className="hidden sm:flex items-center absolute right-0 translate-x-1/2">
                <span className="text-gold text-2xl">→</span>
              </div>
            )}
            {i < nodes.length - 1 && (
              <div className="sm:hidden flex justify-center py-2">
                <span className="text-gold text-2xl">↓</span>
              </div>
            )}
          </div>
        ))}
      </div>

      <p className="text-center text-ink/60 italic max-w-lg mx-auto">
        "A pattern, not a product. It works on any campus, any set of offices."
      </p>

      <div className="text-center mt-8">
        <Link
          to="/"
          className="text-maroon hover:text-gold transition-colors font-medium"
        >
          ← Back to all cards
        </Link>
      </div>
    </div>
  );
}
