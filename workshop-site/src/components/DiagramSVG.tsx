import { ReactNode, useId } from 'react'
import { useScrollReveal } from '../hooks/useScrollReveal'

interface DiagramSVGProps {
  children: ReactNode
  title: string
  description?: string
  viewBox?: string
  className?: string
}

export default function DiagramSVG({
  children,
  title,
  description,
  viewBox = '0 0 800 400',
  className = 'w-full h-auto',
}: DiagramSVGProps) {
  const titleId = useId()
  const descId = useId()
  const ref = useScrollReveal<HTMLElement>()

  return (
    <figure ref={ref} className="diagram-frame reveal my-10">
      <svg
        viewBox={viewBox}
        className={`${className} svg-draw`}
        role="img"
        aria-labelledby={`${titleId}${description ? ` ${descId}` : ''}`}
      >
        <title id={titleId}>{title}</title>
        {description && <desc id={descId}>{description}</desc>}
        {children}
      </svg>
      {description && (
        <figcaption className="text-sm text-ink/70 mt-4 text-center">
          {description}
        </figcaption>
      )}
    </figure>
  )
}
