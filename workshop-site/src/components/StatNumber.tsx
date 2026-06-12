import { useCountUp } from '../hooks/useCountUp'

interface StatNumberProps {
  value: number
  suffix?: string
  decimals?: number
  label: string
}

export default function StatNumber({ value, suffix = '', decimals = 0, label }: StatNumberProps) {
  const { count, ref } = useCountUp(value, 1800, decimals)
  return (
    <div className="stat-card reveal">
      <div ref={ref as React.RefObject<HTMLDivElement>} className="stat-number">
        {count.toFixed(decimals)}{suffix}
      </div>
      <p className="stat-label">{label}</p>
    </div>
  )
}
