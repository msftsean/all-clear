import { cards } from '../data/cards';
import CardTile from '../components/CardTile';
import HubNav from '../components/HubNav';

export default function Landing() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      {/* Hero */}
      <section className="text-center mb-12">
        <h1 className="text-5xl sm:text-6xl font-serif font-extrabold text-maroon tracking-tight">
          47 Doors
        </h1>
        <p className="mt-3 text-lg sm:text-xl text-ink/70 max-w-xl mx-auto">
          Pick a door. Build the agent behind it.
        </p>
        <div className="mt-4 w-16 h-0.5 bg-gold mx-auto" />
      </section>

      {/* Card Gallery */}
      <section>
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
