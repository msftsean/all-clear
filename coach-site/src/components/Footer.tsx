export default function Footer() {
  return (
    <footer className="bg-night border-t border-white/10 mt-auto">
      <div className="max-w-5xl mx-auto px-6 py-8 flex flex-col sm:flex-row gap-4 sm:justify-between sm:items-center">
        <div>
          <span className="font-serif text-white/90 text-lg">47 Doors</span>
          <span className="text-white/40 text-sm ml-3">Coach Prep for the AJCU Hackathon</span>
        </div>
        <div className="flex items-center gap-4 text-sm text-white/40">
          <span>Microsoft</span>
          <span className="text-white/20">|</span>
          <span>AJCU @ Fordham</span>
        </div>
      </div>
    </footer>
  )
}
