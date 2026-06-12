import { KeyboardEvent, useRef } from 'react'

interface Tab {
  id: string
  label: string
}

interface TabNavigationProps {
  tabs: Tab[]
  activeTab: string
  onTabChange: (tabId: string) => void
}

export default function TabNavigation({ tabs, activeTab, onTabChange }: TabNavigationProps) {
  const tabRefs = useRef<Record<string, HTMLButtonElement | null>>({})

  const moveTo = (index: number) => {
    const next = tabs[(index + tabs.length) % tabs.length]
    onTabChange(next.id)
    requestAnimationFrame(() => tabRefs.current[next.id]?.focus())
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    const currentIndex = tabs.findIndex((tab) => tab.id === activeTab)
    if (e.key === 'ArrowRight') {
      e.preventDefault()
      moveTo(currentIndex + 1)
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault()
      moveTo(currentIndex - 1)
    } else if (e.key === 'Home') {
      e.preventDefault()
      moveTo(0)
    } else if (e.key === 'End') {
      e.preventDefault()
      moveTo(tabs.length - 1)
    }
  }

  return (
    <nav className="tab-nav" aria-label="Workshop sections">
      <div
        className="max-w-7xl mx-auto px-6 flex gap-2 overflow-x-auto pb-4"
        role="tablist"
        onKeyDown={handleKeyDown}
      >
        {tabs.map((tab) => (
          <button
            key={tab.id}
            ref={(el) => { tabRefs.current[tab.id] = el }}
            role="tab"
            aria-selected={activeTab === tab.id}
            aria-controls={`${tab.id}-panel`}
            id={`${tab.id}-tab`}
            tabIndex={activeTab === tab.id ? 0 : -1}
            className={`tab-button whitespace-nowrap ${activeTab === tab.id ? 'tab-button-active' : ''}`}
            onClick={() => onTabChange(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </nav>
  )
}
