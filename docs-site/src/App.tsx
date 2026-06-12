import { useEffect, useState } from 'react'
import Nav from './components/Nav'
import Hero from './components/Hero'
import OverviewSection from './components/OverviewSection'
import VersionMatrixSection from './components/VersionMatrixSection'
import ChecklistSection from './components/ChecklistSection'
import StartCommandsSection from './components/StartCommandsSection'
import DemoSequenceSection from './components/DemoSequenceSection'
import TroubleshootingSection from './components/TroubleshootingSection'
import EduFramingSection from './components/EduFramingSection'
import Footer from './components/Footer'

export default function App() {
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
          }
        })
      },
      { threshold: 0.1, rootMargin: '0px 0px -60px 0px' },
    )
    document.querySelectorAll('.reveal').forEach((el) => observer.observe(el))
    return () => observer.disconnect()
  }, [])

  return (
    <div className="min-h-screen bg-deep-space text-starlight font-sans">
      <a href="#main-content" className="skip-link">Skip to main content</a>
      <Nav />
      <main id="main-content">
        <Hero />
        <div className="max-w-4xl mx-auto px-6 pb-20 space-y-24">
          <OverviewSection />
          <VersionMatrixSection />
          <ChecklistSection />
          <StartCommandsSection />
          <DemoSequenceSection />
          <TroubleshootingSection />
          <EduFramingSection />
        </div>
      </main>
      <Footer />
      <BackToTop />
    </div>
  )
}

function BackToTop() {
  const [visible, setVisible] = useState(false)
  useEffect(() => {
    const handler = () => setVisible(window.scrollY > 400)
    window.addEventListener('scroll', handler, { passive: true })
    handler()
    return () => window.removeEventListener('scroll', handler)
  }, [])
  return (
    <button
      onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
      className={`back-top fixed bottom-7 right-7 w-11 h-11 rounded-full bg-mercury-blue text-white flex items-center justify-center transition-all duration-300 hover:brightness-110 focus-visible:ring-2 focus-visible:ring-mercury-blue z-50 ${visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'}`}
      aria-label="Back to top"
    >
      ↑
    </button>
  )
}
