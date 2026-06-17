import { useEffect, useRef, useState } from 'react'
import TabNavigation from './components/TabNavigation'
import Footer from './components/Footer'
import HeroBanner from './components/HeroBanner'
import { sectionEntries, DEFAULT_SECTION_ID } from './content'
import * as FluentIcons from '@fluentui/react-icons/svg'

const navSections = sectionEntries.map((e) => ({ id: e.meta.id, title: e.meta.title }))
const validIds = new Set(navSections.map((s) => s.id))

function readHashSection(): string {
  const hash = window.location.hash.replace(/^#/, '')
  return validIds.has(hash) ? hash : DEFAULT_SECTION_ID
}

const sectionIcons: Record<string, typeof FluentIcons.BookOpenRegular> = {
  prepare: FluentIcons.BookOpenRegular,
  timeline: FluentIcons.CalendarLtrRegular,
  framing: FluentIcons.ChatRegular,
  help: FluentIcons.PersonSupportRegular,
  troubleshooting: FluentIcons.WrenchRegular,
  assess: FluentIcons.CheckmarkCircleRegular,
}

function App() {
  const [activeSectionId, setActiveSectionId] = useState<string>(() =>
    typeof window !== 'undefined' ? readHashSection() : DEFAULT_SECTION_ID
  )
  // Start collapsed when deep-linking straight to a section so its content is
  // not buried beneath the full-height hero.
  const [heroCollapsed, setHeroCollapsed] = useState<boolean>(() =>
    typeof window !== 'undefined' ? readHashSection() !== DEFAULT_SECTION_ID : false
  )
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const mainRef = useRef<HTMLElement>(null)
  const sectionRef = useRef<HTMLElement>(null)
  const firstRender = useRef(true)

  useEffect(() => {
    const onHashChange = () => setActiveSectionId(readHashSection())
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  // On section change (nav, intro list, or back/forward), collapse the hero and
  // bring the active section into view so the content swap is visible. Skipped
  // on the initial render.
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false
      return
    }
    setHeroCollapsed(true)
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    requestAnimationFrame(() =>
      requestAnimationFrame(() => {
        sectionRef.current?.scrollIntoView({
          behavior: reduce ? 'auto' : 'smooth',
          block: 'start',
        })
      })
    )
  }, [activeSectionId])

  // Scroll-reveal with IntersectionObserver
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    if (mediaQuery.matches) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.remove('reveal-hidden')
            entry.target.classList.add('reveal-visible')
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    )

    const els = document.querySelectorAll('[data-reveal]')
    els.forEach((el, i) => {
      el.classList.add('reveal-hidden')
      ;(el as HTMLElement).style.transitionDelay = `${i * 80}ms`
      observer.observe(el)
    })

    return () => observer.disconnect()
  }, [activeSectionId])

  const select = (id: string) => {
    setActiveSectionId(id)
    setMobileMenuOpen(false)
    if (window.location.hash.replace(/^#/, '') !== id) {
      window.location.hash = id
    }
  }

  const active = sectionEntries.find((e) => e.meta.id === activeSectionId) ?? sectionEntries[0]
  const ActiveComponent = active.component

  return (
    <div className="min-h-screen flex flex-col bg-paper">
      {/* Skip link */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      {/* Hero */}
      <HeroBanner
        onSectionSelect={select}
        activeSectionId={activeSectionId}
        collapsed={heroCollapsed}
        onToggleCollapse={() => setHeroCollapsed((c) => !c)}
      />

      {/* Sticky pill nav */}
      <header
        className="pill-nav bg-white/80 border-b border-border sticky top-0 z-30 shadow-soft"
        role="banner"
      >
        <TabNavigation
          sections={navSections}
          activeSectionId={active.meta.id}
          mobileMenuOpen={mobileMenuOpen}
          onSelect={select}
          onToggleMenu={() => setMobileMenuOpen((open) => !open)}
        />
      </header>

      <main id="main-content" tabIndex={-1} ref={mainRef} className="flex-1 max-w-5xl w-full mx-auto px-4 py-12">
        {/* Intro section — "About this site" */}
        <section aria-labelledby="intro-heading" className="mb-12" data-reveal>
          <h2 id="intro-heading" className="sr-only">About this site</h2>
          <div className="card-raised bg-cofounder-soft rounded-2xl">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-cofounder-soft flex items-center justify-center">
                <span aria-hidden="true" className="text-cofounder text-lg">◆</span>
              </div>
              <div className="min-w-0">
                <p className="text-ink/80 leading-relaxed">
                  This is a calm, scannable companion for <strong>coaches</strong> running the 47 Doors
                  AJCU hackathon. It re-presents the existing coach guides — how to prepare the room and
                  tech, run the day, frame the mission, help blocked participants, troubleshoot setup
                  failures, and assess the build sprint.
                </p>
                <p className="text-ink/80 leading-relaxed mt-3">
                  Use it on a laptop or phone, before and during the event. Jump to any of the six
                  sections below; <strong>Prepare</strong> is the place to start the night before.
                </p>
              </div>
            </div>
            <ul className="mt-6 grid gap-2 sm:grid-cols-2" role="list">
              {sectionEntries.map((e) => {
                const Icon = sectionIcons[e.meta.id]
                return (
                  <li key={e.meta.id}>
                    <button
                      type="button"
                      onClick={() => select(e.meta.id)}
                      className="text-left w-full flex items-start gap-3 px-3 py-2.5 rounded-xl hover:bg-cofounder-soft transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cofounder focus-visible:ring-offset-2"
                    >
                      {Icon && <Icon className="mt-0.5 flex-shrink-0 text-cofounder" style={{ width: 18, height: 18 }} aria-hidden="true" />}
                      <span>
                        <span className="font-semibold text-cofounder">{e.meta.title}</span>
                        <span className="text-ink/60 text-sm"> — {e.meta.summary}</span>
                      </span>
                    </button>
                  </li>
                )
              })}
            </ul>
          </div>
        </section>

        {/* Active section */}
        <section ref={sectionRef} aria-labelledby="section-heading" data-reveal className="scroll-mt-20">
          <div className="flex items-center gap-3 mb-2">
            {(() => {
              const Icon = sectionIcons[active.meta.id]
              return Icon ? (
                <div className="w-9 h-9 rounded-xl bg-cofounder-soft flex items-center justify-center flex-shrink-0">
                  <Icon className="text-cofounder" style={{ width: 18, height: 18 }} aria-hidden="true" />
                </div>
              ) : null
            })()}
            <h2 id="section-heading" className="text-2xl font-semibold text-ink">
              {active.meta.title}
            </h2>
          </div>
          <p className="text-ink/60 mb-8 pl-12">{active.meta.summary}</p>
          <ActiveComponent />
        </section>
      </main>

      <Footer />
    </div>
  )
}

export default App
