export default function Footer() {
  return (
    <footer className="border-t border-lead/50 bg-midnight-slate/60 px-6 py-10">
      <div className="max-w-4xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4 text-sm text-silver">
        <div>
          <div className="text-starlight font-semibold">47 Doors Voice Feature Demo Runbook</div>
          <div className="text-xs text-lead mt-1">Mercury cinematic redesign · React 18 + Vite 5 + Tailwind 3.4</div>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="px-3 py-1 rounded-full border border-lead/50 bg-deep-space">AAD gated</span>
          <span className="px-3 py-1 rounded-full border border-lead/50 bg-deep-space">Azure live</span>
          <span className="px-3 py-1 rounded-full border border-lead/50 bg-deep-space">Voice ready</span>
        </div>
      </div>
    </footer>
  )
}
