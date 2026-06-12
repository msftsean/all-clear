import { ReactNode } from 'react'

type Tone = 'info' | 'warn' | 'success'

interface CalloutCardProps {
  title?: string
  children: ReactNode
  tone?: Tone
}

const toneStyles: Record<Tone, { border: string; bg: string; icon: string; title: string }> = {
  info: { border: 'border-l-cofounder', bg: 'bg-cofounder-soft', icon: 'text-cofounder', title: 'text-cofounder' },
  warn: { border: 'border-l-amber/60', bg: 'bg-amber/8', icon: 'text-amber', title: 'text-amber' },
  success: { border: 'border-l-sage', bg: 'bg-sage-soft', icon: 'text-sage', title: 'text-sage' },
}

const iconPaths: Record<Tone, string> = {
  info: 'M10 2a8 8 0 1 0 0 16 8 8 0 0 0 0-16Zm.75 11.5a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 1.5 0v4.5ZM10 7.25a.85.85 0 1 1 0-1.7.85.85 0 0 1 0 1.7Z',
  warn: 'M10.7 3.35a.8.8 0 0 0-1.4 0L2.2 16.05A.8.8 0 0 0 2.9 17.25h14.2a.8.8 0 0 0 .7-1.2L10.7 3.35ZM10.75 14a.75.75 0 0 1-1.5 0 .75.75 0 0 1 1.5 0ZM10.6 8.1l-.25 4.1h-.7L9.4 8.1h1.2Z',
  success: 'M10 2a8 8 0 1 0 0 16 8 8 0 0 0 0-16Zm3.65 6.35-4.5 4.5a.5.5 0 0 1-.72-.02l-2-2.25a.5.5 0 1 1 .74-.66l1.65 1.86 4.12-4.13a.5.5 0 0 1 .71.7Z',
}

export default function CalloutCard({ title, children, tone = 'info' }: CalloutCardProps) {
  const styles = toneStyles[tone]

  return (
    <div className={`callout border-l-4 ${styles.border} ${styles.bg}`}>
      <div className="flex gap-3">
        <svg className={`mt-0.5 flex-shrink-0 ${styles.icon}`} style={{ width: 20, height: 20 }} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path d={iconPaths[tone]} />
        </svg>
        <div>
          {title && <h3 className={`font-semibold mb-1.5 text-sm ${styles.title}`}>{title}</h3>}
          <div className="text-ink/75 leading-relaxed text-sm">{children}</div>
        </div>
      </div>
    </div>
  )
}
