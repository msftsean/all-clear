import { useEffect, useMemo, useState } from 'react'
import { ArrowRightRegular, DoorArrowRightRegular, ShieldCheckmarkRegular, SparkleRegular } from '@fluentui/react-icons'
import TabNavigation from './components/TabNavigation'
import Footer from './components/Footer'
import ThemeToggle from './components/ThemeToggle'
import { useTheme } from './hooks/useTheme'
import { useCountUp } from './hooks/useCountUp'

import Overview from './tabs/Overview'
import TheProblem from './tabs/TheProblem'
import ChatbotsToAgents from './tabs/ChatbotsToAgents'
import TrustBoundaries from './tabs/TrustBoundaries'
import Architecture from './tabs/Architecture'
import VoiceAccessibility from './tabs/VoiceAccessibility'
import Telephony from './tabs/Telephony'
import DemoWalkthrough from './tabs/DemoWalkthrough'
import ResponsibleAI from './tabs/ResponsibleAI'
import ReuseAcrossCampus from './tabs/ReuseAcrossCampus'
import YourFirstAgent from './tabs/YourFirstAgent'
import PresenterScript from './tabs/PresenterScript'
import RunOfShow from './tabs/RunOfShow'

type WorkshopTab = {
  id: string
  label: string
  component: () => JSX.Element
}

const tabs: WorkshopTab[] = [
  { id: 'overview', label: 'Overview', component: Overview },
  { id: 'problem', label: 'The Problem', component: TheProblem },
  { id: 'chatbots-to-agents', label: 'Chatbots to Agents', component: ChatbotsToAgents },
  { id: 'trust', label: 'Trust & Boundaries', component: TrustBoundaries },
  { id: 'architecture', label: 'Architecture', component: Architecture },
  { id: 'voice', label: 'Voice & Accessibility', component: VoiceAccessibility },
  { id: 'telephony', label: 'Phone Integration', component: Telephony },
  { id: 'demo', label: 'Demo Walkthrough', component: DemoWalkthrough },
  { id: 'responsible-ai', label: 'Responsible AI', component: ResponsibleAI },
  { id: 'reuse', label: 'Reuse Across Campus', component: ReuseAcrossCampus },
  { id: 'your-first-agent', label: 'Your First Agent', component: YourFirstAgent },
  { id: 'run-of-show', label: 'Run of Show', component: RunOfShow },
  { id: 'presenter-script', label: 'Presenter Script', component: PresenterScript },
]

function DoorMark() {
  return (
    <svg className="door-mark" viewBox="0 0 48 48" aria-hidden="true">
      <path d="M13 43V6h22v37" fill="none" stroke="currentColor" strokeWidth="3" strokeLinejoin="round" />
      <path d="M19 43V13h16v30" fill="none" stroke="currentColor" strokeWidth="3" strokeLinejoin="round" />
      <circle cx="30" cy="29" r="1.8" fill="currentColor" />
    </svg>
  )
}

function Hero({ onNavigate }: { onNavigate: (tabId: string) => void }) {
  const doors = useCountUp(47, 1600)
  const agents = useCountUp(3, 1600)
  const principles = useCountUp(7, 1600)

  return (
    <section className="hero-shell" aria-labelledby="hero-title">
      <div className="hero-orb hero-orb-one" />
      <div className="hero-orb hero-orb-two" />
      <div className="max-w-7xl mx-auto px-6 py-20 md:py-28 hero-animate relative">
        <div className="hero-kicker">
          <SparkleRegular style={{ fontSize: 18 }} /> 45-minute executive briefing
        </div>
        <h1 id="hero-title" className="hero-title">
          Trustworthy<br />Agentic AI
        </h1>
        <p className="hero-subtitle">
          A cinematic workshop companion for building AI agents that earn institutional trust — one front door, every student need, no hand-waving.
        </p>
        <div className="hero-actions">
          <button className="btn-primary" onClick={() => onNavigate('problem')}>
            Start the story <ArrowRightRegular style={{ fontSize: 18 }} />
          </button>
          <button className="btn-ghost" onClick={() => onNavigate('architecture')}>
            See architecture
          </button>
        </div>
        <div className="hero-stats" aria-label="Workshop highlights">
          <div className="hero-stat">
            <DoorArrowRightRegular style={{ fontSize: 26 }} />
            <strong ref={doors.ref}>{Math.round(doors.count)}+</strong>
            <span>Portals → 1 Door</span>
          </div>
          <div className="hero-stat">
            <ShieldCheckmarkRegular style={{ fontSize: 26 }} />
            <strong ref={agents.ref}>{Math.round(agents.count)}</strong>
            <span>Agent Pipeline</span>
          </div>
          <div className="hero-stat">
            <DoorMark />
            <strong ref={principles.ref}>{Math.round(principles.count)}</strong>
            <span>Trust Principles</span>
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
              <DoorMark />
              <div>
                <p className="brand-title">47 Doors</p>
                <p className="brand-subtitle">Workshop Companion</p>
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
