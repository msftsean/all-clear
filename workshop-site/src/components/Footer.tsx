export default function Footer() {
  return (
    <footer className="footer-shell mt-auto">
      <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between gap-4 text-sm text-ink/70">
        <div>
          <strong className="text-fg">All Clear</strong> — surge-scale incident triage with accountable automation
        </div>
        <div className="flex items-center gap-4">
          <span>Signal preserved</span>
          <span aria-hidden="true">|</span>
          <span>Decision auditable</span>
        </div>
      </div>
    </footer>
  )
}
