import type { Theme } from '../hooks/useTheme'

interface ThemeToggleProps {
  theme: Theme
  onToggle: () => void
}

export default function ThemeToggle({ theme, onToggle }: ThemeToggleProps) {
  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={onToggle}
      aria-label={`Switch to ${theme === 'sequel' ? 'Saigon' : 'Sequel'} theme`}
      aria-pressed={theme === 'saigon'}
    >
      <span className={theme === 'sequel' ? 'active' : ''}>Sequel</span>
      <span className={theme === 'saigon' ? 'active' : ''}>Saigon</span>
    </button>
  )
}
