import { useEffect, useMemo, useState } from 'react'
import {
  ArrowRightRegular,
  ClockRegular,
  ShieldCheckmarkRegular,
  WarningRegular,
} from '@fluentui/react-icons'
import TabNavigation from './components/TabNavigation'
import Footer from './components/Footer'
import ThemeToggle from './components/ThemeToggle'
import { useTheme } from './hooks/useTheme'
import { useCountUp } from './hooks/useCountUp'

import Overview from './tabs/Overview'
import SignalToIncident from './tabs/SignalToIncident'
import Pipeline from './tabs/Pipeline'
import SeveritySla from './tabs/SeveritySla'
import SurgeDedup from './tabs/SurgeDedup'
import BoundedAuthority from './tabs/BoundedAuthority'
import VoicePhone from './tabs/VoicePhone'
import ClearBoard from './tabs/ClearBoard'
import DemoWalkthrough from './tabs/DemoWalkthrough'
import Safety from './tabs/Safety'
import WorkshopExercise from './tabs/WorkshopExercise'
import RunOfShow from './tabs/RunOfShow'
import PresenterScript from './tabs/PresenterScript'

type WorkshopTab = {
  id: string
  label: string
  component: () => JSX.Element
}

const tabs: WorkshopTab[] = [
  { id: 'overview', label: 'Overview', component: Overview },
  { id: 'contract', label: 'Signal to Incident', component: SignalToIncident },
  { id: 'pipeline', label: 'Pipeline', component: Pipeline },
  { id: 'severity', label: 'SEV & SLA', component: SeveritySla },
  { id: 'surge', label: 'Surge Dedup', component: SurgeDedup },
  { id: 'authority', label: 'Bounded Authority', component: BoundedAuthority },
  { id: 'voice-phone', label: 'Voice & Phone', component: VoicePhone },
  { id: 'clearboard', label: 'ClearBoard', component: ClearBoard },
  { id: 'demo', label: 'Demo Walkthrough', component: DemoWalkthrough },
  { id: 'safety', label: 'Safety', component: Safety },
  { id: 'exercise', label: 'Triage Exercise', component: WorkshopExercise },
  { id: 'run-of-show', label: 'Run of Show', component: RunOfShow },
  { id: 'presenter-script', label: 'Presenter Script', component: PresenterScript },
]

function AllClearMark() {
  return (
    <svg className="all-clear-mark" viewBox="0 0 48 48" aria-hidden="true">
      <circle cx="24" cy="24" r="18" fill="none" stroke="currentColor" strokeWidth="3" />
      <path d="m15 24 6 6 13-14" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M24 2v5M24 41v5M2 24h5M41 24h5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  )
}

function Hero({ onNavigate }: { onNavigate: (tabId: string) => void }) {
  const responseMinutes = useCountUp(15, 1400)
  const severities = useCountUp(4, 1400)
  const tools = useCountUp(3, 1400)

  return (
    <section className="hero-shell" aria-labelledby="hero-title">
      <div className="incident-grid" aria-hidden="true" />
      <div className="hero-orb hero-orb-one" />
      <div className="hero-orb hero-orb-two" />
      <div className="max-w-7xl mx-auto px-6 py-20 md:py-28 hero-animate relative">
        <div className="hero-kicker">
          <WarningRegular style={{ fontSize: 18 }} /> Incident-triage workshop companion
        </div>
        <h1 id="hero-title" className="hero-title">
          From noise<br />to all clear.
        </h1>
        <p className="hero-subtitle">
          Learn the operating contract that turns noisy, multi-channel signals into deduplicated incidents with accountable severity, queues, SLA clocks, and citation-grounded situation reports.
        </p>
        <div className="hero-actions">
          <button className="btn-primary" onClick={() => onNavigate('contract')}>
            Follow a signal <ArrowRightRegular style={{ fontSize: 18 }} />
          </button>
          <button className="btn-ghost" onClick={() => onNavigate('clearboard')}>
            Open ClearBoard lesson
          </button>
        </div>
        <div className="hero-stats" aria-label="All Clear operating controls">
          <div className="hero-stat">
            <ClockRegular style={{ fontSize: 26 }} />
            <strong ref={responseMinutes.ref}>{Math.round(responseMinutes.count)}</strong>
            <span>Minute SEV1 response SLA</span>
          </div>
          <div className="hero-stat">
            <WarningRegular style={{ fontSize: 26 }} />
            <strong ref={severities.ref}>{Math.round(severities.count)}</strong>
            <span>Deterministic severity levels</span>
          </div>
          <div className="hero-stat">
            <ShieldCheckmarkRegular style={{ fontSize: 26 }} />
            <strong ref={tools.ref}>{Math.round(tools.count)}</strong>
            <span>Bounded ActionAgent tools</span>
          </div>
        </div>
      </div>
    </section>
  )
}

function App() {
  const [activeTab, setActiveTab] = useState('overview')
  const { theme, toggleTheme } = useTheme()

  const active = useMemo(() => tabs.find((tab) => tab.id === activeTab) ?? tabs[0], [activeTab])
  const ActiveComponent = active.component

  useEffect(() => {
    const panel = document.getElementById(`${activeTab}-panel`)
    panel?.classList.add('tab-panel-enter')
    const timer = window.setTimeout(() => panel?.classList.remove('tab-panel-enter'), 350)
    const revealTargets = panel?.querySelectorAll<HTMLElement>('h2, .card, .callout, table, pre') ?? []
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const observers: IntersectionObserver[] = []

    revealTargets.forEach((el, index) => {
      el.classList.add('reveal')
      el.style.setProperty('--delay', `${Math.min(index, 8) * 45}ms`)
      if (prefersReduced) {
        el.classList.add('revealed')
        return
      }
      const observer = new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting) {
          el.classList.add('revealed')
          observer.disconnect()
        }
      }, { threshold: 0.08 })
      observer.observe(el)
      observers.push(observer)
    })

    return () => {
      window.clearTimeout(timer)
      observers.forEach((observer) => observer.disconnect())
    }
  }, [activeTab])

  return (
    <>
      <a href="#main-content" className="skip-link">Skip to main content</a>
      <div className="min-h-screen flex flex-col site-frame">
        <header className="sticky top-0 z-50 header-glass">
          <nav className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between gap-4" aria-label="Site">
            <div className="brand-lockup">
              <AllClearMark />
              <div>
                <p className="brand-title">All Clear</p>
                <p className="brand-subtitle">Incident-triage workshop</p>
              </div>
            </div>
            <ThemeToggle theme={theme} onToggle={toggleTheme} />
          </nav>
          <TabNavigation tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />
        </header>

        <main id="main-content" className="flex-1">
          {activeTab === 'overview' && <Hero onNavigate={setActiveTab} />}
          <div className="tab-stage" aria-live="polite" aria-atomic="true">
            <ActiveComponent />
          </div>
        </main>

        <Footer />
      </div>
    </>
  )
}

export default App
