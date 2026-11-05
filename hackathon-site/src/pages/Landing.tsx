import { cards } from '../data/cards';
import CardTile from '../components/CardTile';
import HubNav from '../components/HubNav';

export default function Landing() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      {/* Hero */}
      <section className="text-center mb-12">
        <h1 className="text-5xl sm:text-6xl font-serif font-extrabold text-maroon tracking-tight">
          All Clear
        </h1>
        <p className="mt-3 text-lg sm:text-xl text-ink/70 max-w-xl mx-auto">
          Turn noisy surge signals into safe, owned incidents.
        </p>
        <div className="mt-4 w-16 h-0.5 bg-gold mx-auto" />
      </section>

      <section>
        <div className="mb-5 flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
          <h2 className="font-serif text-2xl font-bold text-maroon">Triage scenarios</h2>
          <p className="font-mono text-sm text-ink/60">signal → incident → owner → sitrep</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {cards.map((card) => (
            <CardTile key={card.slug} card={card} />
          ))}
        </div>
      </section>

      {/* Hub Nav */}
      <HubNav />
    </div>
  );
}
