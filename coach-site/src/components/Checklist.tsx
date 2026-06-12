interface ChecklistProps {
  title?: string
  items: string[]
}

export default function Checklist({ title, items }: ChecklistProps) {
  return (
    <div className="card">
      {title && <h3 className="font-semibold text-ink mb-3 text-sm uppercase tracking-wide text-ink/60">{title}</h3>}
      <ul className="space-y-2" role="list">
        {items.map((item, i) => (
          <li key={i} className="flex items-start gap-3 text-ink/75 leading-relaxed text-sm">
            <span
              aria-hidden="true"
              className="mt-0.5 h-5 w-5 flex-shrink-0 rounded-md border-2 border-cofounder/30 bg-cofounder-soft flex items-center justify-center"
            >
              <svg className="text-cofounder/0" style={{ width: 10, height: 10 }} viewBox="0 0 20 20" fill="currentColor">
                <path d="M3.37 10.17a.5.5 0 0 0-.74.66l4 4.5c.19.22.52.23.72.02l10.5-10.5a.5.5 0 0 0-.7-.7L7.02 14.27l-3.65-4.1Z" />
              </svg>
            </span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
