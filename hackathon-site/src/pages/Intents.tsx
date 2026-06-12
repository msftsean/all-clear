import { Link } from 'react-router-dom';

const intents = [
  {
    name: 'Financial Aid',
    key: 'financial_aid',
    office: 'Bursar / Financial Aid',
    topics: 'Cost, scholarships, aid packages, billing, work-study',
  },
  {
    name: 'Registrar',
    key: 'registrar',
    office: "Registrar's Office",
    topics: 'Registration, transcripts, enrollment, course changes, graduation',
  },
  {
    name: 'Campus Ministry',
    key: 'campus_ministry',
    office: 'Office of Campus Ministry',
    topics: 'Liturgy, sacraments, retreats, chaplaincy, service & immersion, interfaith life',
  },
  {
    name: 'IT',
    key: 'it',
    office: 'University IT',
    topics: 'Accounts, passwords, Wi-Fi, devices, learning systems',
  },
  {
    name: 'Student Wellness',
    key: 'student_wellness',
    office: 'Counseling & Health Services',
    topics: 'Mental health, medical, crisis, accessibility, basic needs',
  },
  {
    name: 'General / Mission',
    key: 'general',
    office: 'Front-desk pool',
    topics: 'Anything else; mission and student-life questions',
  },
];

export default function Intents() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <h1 className="text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">
        The Six Doors
      </h1>

      {/* Desktop table */}
      <div className="hidden sm:block overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b-2 border-gold">
              <th className="py-3 pr-4 font-serif text-maroon">Intent</th>
              <th className="py-3 pr-4 font-mono text-sm text-gold">Key</th>
              <th className="py-3 pr-4 font-serif text-maroon">Office</th>
              <th className="py-3 font-serif text-maroon">Topics</th>
            </tr>
          </thead>
          <tbody>
            {intents.map((intent) => (
              <tr key={intent.key} className="border-b border-deep-cream">
                <td className="py-3 pr-4 font-semibold">{intent.name}</td>
                <td className="py-3 pr-4 font-mono text-sm text-ink/60">
                  {intent.key}
                </td>
                <td className="py-3 pr-4 text-ink/80">{intent.office}</td>
                <td className="py-3 text-sm text-ink/70">{intent.topics}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile cards */}
      <div className="sm:hidden space-y-4">
        {intents.map((intent) => (
          <div
            key={intent.key}
            className="bg-white rounded-xl border border-deep-cream p-4 shadow-sm"
          >
            <h3 className="font-serif font-bold text-maroon">{intent.name}</h3>
            <p className="font-mono text-xs text-gold mt-0.5">{intent.key}</p>
            <p className="text-sm text-ink/80 mt-1">{intent.office}</p>
            <p className="text-xs text-ink/60 mt-2">{intent.topics}</p>
          </div>
        ))}
      </div>

      <p className="text-center text-ink/60 italic mt-8 max-w-lg mx-auto">
        "Campus Ministry is a first-class peer to IT and the Registrar — not an afterthought."
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
