import { Link } from 'react-router-dom';

const rules = [
  {
    title: 'Whole-person overlap',
    body: 'Distress can route to both Wellness and Ministry. Clinical signals (sleep loss, panic, "I can\'t function") → Wellness. Meaning/faith/discernment signals → Ministry. Ambiguous → Wellness, with a chaplaincy offer.',
  },
  {
    title: 'Safety override',
    body: 'Any risk-of-harm signal → Student Wellness, escalate=true, priority=urgent. Surface the 24/7 crisis line and create a high-priority ticket regardless of hours.',
  },
  {
    title: 'Offer, don\'t auto-create (Campus Ministry)',
    body: 'Pastoral handoffs are opt-in — the agent offers a chaplain, it doesn\'t book one.',
  },
  {
    title: 'Autonomous tickets (Wellness & Financial Aid)',
    body: 'The cost of a missed ticket is high, so the agent may create one on its own.',
  },
  {
    title: 'Financial vs. Registrar',
    body: '"Can I drop a class without losing aid?" → Financial Aid (aid is the blocker). "What\'s the drop deadline?" → Registrar.',
  },
  {
    title: 'IT vs. any department',
    body: 'Route to the owning department to learn how to USE a system; route to IT only when the system itself is broken.',
  },
];

export default function Rules() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">
        Escalation &amp; Routing Rules
      </h1>

      <div className="space-y-6">
        {rules.map((rule) => (
          <div
            key={rule.title}
            className="bg-white rounded-xl border border-deep-cream p-5 shadow-sm"
          >
            <h3 className="font-serif font-bold text-maroon text-lg mb-2">
              {rule.title}
            </h3>
            <p className="text-ink/80 leading-relaxed">{rule.body}</p>
          </div>
        ))}
      </div>

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
