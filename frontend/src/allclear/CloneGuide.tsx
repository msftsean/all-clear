/**
 * CloneGuide — "Get my latest work onto my local machine"
 * Three scenarios: first-time clone, already-cloned pull, GitHub Desktop GUI.
 */

import { useState } from "react";

const REPO_URL = "https://github.com/EstablishedCorp/all-clear";
const LATEST_COMMITS = [
  { hash: "5db4f4f", msg: "feat(ui): add CloneGuide page at ?page=clone" },
  { hash: "1338486", msg: "fix(admin): use safe FastAPI deps, Body() fix" },
  { hash: "941c4d1", msg: "fix(admin): align list_all_tickets signature" },
  { hash: "b83730b", msg: "feat(admin): wire lab US6+US7 — branding + tickets" },
  { hash: "84358d8", msg: "Redesign coach site visual system" },
];

interface Scenario {
  id: string;
  eyebrow: string;
  label: string;
  when: string;
  recommended: boolean;
  steps: { title: string; code?: string; note?: string }[];
}

const SCENARIOS: Scenario[] = [
  {
    id: "pull",
    eyebrow: "Already have it",
    label: "git pull",
    when: "You've cloned the repo before — just pull the latest commits.",
    recommended: true,
    steps: [
      {
        title: "Open your terminal in the repo folder",
        code: "cd all-clear",
      },
      {
        title: "Pull the latest work from main",
        code: "git pull origin main",
        note: "This fetches and merges every commit pushed during this session.",
      },
      {
        title: "Start the backend in mock mode",
        code: "cd backend\nsource .venv/bin/activate\nMOCK_MODE=true ENVIRONMENT=test uvicorn app.main:app --reload --port 8000",
      },
      {
        title: "Start the frontend (new terminal)",
        code: "cd frontend\nnpm install\nnpm run dev",
      },
    ],
  },
  {
    id: "clone",
    eyebrow: "First time",
    label: "git clone",
    when: "You've never cloned this repo on this machine.",
    recommended: false,
    steps: [
      {
        title: "Clone via HTTPS",
        code: `git clone ${REPO_URL}`,
        note: "If prompted for a password, use a GitHub Personal Access Token.",
      },
      {
        title: "Or clone with the GitHub CLI (easier auth)",
        code: "gh repo clone EstablishedCorp/all-clear",
        note: "Run `gh auth login` first if you haven't already.",
      },
      {
        title: "Enter the repo and run",
        code: "cd all-clear\ncd backend && python -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\nMOCK_MODE=true ENVIRONMENT=test uvicorn app.main:app --reload --port 8000",
      },
    ],
  },
  {
    id: "desktop",
    eyebrow: "No terminal",
    label: "GitHub Desktop",
    when: "Prefer a GUI — no command line needed.",
    recommended: false,
    steps: [
      {
        title: "Download GitHub Desktop",
        note: "desktop.github.com — available for macOS and Windows.",
      },
      {
        title: "Sign in with your GitHub account",
        note: "File → Options → Accounts → Sign In.",
      },
      {
        title: "If you already have the repo: Fetch & Pull",
        note: "Open the repo in Desktop → click 'Fetch origin' → then 'Pull origin'.",
      },
      {
        title: "If cloning for the first time",
        code: `Repository URL: ${REPO_URL}`,
        note: "File → Clone Repository → URL tab → paste the URL above.",
      },
    ],
  },
];

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={() => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }}
      className="ml-2 shrink-0 rounded-chip border border-paperline bg-paper2 px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-midwarm shadow-antimetal-soft transition-all hover:border-voice/40 hover:text-voice"
    >
      {copied ? "✓ copied" : "copy"}
    </button>
  );
}

function CodeBlock({ code }: { code: string }) {
  return (
    <div className="relative mt-2 flex items-start gap-2 rounded-bubble border border-paperline bg-paper px-4 py-3 shadow-antimetal-soft">
      <pre className="flex-1 overflow-x-auto font-mono text-[12.5px] leading-relaxed text-inkwarm whitespace-pre-wrap break-all">
        {code}
      </pre>
      <CopyButton text={code} />
    </div>
  );
}

function ScenarioCard({ scenario, isOpen, onToggle }: {
  scenario: Scenario;
  isOpen: boolean;
  onToggle: () => void;
}) {
  return (
    <div className={`rounded-card border transition-all duration-200 ${
      scenario.recommended
        ? "border-voice/40 shadow-antimetal-card bg-paper2"
        : "border-paperline bg-paper2 shadow-antimetal-soft"
    }`}>
      <button
        className="flex w-full items-start gap-4 rounded-card p-5 text-left"
        onClick={onToggle}
        aria-expanded={isOpen}
      >
        <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full border font-mono text-xs font-semibold ${
          scenario.recommended
            ? "border-voice/30 bg-voice/10 text-voice"
            : "border-paperline bg-paper text-midwarm"
        }`}>
          {scenario.recommended ? "★" : scenario.id === "clone" ? "2" : "3"}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-display text-[17px] font-semibold tracking-tight text-inkwarm">
              {scenario.label}
            </span>
            <span className={`rounded-chip px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wider ${
              scenario.recommended
                ? "bg-voice/10 text-voice"
                : "bg-paper text-midwarm border border-paperline"
            }`}>
              {scenario.eyebrow}
            </span>
          </div>
          <p className="mt-1 text-sm leading-relaxed text-midwarm">{scenario.when}</p>
        </div>
        <span className={`mt-1 shrink-0 font-mono text-xs text-midwarm transition-transform duration-200 ${isOpen ? "rotate-90" : ""}`}>
          ▶
        </span>
      </button>

      {isOpen && (
        <div className="border-t border-paperline px-5 pb-5 pt-4 animate-rise">
          <ol className="space-y-5">
            {scenario.steps.map((step, i) => (
              <li key={i} className="flex gap-3">
                <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-paperline bg-paper font-mono text-[10px] text-midwarm">
                  {i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-inkwarm">{step.title}</p>
                  {step.note && <p className="mt-0.5 text-xs text-midwarm">{step.note}</p>}
                  {step.code && <CodeBlock code={step.code} />}
                </div>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default function CloneGuide() {
  const [openId, setOpenId] = useState<string>("pull");

  return (
    <div className="flex h-full w-full flex-col bg-paper md:flex-row">
      {/* Left column — paper world */}
      <div className="z-10 flex h-full w-full flex-col border-r border-paperline bg-paper2 shadow-[rgba(0,39,80,0.04)_1px_0_0_0] md:w-[430px] md:flex-none overflow-y-auto">
        {/* Header */}
        <header className="flex items-center justify-between border-b border-paperline px-5 py-4">
          <div className="flex items-center gap-2.5">
            <svg width="24" height="24" viewBox="0 0 64 64" fill="none">
              <defs>
                <linearGradient id="ac-ring-g" x1="10" y1="54" x2="54" y2="10" gradientUnits="userSpaceOnUse">
                  <stop offset="0" stopColor="#0050F8"/>
                  <stop offset="1" stopColor="#5FBDF7"/>
                </linearGradient>
              </defs>
              <path d="M54.22 26.05 A23 23 0 1 1 41.72 11.16" stroke="url(#ac-ring-g)" strokeWidth="6" strokeLinecap="round" fill="none"/>
              <circle cx="41.72" cy="11.16" r="4" fill="#D0F100"/>
              <path d="M21 33 L29 41 L44 23" stroke="#D0F100" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
            </svg>
            <span className="font-display text-[21px] font-medium tracking-tight text-inkwarm">All Clear</span>
          </div>
          <span className="rounded-chip bg-paper px-2.5 py-1 font-mono text-[10px] text-midwarm shadow-antimetal-soft">
            ● get latest code
          </span>
        </header>

        {/* Intro */}
        <div className="border-b border-paperline px-5 py-4">
          <p className="eyebrow mb-1 text-midwarm">Your latest work</p>
          <p className="font-display text-[18px] font-semibold leading-snug tracking-tight text-inkwarm">
            Get your latest code to your local machine
          </p>
          <p className="mt-1.5 text-sm leading-relaxed text-midwarm">
            All your work is already pushed to{" "}
            <span className="font-mono text-[12px] text-inkwarm">main</span>.
            Pick the scenario that matches where you are.
          </p>
        </div>

        {/* Repo URL */}
        <div className="border-b border-paperline px-5 py-3">
          <p className="eyebrow mb-1.5 text-midwarm">Repository</p>
          <div className="flex items-center gap-2 rounded-bubble border border-paperline bg-paper px-3 py-2 shadow-antimetal-soft">
            <span className="flex-1 font-mono text-[11px] text-inkwarm truncate">{REPO_URL}</span>
            <CopyButton text={REPO_URL} />
          </div>
        </div>

        {/* Scenarios */}
        <div className="flex flex-col gap-3 p-5">
          {SCENARIOS.map((s) => (
            <ScenarioCard
              key={s.id}
              scenario={s}
              isOpen={openId === s.id}
              onToggle={() => setOpenId(openId === s.id ? "" : s.id)}
            />
          ))}
        </div>
      </div>

      {/* Right panel — night world */}
      <div className="flex flex-1 flex-col bg-night overflow-y-auto">
        <div className="border-b border-nline px-8 py-5">
          <p className="eyebrow text-ndim">Latest commits on main</p>
        </div>

        <div className="flex flex-1 items-start justify-center px-8 py-10">
          <div className="w-full max-w-lg space-y-6">

            {/* Quick answer card */}
            <div className="rounded-card border border-voice/30 bg-panel shadow-dark-glass p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="flex h-9 w-9 items-center justify-center rounded-full border border-voice/40 bg-voice/10">
                  <span className="font-mono text-sm text-voice">★</span>
                </div>
                <div>
                  <p className="eyebrow text-voice mb-0.5">Quickest path</p>
                  <p className="font-display text-[20px] font-semibold tracking-tight text-nink">
                    Already cloned? Just pull.
                  </p>
                </div>
              </div>
              <p className="text-sm text-ndim leading-relaxed mb-4">
                Your work was pushed to <span className="font-mono text-[12px] text-nink">main</span> during this session.
                If you cloned the repo before, two commands get you fully up to date.
              </p>
              <div className="space-y-2">
                {[
                  { cmd: "cd all-clear", label: "enter repo" },
                  { cmd: "git pull origin main", label: "sync" },
                ].map(({ cmd, label }, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="flex flex-1 items-center gap-2 rounded-bubble border border-nline bg-night/50 px-3 py-1.5">
                      <span className="flex-1 font-mono text-[13px] text-nink">{cmd}</span>
                      <span className="font-mono text-[10px] text-ndim">{label}</span>
                    </div>
                    <CopyButton text={cmd} />
                  </div>
                ))}
              </div>
            </div>

            {/* Recent commits */}
            <div className="rounded-card border border-nline bg-panel/60 shadow-dark-glass p-5">
              <p className="eyebrow text-ndim mb-4">What you'll get</p>
              <div className="space-y-2">
                {LATEST_COMMITS.map((c, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <span className="mt-0.5 font-mono text-[11px] text-voice shrink-0">{c.hash}</span>
                    <span className="text-xs text-ndim leading-snug">{c.msg}</span>
                  </div>
                ))}
              </div>
              <div className="mt-4 pt-3 border-t border-nline flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-clear animate-blink shrink-0" />
                <span className="font-mono text-[10px] text-ndim">All commits pushed to origin/main</span>
              </div>
            </div>

            {/* Never cloned callout */}
            <div className="rounded-card border border-nline bg-panel/40 p-5">
              <p className="eyebrow text-ndim mb-2">First time on this machine?</p>
              <p className="text-xs text-ndim leading-relaxed mb-3">
                Clone first, then you're set for all future pulls.
              </p>
              <div className="flex items-center gap-2 rounded-bubble border border-nline bg-night/60 px-3 py-2">
                <span className="flex-1 font-mono text-[12px] text-nink">git clone {REPO_URL}</span>
                <CopyButton text={`git clone ${REPO_URL}`} />
              </div>
            </div>

            <p className="text-center font-mono text-[10px] text-ndim/50 uppercase tracking-wider">
              All Clear · EstablishedCorp/all-clear · {new Date().getFullYear()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
