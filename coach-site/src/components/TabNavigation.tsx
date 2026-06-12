import { useEffect, useRef } from 'react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'

interface NavSection { id: string; title: string }

interface TabNavigationProps {
  sections: NavSection[]
  activeSectionId: string
  mobileMenuOpen: boolean
  onSelect: (id: string) => void
  onToggleMenu: () => void
}

export default function TabNavigation({
  sections,
  activeSectionId,
  mobileMenuOpen,
  onSelect,
  onToggleMenu,
}: TabNavigationProps) {
  const toggleRef = useRef<HTMLButtonElement | null>(null)

  useEffect(() => {
    if (!mobileMenuOpen) return
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onToggleMenu()
        toggleRef.current?.focus()
      }
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [mobileMenuOpen, onToggleMenu])

  return (
    <div>
      {/* Desktop nav */}
      <nav aria-label="Coach sections" className="hidden sm:flex items-center gap-1 max-w-5xl mx-auto px-4 py-2 overflow-x-auto">
        {sections.map((section) => {
          const active = section.id === activeSectionId
          return (
            <button
              key={section.id}
              type="button"
              aria-current={active ? 'true' : undefined}
              className={`tab-button ${active ? 'tab-button-active' : ''}`}
              onClick={() => onSelect(section.id)}
            >
              {section.title}
            </button>
          )
        })}
      </nav>

      {/* Mobile */}
      <div className="sm:hidden flex items-center justify-between max-w-5xl mx-auto px-4 py-2">
        <span className="text-sm font-medium text-ink/60" aria-hidden="true">
          {sections.find((s) => s.id === activeSectionId)?.title ?? 'Sections'}
        </span>
        <button
          ref={toggleRef}
          type="button"
          aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={mobileMenuOpen}
          aria-controls="mobile-section-menu"
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-pill border border-border text-sm font-medium text-ink bg-surface focus:outline-none focus-visible:ring-2 focus-visible:ring-cofounder focus-visible:ring-offset-2 transition-colors hover:border-cofounder/40"
          onClick={onToggleMenu}
        >
          {mobileMenuOpen ? (
            <XMarkIcon className="h-4 w-4" aria-hidden="true" />
          ) : (
            <Bars3Icon className="h-4 w-4" aria-hidden="true" />
          )}
          Menu
        </button>
      </div>

      {/* Mobile disclosure */}
      {mobileMenuOpen && (
        <nav
          id="mobile-section-menu"
          aria-label="Sections"
          className="sm:hidden border-t border-border bg-white"
        >
          <ul className="flex flex-col py-1 max-w-5xl mx-auto">
            {sections.map((section) => {
              const active = section.id === activeSectionId
              return (
                <li key={section.id}>
                  <button
                    type="button"
                    aria-current={active ? 'true' : undefined}
                    className={`w-full text-left px-4 py-2.5 text-sm font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-cofounder focus-visible:ring-inset transition-colors ${
                      active ? 'text-cofounder bg-cofounder-soft' : 'text-ink hover:bg-paper'
                    }`}
                    onClick={() => onSelect(section.id)}
                  >
                    {section.title}
                  </button>
                </li>
              )
            })}
          </ul>
        </nav>
      )}
    </div>
  )
}
