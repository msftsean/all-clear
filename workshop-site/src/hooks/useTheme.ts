import { useEffect, useState } from 'react'

export type Theme = 'day' | 'night'

function readStoredTheme(): Theme {
  const stored = localStorage.getItem('workshop-theme')
  return stored === 'day' || stored === 'night' ? stored : 'day'
}

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => readStoredTheme())

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('workshop-theme', theme)
  }, [theme])

  const toggleTheme = () => setTheme((current) => current === 'day' ? 'night' : 'day')

  return { theme, toggleTheme }
}
