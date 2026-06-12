import { Link } from 'react-router-dom';

const schedule = [
  { start: '1:00', time: '1:00–1:08', block: 'Open & frame', lead: 'Sean', minutes: 8 },
  { start: '1:08', time: '1:08–1:22', block: 'The pattern — three agents', lead: 'Sean', minutes: 14 },
  { start: '1:22', time: '1:22–1:32', block: 'Live demo · Card D', lead: 'Jake', minutes: 10 },
  { start: '1:32', time: '1:32–1:40', block: 'Form teams · pick a card', lead: 'All', minutes: 8 },
  { start: '1:40', time: '1:40–2:40', block: 'Build sprint 1', lead: 'Teams + coaches', minutes: 60 },
  { start: '2:40', time: '2:40–2:50', block: 'Break', lead: '—', minutes: 10 },
  { start: '2:50', time: '2:50–3:05', block: 'Build sprint 2 · harden', lead: 'Teams + coaches', minutes: 15 },
  { start: '3:05', time: '3:05–3:55', block: 'Demos · 5 × 10 min', lead: 'Teams', minutes: 50 },
  { start: '3:55', time: '3:55–4:00', block: 'Close', lead: 'Sean', minutes: 5 },
];

const timeline = schedule.map((s) => ({ time: s.start, label: s.block }));

export default function RunOfShow() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <h1 className="text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">
        Run of Show
      </h1>

      {/* Timeline */}
      <div className="relative mt-8">
        {/* Desktop horizontal */}
        <div className="hidden md:block">
          <div className="flex items-start justify-between relative">
            {/* Gold connecting line */}
            <div className="absolute top-5 left-0 right-0 h-0.5 bg-gold" />

            {timeline.map((item) => (
              <div key={item.time} className="relative flex flex-col items-center text-center flex-1">
                <div className="w-10 h-10 rounded-full bg-gold text-maroon flex items-center justify-center font-bold text-xs z-10 shadow-sm">
                  {item.time}
                </div>
                <p className="mt-2 text-sm font-medium text-ink/80 max-w-[90px]">
                  {item.label}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Mobile vertical */}
        <div className="md:hidden space-y-0">
          {timeline.map((item, i) => (
            <div key={item.time} className="flex items-start gap-4">
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-full bg-gold text-maroon flex items-center justify-center font-bold text-xs shadow-sm shrink-0">
                  {item.time}
                </div>
                {i < timeline.length - 1 && (
                  <div className="w-0.5 h-8 bg-gold/40" />
                )}
              </div>
              <p className="font-medium text-ink/80 pt-2">{item.label}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Detailed schedule */}
      <div className="mt-12 bg-white rounded-2xl border border-deep-cream p-6 shadow-sm overflow-x-auto">
        <h2 className="font-serif text-xl font-bold text-maroon mb-4">Schedule</h2>
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="text-left text-maroon border-b-2 border-gold">
              <th className="py-2 pr-4 font-semibold">Time</th>
              <th className="py-2 pr-4 font-semibold">Block</th>
              <th className="py-2 pr-4 font-semibold">Lead</th>
              <th className="py-2 pr-2 font-semibold text-right">Min</th>
            </tr>
          </thead>
          <tbody>
            {schedule.map((s) => (
              <tr key={s.time} className="border-b border-deep-cream last:border-0">
                <td className="py-2 pr-4 font-mono text-ink/70 whitespace-nowrap">{s.time}</td>
                <td className="py-2 pr-4 text-ink/90 font-medium">{s.block}</td>
                <td className="py-2 pr-4 text-ink/70">{s.lead}</td>
                <td className="py-2 pr-2 text-right text-ink/70">{s.minutes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Build Contract */}
      <div className="mt-12 bg-white rounded-2xl border border-deep-cream p-6 shadow-sm">
        <h2 className="font-serif text-xl font-bold text-maroon mb-3">
          The Build Contract
        </h2>
        <p className="text-ink/80 leading-relaxed italic">
          "Working beats perfect — routing works end to end · one escalation rule
          lands · you can demo it live."
        </p>
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
