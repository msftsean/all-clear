import { useEffect, useRef, useState } from 'react'

export function useCountUp(end: number, duration = 2000, decimals = 0) {
  const [count, setCount] = useState(0)
  const started = useRef(false)
  const frame = useRef<number>()
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (prefersReduced) {
      setCount(end)
      return
    }

    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting || started.current) return
      started.current = true
      const start = performance.now()

      const animate = (now: number) => {
        const progress = Math.min((now - start) / duration, 1)
        const eased = 1 - Math.pow(1 - progress, 3)
        setCount(Number((eased * end).toFixed(decimals)))
        if (progress < 1) frame.current = requestAnimationFrame(animate)
      }

      frame.current = requestAnimationFrame(animate)
      observer.disconnect()
    }, { threshold: 0.3 })

    observer.observe(el)
    return () => {
      observer.disconnect()
      if (frame.current) cancelAnimationFrame(frame.current)
    }
  }, [end, duration, decimals])

  return { count, ref }
}
