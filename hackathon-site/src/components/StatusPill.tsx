interface StatusPillProps {
  label: string;
}

export default function StatusPill({ label }: StatusPillProps) {
  return (
    <span className="inline-block px-3 py-0.5 rounded-full bg-maroon text-cream text-xs font-semibold uppercase tracking-wide">
      {label}
    </span>
  );
}
