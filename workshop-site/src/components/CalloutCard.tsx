import { ReactNode } from 'react'
import { LightbulbRegular, WarningRegular } from '@fluentui/react-icons'

interface CalloutCardProps {
  title?: string
  children: ReactNode
  variant?: 'default' | 'accent'
  icon?: ReactNode
}

export default function CalloutCard({ title, children, variant = 'default', icon }: CalloutCardProps) {
  const fallbackIcon = variant === 'accent'
    ? <WarningRegular style={{ fontSize: 22 }} />
    : <LightbulbRegular style={{ fontSize: 22 }} />

  return (
    <aside className={`callout callout-${variant}`}>
      {(title || icon) && (
        <div className="flex items-center gap-3 mb-3">
          <div className="icon-chip" aria-hidden="true">{icon ?? fallbackIcon}</div>
          {title && <h3 className="font-semibold text-dark-text">{title}</h3>}
        </div>
      )}
      <div className="text-ink/75 leading-relaxed">
        {children}
      </div>
    </aside>
  )
}
