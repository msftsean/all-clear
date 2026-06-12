import { useEffect, useState } from 'react'

export type Theme = 'sequel' | 'saigon'

function readStoredTheme(): Theme {
  const stored = localStorage.getItem('workshop-theme')
  return stored === 'saigon' || stored === 'sequel' ? stored : 'sequel'
}

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => readStoredTheme())

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('workshop-theme', theme)
  }, [theme])

  const toggleTheme = () => setTheme((current) => current === 'sequel' ? 'saigon' : 'sequel')

  return { theme, toggleTheme }
}
