import { Link } from 'react-router-dom';
import type { Card } from '../data/cards';
import LetterBadge from './LetterBadge';
import StatusPill from './StatusPill';

interface CardTileProps {
  card: Card;
}

export default function CardTile({ card }: CardTileProps) {
  return (
    <Link
      to={`/cards/${card.slug}`}
      className="group block bg-white rounded-2xl shadow-sm hover:shadow-md border border-deep-cream/60 p-5 transition-all hover:-translate-y-0.5"
    >
      <div className="flex items-start gap-4">
        <LetterBadge letter={card.letter} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-serif text-lg font-bold text-maroon group-hover:text-deep-maroon transition-colors">
              {card.title}
            </h3>
            {card.pill && <StatusPill label={card.pill} />}
          </div>
          <p className="mt-1 text-sm text-ink/70 font-mono">{card.skill}</p>
        </div>
      </div>
    </Link>
  );
}
