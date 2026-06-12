import { Link } from 'react-router-dom';
import type { Card } from '../data/cards';

interface CardNavProps {
  prev: Card | undefined;
  next: Card | undefined;
}

export default function CardNav({ prev, next }: CardNavProps) {
  return (
    <nav className="flex items-center justify-between mt-10 pt-6 border-t border-deep-cream">
      <div>
        {prev ? (
          <Link
            to={`/cards/${prev.slug}`}
            className="text-maroon hover:text-gold transition-colors font-medium"
          >
            ← Card {prev.letter}: {prev.title}
          </Link>
        ) : (
          <span />
        )}
      </div>

      <Link
        to="/"
        className="px-4 py-2 rounded-lg bg-deep-cream text-maroon font-semibold text-sm hover:bg-gold hover:text-white transition-colors"
      >
        All Cards
      </Link>

      <div>
        {next ? (
          <Link
            to={`/cards/${next.slug}`}
            className="text-maroon hover:text-gold transition-colors font-medium"
          >
            Card {next.letter}: {next.title} →
          </Link>
        ) : (
          <span />
        )}
      </div>
    </nav>
  );
}
