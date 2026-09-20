import { ShieldCheckmarkRegular, PhoneRegular } from '@fluentui/react-icons'
import { useEffect, useState } from 'react'

const NAV_ITEMS = [
  { id: 'overview', label: 'Overview' }, { id: 'version-matrix', label: 'Compatibility' },
  { id: 'checklist', label: 'Checklist' }, { id: 'start-commands', label: 'Start' },
  { id: 'demo-sequence', label: 'Triage demo' }, { id: 'troubleshooting', label: 'Troubleshoot' },
  { id: 'operating-model', label: 'Operating model' },
]

interface AuthResponse { clientPrincipal?: { userDetails?: string; userId?: string } }

export default function Nav() {
  const [active, setActive] = useState('')
  const [authName, setAuthName] = useState<string | null>(null)
  useEffect(() => {
    const update = () => { const offset = window.scrollY + 100; let current = ''; document.querySelectorAll('section[id]').forEach((s) => { if ((s as HTMLElement).offsetTop <= offset) current = s.id }); setActive(current) }
    window.addEventListener('scroll', update, { passive: true }); update(); return () => window.removeEventListener('scroll', update)
  }, [])
  useEffect(() => {
    fetch('/.auth/me', { cache: 'no-store' }).then((r) => r.ok ? r.json() as Promise<AuthResponse> : null)
      .then((data) => { const p = data?.clientPrincipal; if (p) setAuthName(p.userDetails || p.userId || 'Authenticated') }).catch(() => undefined)
  }, [])
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-16 bg-deep-space/90 backdrop-blur-md border-b border-lead/50 flex items-center px-6 gap-4" aria-label="Main navigation">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 bg-mercury-blue text-deep-space px-3 py-1 rounded-full text-sm">Skip to content</a>
      <div className="font-semibold text-sm text-silver whitespace-nowrap mr-2 flex items-center gap-2"><ShieldCheckmarkRegular className="text-mercury-blue text-xl" aria-hidden="true" /><span>All Clear</span><span className="text-lead/60">/</span><PhoneRegular className="text-mercury-blue" aria-hidden="true" /><span className="font-light text-silver/70">Ops companion</span></div>
      <div className="flex items-center gap-1 overflow-x-auto flex-1" role="list">{NAV_ITEMS.map((item) => <a key={item.id} href={`#${item.id}`} role="listitem" className={`whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 border ${active === item.id ? 'bg-mercury-blue text-deep-space border-mercury-blue' : 'text-silver border-transparent hover:bg-interactive hover:text-starlight'}`} aria-current={active === item.id ? 'true' : undefined}>{item.label}</a>)}</div>
      {authName && <div className="flex items-center gap-3 ml-auto flex-shrink-0 pl-4"><div className="flex items-center gap-2 text-xs text-silver"><span className="w-2 h-2 rounded-full bg-emerald-400" /><span className="max-w-32 truncate text-starlight font-medium">{authName}</span></div><a href="/.auth/logout" className="px-3 py-1.5 rounded-full text-xs text-silver border border-lead/50 hover:bg-interactive hover:text-starlight">Sign out</a></div>}
    </nav>
  )
}
