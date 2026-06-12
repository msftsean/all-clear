import { useState } from 'react'
import { ChevronDownRegular, ChevronUpRegular, PresenterRegular } from '@fluentui/react-icons'

interface CollapsibleNotesProps {
  children: React.ReactNode
}

export default function CollapsibleNotes({ children }: CollapsibleNotesProps) {
  const [isOpen, setIsOpen] = useState(false)
  const panelId = 'presenter-notes'

  return (
    <section className="notes-shell" aria-label="Presenter notes">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="notes-toggle"
        aria-expanded={isOpen}
        aria-controls={panelId}
      >
        <PresenterRegular style={{ fontSize: 18 }} />
        Presenter Notes
        {isOpen ? <ChevronUpRegular style={{ fontSize: 18 }} /> : <ChevronDownRegular style={{ fontSize: 18 }} />}
      </button>

      {isOpen && (
        <div id={panelId} className="notes-panel">
          {children}
        </div>
      )}
    </section>
  )
}
