import SectionHeader from './SectionHeader'

export default function StartCommandsSection() {
  return (
    <section id="start-commands" className="scroll-mt-24 reveal reveal-delay-1">
      <SectionHeader icon="🚀" title="Start Commands" id="start-commands-heading" />
      <pre className="text-mercury-blue/80 text-xs mb-8">{`┌──────────────────────────────────────────────────────┐
│  🚀  LAUNCH SEQUENCE — CHOOSE YOUR PATH              │
├──────────────────────────────────────────────────────┤
│  Option A  ── ☁️  Azure Container Apps (Recommended) │
│  Option B  ── 🐳 Docker (local alternative)          │
│  Option C  ── 💻 Local Dev (debugging fallback)      │
│  Option D  ── ☁️  GitHub Codespaces (cloud dev)       │
└──────────────────────────────────────────────────────┘`}</pre>

      <div className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 mb-4 card-hover">
        <h3 className="text-mercury-blue font-medium text-lg mb-3">☁️ Option A — Azure Container Apps <em className="text-silver font-light">(Recommended)</em></h3>
        <p className="text-silver text-sm mb-4">This is the <strong className="text-starlight">primary demo path</strong>. Azure resources are live and verified in <code>rg-vvoice</code> (eastus2).</p>
        <pre>{`# 1️⃣  Authenticate (once per machine)
azd auth login

# 2️⃣  Provision + deploy everything (first time, ~5 min)
azd up

# 2b️⃣  Subsequent deploys (code changes only)
azd deploy

# 3️⃣  Get the live URL
azd env get-values | grep AZURE_CONTAINERAPP_URL`}</pre>
        <blockquote className="border-l-4 border-mercury-blue/50 pl-4 py-2 bg-mercury-blue/5 rounded-r-xl text-silver text-sm mt-4">
          <strong className="text-starlight">💡 Subscription:</strong> <code>ME-MngEnvMCAP262307-segayle-1</code> · <strong className="text-starlight">Region:</strong> <code>eastus2</code>
        </blockquote>
      </div>

      <div className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 mb-4 card-hover">
        <h3 className="text-mercury-blue font-medium text-lg mb-3">🐳 Option B — Docker <em className="text-silver font-light">(Local Alternative)</em></h3>
        <pre>{`docker-compose up
# 🖼️ Frontend: http://localhost:5173
# 🖥️ Backend:  http://localhost:8000`}</pre>
      </div>

      <div className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 mb-4 card-hover">
        <h3 className="text-mercury-blue font-medium text-lg mb-3">💻 Option C — Local Dev <em className="text-silver font-light">(Debugging Fallback)</em></h3>
        <pre>{`# 🖥️ Terminal 1 — Backend
cd backend
cp .env.example .env          # Set MOCK_MODE=false + Azure creds for live mode
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`}</pre>
        <pre className="mt-2">{`# 🖼️ Terminal 2 — Frontend
cd frontend
npm install
npm run dev                   # Opens http://localhost:5173`}</pre>
      </div>

      <div className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 mb-4 card-hover">
        <h3 className="text-mercury-blue font-medium text-lg mb-3">☁️ Option D — GitHub Codespaces</h3>
        <pre>{`# Same as Option C — Vite proxy handles /api routing
# ⚠️  DO NOT set VITE_API_BASE_URL to a localhost URL inside Codespaces
# Leave it as empty string in frontend/.env.local:
echo "VITE_API_BASE_URL=" > frontend/.env.local`}</pre>
      </div>

      <div className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover">
        <h3 className="text-mercury-blue font-medium text-lg mb-3">🩺 Health Check <em className="text-silver font-light">(Verify before demoing)</em></h3>
        <blockquote className="border-l-4 border-mercury-blue/50 pl-4 py-2 bg-mercury-blue/5 rounded-r-xl text-silver text-sm mb-4">
          The live Container App URL is hardcoded below. Both endpoints have been verified ✅.
        </blockquote>
        <pre>{`# ☁️ Azure (primary — LIVE)
curl https://frontdoor-6wfum6gndxawy-backend.blackflower-446b9850.eastus2.azurecontainerapps.io/api/health
# ✅ Verified: LLM connecting, services up: ticketing, knowledge_base, session_store

curl https://frontdoor-6wfum6gndxawy-backend.blackflower-446b9850.eastus2.azurecontainerapps.io/api/realtime/health
# ✅ Verified: { "realtime_available": true, "mock_mode": false, "voice_enabled": true }

# 💻 Local fallback
# curl http://localhost:8000/api/health
# curl http://localhost:8000/api/realtime/health`}</pre>
        <div className="mt-4 space-y-2">
          {[
            { label: 'Backend Health', status: 'healthy (ticketing ✅ · knowledge_base ✅ · session_store ✅)' },
            { label: 'Realtime Health', status: 'available (mock_mode: false · voice_enabled: true — Azure Live)' },
            { label: 'Frontend Load', status: 'frontdoor-6wfum6gndxawy-backend.blackflower-446b9850.eastus2.azurecontainerapps.io' },
          ].map((row) => (
            <div key={row.label} className="flex items-center gap-3 text-sm">
              <span className="text-silver font-mono min-w-32 text-xs">{row.label}</span>
              <div className="flex-1 h-1.5 bg-white/5 rounded-full overflow-hidden"><div className="h-full rounded-full bg-emerald-500 w-full" /></div>
              <span className="text-emerald-400 text-xs">✅</span>
              <span className="text-silver text-xs truncate max-w-xs hidden lg:block">{row.status}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
