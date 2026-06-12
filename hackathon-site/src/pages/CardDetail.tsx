import { useParams, Navigate } from 'react-router-dom';
import { cards } from '../data/cards';
import LetterBadge from '../components/LetterBadge';
import StatusPill from '../components/StatusPill';
import CardNav from '../components/CardNav';

export default function CardDetail() {
  const { slug } = useParams<{ slug: string }>();
  const index = cards.findIndex((c) => c.slug === slug);

  if (index === -1) {
    return <Navigate to="/" replace />;
  }

  const card = cards[index];
  const prev = index > 0 ? cards[index - 1] : undefined;
  const next = index < cards.length - 1 ? cards[index + 1] : undefined;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* 1. Eyebrow */}
      <div className="flex items-center gap-3 mb-2">
        <LetterBadge letter={card.letter} size="lg" />
        <div>
          <p className="text-sm font-mono text-ink/50 uppercase tracking-wider">
            Card {card.letter} · <span className="text-gold">{card.slug}</span>
          </p>
          {card.pill && (
            <div className="mt-1">
              <StatusPill label={card.pill} />
            </div>
          )}
        </div>
      </div>

      {/* 2. Title */}
      <h1 className="text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule mt-4">
        {card.title}
      </h1>

      {/* 3. The Message */}
      <section className="mb-8">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-ink/50 mb-2">
          The Message
        </h2>
        <blockquote className="chat-bubble text-base leading-relaxed">
          "{card.message}"
        </blockquote>
      </section>

      {/* 4. Your Build */}
      <section className="mb-8">
        <h2 className="text-lg font-serif font-bold text-maroon mb-2">
          Your Build
        </h2>
        <p className="text-ink/80 leading-relaxed">{card.build}</p>
      </section>

      {/* 5. Skill */}
      <section className="mb-8">
        <h2 className="text-lg font-serif font-bold text-maroon mb-2">
          The Skill You'll Practice
        </h2>
        <p className="font-mono text-sm bg-deep-cream rounded-lg px-4 py-2 inline-block">
          {card.skill}
        </p>
      </section>

      {/* 6. Done When */}
      <section className="mb-8">
        <h2 className="text-lg font-serif font-bold text-maroon mb-2">
          Done When
        </h2>
        <ul className="space-y-2">
          {card.doneWhen.map((item, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="text-gold mt-0.5 font-bold">✓</span>
              <span className="text-ink/80">{item}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* 7. Routing Answer Key (collapsible) */}
      <section className="mb-8">
        <details className="bg-deep-cream/50 rounded-xl p-4 border border-deep-cream">
          <summary className="font-serif font-bold text-maroon text-base">
            Routing Answer Key
          </summary>
          <p className="mt-3 text-sm text-ink/70 leading-relaxed font-mono">
            {card.routingKey}
          </p>
        </details>
      </section>

      {/* 8. KB Articles */}
      <section className="mb-4">
        <h2 className="text-lg font-serif font-bold text-maroon mb-2">
          KB You Can Retrieve Against
        </h2>
        <ul className="space-y-1.5">
          {card.kb.map((article, i) => (
            <li key={i} className="flex items-start gap-2 text-ink/80">
              <span className="text-gold">📄</span>
              {article}
            </li>
          ))}
        </ul>
      </section>

      {/* 9. Footer Nav */}
      <CardNav prev={prev} next={next} />
    </div>
  );
}
