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
      aria-label={`Switch to ${theme === 'day' ? 'night' : 'day'} theme`}
      aria-pressed={theme === 'night'}
    >
      <span className={theme === 'day' ? 'active' : ''}>Day</span>
      <span className={theme === 'night' ? 'active' : ''}>Night</span>
    </button>
  )
}
