interface LetterBadgeProps {
  letter: string;
  size?: 'sm' | 'md' | 'lg';
}

export default function LetterBadge({ letter, size = 'md' }: LetterBadgeProps) {
  const sizes = {
    sm: 'w-10 h-10 text-lg',
    md: 'w-12 h-12 text-xl',
    lg: 'w-16 h-16 text-3xl',
  };

  return (
    <span
      className={`${sizes[size]} inline-flex items-center justify-center rounded-full bg-gold text-maroon font-serif font-bold shadow-sm`}
    >
      {letter}
    </span>
  );
}
