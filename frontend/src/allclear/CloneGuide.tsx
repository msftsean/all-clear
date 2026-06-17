/**
 * CloneGuide — All Clear-branded page showing three ways to clone the
 * EstablishedCorp/all-clear repository to a local machine.
 *
 * Aesthetic: mirrors the All Clear "paper world" sidebar exactly —
 * paper / paper2 / paperline / inkwarm / midwarm / voice tokens,
 * Google Sans Flex display, Google Sans Code mono, antimetal shadows,
 * nebula radial background, dot grid.
 */

import { useState } from "react";

const REPO_URL = "https://github.com/EstablishedCorp/all-clear";
const REPO_SSH = "git@github.com:EstablishedCorp/all-clear.git";

interface Method {
  id: string;
  label: string;
  eyebrow: string;
  recommended: boolean;
  summary: string;
  steps: { title: string; code?: string; note?: string }[];
  pros: string[];
  cons: string[];
}

const METHODS: Method[] = [
  {
    id: "gh-cli",
    label: "GitHub CLI",
    eyebrow: "Recommended",
    recommended: true,
    summary:
      "One command. The GitHub CLI (`gh`) authenticates, clones, and sets up the remote — no token juggling, no SSH key setup required.",
    steps: [
      {
        title: "Install the CLI",
        code: "# macOS\nbrew install gh\n\n# Windows (winget)\nwinget install GitHub.cli\n\n# Linux — see cli.github.com",
        note: "Already installed? Skip this step.",
      },
      {
        title: "Authenticate once",
        code: "gh auth login",
        note: "Follow the browser prompt — takes about 30 seconds.",
      },
      {
        title: "Clone the repo",
        code: "gh repo clone EstablishedCorp/all-clear",
      },
      {
        title: "Run locally in mock mode",
        code: "cd all-clear/backend\npython -m venv .venv && source .venv/bin/activate\npip install -r requirements.txt\nMOCK_MODE=true ENVIRONMENT=test uvicorn app.main:app --reload --port 8000",
      },
    ],
    pros: [
      "No token or SSH key setup",
      "Works behind most corporate firewalls (HTTPS)",
      "One-time auth — works for all future GitHub repos",
    ],
    cons: ["Requires installing the CLI (~40 MB)"],
  },
  {
    id: "https",
    label: "HTTPS + Personal Access Token",
    eyebrow: "Method 2",
    recommended: false,
    summary:
      "Clone over HTTPS using a GitHub Personal Access Token (PAT). Works everywhere without additional tools — just `git`.",
    steps: [
      {
        title: "Create a PAT",
        note:
          "GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens. Grant read access to EstablishedCorp/all-clear.",
      },
      {
        title: "Clone",
        code: "git clone https://github.com/EstablishedCorp/all-clear",
        note: "When prompted for a password, enter your PAT (not your GitHub password).",
      },
      {
        title: "Cache credentials (optional)",
        code: "git config --global credential.helper store",
        note: "Avoids re-entering the token on every push/pull.",
      },
    ],
    pros: [
      "Works on any machine with `git` installed",
      "No extra tools needed",
      "Fine-grained permission scoping",
    ],
    cons: [
      "PATs expire and need renewal",
      "Token must be stored securely",
      "Manual browser steps to generate",
    ],
  },
  {
    id: "ssh",
    label: "SSH Key",
    eyebrow: "Method 3",
    recommended: false,
    summary:
      "Clone over SSH using an ed25519 key pair. Most secure option and avoids token expiry — ideal for developers who already have SSH keys configured.",
    steps: [
      {
        title: "Generate a key (if you don't have one)",
        code: 'ssh-keygen -t ed25519 -C "your@email.com"',
        note: "Skip if you already have ~/.ssh/id_ed25519.",
      },
      {
        title: "Add public key to GitHub",
        code: "cat ~/.ssh/id_ed25519.pub",
        note: "Copy output → GitHub → Settings → SSH Keys → New SSH Key.",
      },
      {
        title: "Clone",
        code: `git clone ${REPO_SSH}`,
      },
    ],
    pros: [
      "No expiring tokens",
      "Most secure — private key never leaves your machine",
      "Seamless once set up",
    ],
    cons: [
      "Requires SSH port 22 (blocked on some networks)",
      "Initial setup takes 5–10 minutes",
      "Per-machine key management",
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
      title="Copy to clipboard"
    >
      {copied ? "✓ copied" : "copy"}
    </button>
  );
}

function CodeBlock({ code }: { code: string }) {
  return (
    <div className="relative mt-2 flex items-start gap-2 rounded-bubble border border-paperline bg-paper px-4 py-3 shadow-antimetal-soft">
      <pre className="flex-1 overflow-x-auto font-mono text-[12.5px] leading-relaxed text-inkwarm">
        {code}
      </pre>
      <CopyButton text={code} />
    </div>
  );
}

function MethodCard({ method, isOpen, onToggle }: { method: Method; isOpen: boolean; onToggle: () => void }) {
  return (
    <div
      className={`rounded-card border transition-all duration-200 ${
        method.recommended
          ? "border-voice/40 shadow-antimetal-card bg-paper2"
          : "border-paperline bg-paper2 shadow-antimetal-soft"
      }`}
    >
      {/* Header */}
      <button
        className="flex w-full items-start gap-4 rounded-card p-5 text-left"
        onClick={onToggle}
        aria-expanded={isOpen}
      >
        {/* Eyebrow + number bubble */}
        <div
          className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full border font-mono text-xs font-semibold ${
            method.recommended
              ? "border-voice/30 bg-voice/10 text-voice"
              : "border-paperline bg-paper text-midwarm"
          }`}
        >
          {method.recommended ? "★" : method.id === "https" ? "2" : "3"}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-display text-[17px] font-semibold tracking-tight text-inkwarm">
              {method.label}
            </span>
            {method.recommended && (
              <span className="rounded-chip bg-voice/10 px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-voice">
                Recommended
              </span>
            )}
          </div>
          <p className="mt-1 text-sm leading-relaxed text-midwarm line-clamp-2">
            {method.summary}
          </p>
        </div>

        <span
          className={`mt-1 shrink-0 font-mono text-xs text-midwarm transition-transform duration-200 ${isOpen ? "rotate-90" : ""}`}
        >
          ▶
        </span>
      </button>

      {/* Expanded content */}
      {isOpen && (
        <div className="border-t border-paperline px-5 pb-5 pt-4 animate-rise">
          {/* Steps */}
          <ol className="space-y-5">
            {method.steps.map((step, i) => (
              <li key={i} className="flex gap-3">
                <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-paperline bg-paper font-mono text-[10px] text-midwarm">
                  {i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-inkwarm">{step.title}</p>
                  {step.note && (
                    <p className="mt-0.5 text-xs text-midwarm">{step.note}</p>
                  )}
                  {step.code && <CodeBlock code={step.code} />}
                </div>
              </li>
            ))}
          </ol>

          {/* Pros / Cons */}
          <div className="mt-5 grid grid-cols-2 gap-3">
            <div className="rounded-bubble border border-paperline bg-paper p-3">
              <p className="eyebrow mb-2 text-clear">Pros</p>
              <ul className="space-y-1">
                {method.pros.map((p, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-xs text-midwarm">
                    <span className="mt-0.5 text-clear">✓</span> {p}
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-bubble border border-paperline bg-paper p-3">
              <p className="eyebrow mb-2 text-sev2">Cons</p>
              <ul className="space-y-1">
                {method.cons.map((c, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-xs text-midwarm">
                    <span className="mt-0.5 text-sev2">–</span> {c}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function CloneGuide() {
  const [openId, setOpenId] = useState<string>("gh-cli");

  return (
    <div className="flex h-full w-full flex-col bg-paper md:flex-row">
      {/* ---- Left column (matches BriefingRoom sidebar width) ---- */}
      <div className="z-10 flex h-full w-full flex-col border-r border-paperline bg-paper2 shadow-[rgba(0,39,80,0.04)_1px_0_0_0] md:w-[430px] md:flex-none overflow-y-auto">
        {/* Header */}
        <header className="flex items-center justify-between border-b border-paperline px-5 py-4">
          <div className="flex items-center gap-2.5">
            <svg width="24" height="24" viewBox="0 0 64 64" fill="none" aria-label="All Clear">
              <defs>
                <linearGradient id="ac-ring-sm" x1="10" y1="54" x2="54" y2="10" gradientUnits="userSpaceOnUse">
                  <stop offset="0" stopColor="#0050F8"/>
                  <stop offset="1" stopColor="#5FBDF7"/>
                </linearGradient>
              </defs>
              <path d="M54.22 26.05 A23 23 0 1 1 41.72 11.16" stroke="url(#ac-ring-sm)" strokeWidth="6" strokeLinecap="round" fill="none"/>
              <circle cx="41.72" cy="11.16" r="4" fill="#D0F100"/>
              <path d="M21 33 L29 41 L44 23" stroke="#D0F100" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
            </svg>
            <span className="font-display text-[21px] font-medium tracking-tight text-inkwarm">
              All Clear
            </span>
          </div>
          <span className="rounded-chip bg-paper px-2.5 py-1 font-mono text-[10px] text-midwarm shadow-antimetal-soft">
            ● repository setup
          </span>
        </header>

        {/* Intro */}
        <div className="border-b border-paperline px-5 py-4">
          <p className="eyebrow mb-1 text-midwarm">Getting Started</p>
          <p className="font-display text-[18px] font-semibold leading-snug tracking-tight text-inkwarm">
            Clone to your local machine
          </p>
          <p className="mt-1.5 text-sm leading-relaxed text-midwarm">
            Three ways to get <span className="font-mono text-[12px] text-inkwarm">EstablishedCorp/all-clear</span> running locally. Choose the method that fits your setup.
          </p>
        </div>

        {/* Repo URL quick-copy */}
        <div className="border-b border-paperline px-5 py-3">
          <p className="eyebrow mb-1.5 text-midwarm">Repository</p>
          <div className="flex items-center gap-2 rounded-bubble border border-paperline bg-paper px-3 py-2 shadow-antimetal-soft">
            <span className="flex-1 font-mono text-[11px] text-inkwarm truncate">{REPO_URL}</span>
            <CopyButton text={REPO_URL} />
          </div>
        </div>

        {/* Methods */}
        <div className="flex flex-col gap-3 p-5">
          {METHODS.map((m) => (
            <MethodCard
              key={m.id}
              method={m}
              isOpen={openId === m.id}
              onToggle={() => setOpenId(openId === m.id ? "" : m.id)}
            />
          ))}
        </div>
      </div>

      {/* ---- Right panel: recommendation summary (night world) ---- */}
      <div className="flex flex-1 flex-col bg-night overflow-y-auto">
        {/* Canvas header */}
        <div className="border-b border-nline px-8 py-5">
          <p className="eyebrow text-ndim">Our Recommendation</p>
        </div>

        <div className="flex flex-1 items-start justify-center px-8 py-10">
          <div className="w-full max-w-lg">
            {/* Recommendation card */}
            <div className="rounded-card border border-nline bg-panel shadow-dark-glass p-7">
              <div className="flex items-center gap-3 mb-5">
                <div className="flex h-10 w-10 items-center justify-center rounded-full border border-voice/40 bg-voice/10">
                  <svg width="20" height="20" viewBox="0 0 64 64" fill="none">
                    <defs>
                      <linearGradient id="ac-rec" x1="10" y1="54" x2="54" y2="10" gradientUnits="userSpaceOnUse">
                        <stop offset="0" stopColor="#0050F8"/>
                        <stop offset="1" stopColor="#5FBDF7"/>
                      </linearGradient>
                    </defs>
                    <path d="M54.22 26.05 A23 23 0 1 1 41.72 11.16" stroke="url(#ac-rec)" strokeWidth="6" strokeLinecap="round" fill="none"/>
                    <circle cx="41.72" cy="11.16" r="4" fill="#D0F100"/>
                    <path d="M21 33 L29 41 L44 23" stroke="#D0F100" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                  </svg>
                </div>
                <div>
                  <p className="eyebrow text-voice mb-0.5">Best for this group</p>
                  <p className="font-display text-[22px] font-semibold tracking-tight text-nink">GitHub CLI</p>
                </div>
              </div>

              <p className="text-sm leading-relaxed text-ndim mb-6">
                Erik and the team are coming from a GitHub-native environment. The <span className="font-mono text-[12px] text-nink">gh</span> CLI authenticates through the browser in 30 seconds — no tokens to create, rotate, or store, and no SSH keys to provision per machine.
              </p>

              {/* 3-step summary */}
              <div className="space-y-3">
                {[
                  { cmd: "brew install gh", label: "Install" },
                  { cmd: "gh auth login", label: "Authenticate" },
                  { cmd: "gh repo clone EstablishedCorp/all-clear", label: "Clone" },
                ].map(({ cmd, label }, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-nline font-mono text-[10px] text-ndim">
                      {i + 1}
                    </span>
                    <div className="flex flex-1 items-center gap-2 rounded-bubble border border-nline bg-night/50 px-3 py-1.5">
                      <span className="flex-1 font-mono text-[12px] text-nink">{cmd}</span>
                      <span className="font-mono text-[10px] text-ndim">{label}</span>
                    </div>
                    <CopyButton text={cmd} />
                  </div>
                ))}
              </div>

              <div className="mt-6 rounded-bubble border border-clear/20 bg-clear/5 px-4 py-3">
                <p className="text-xs leading-relaxed text-ndim">
                  <span className="text-clear font-medium">Then run in mock mode</span> — zero Azure credentials needed. The entire pipeline runs offline against deterministic mock twins.
                </p>
                <div className="mt-2 rounded border border-nline bg-night/60 px-3 py-2">
                  <pre className="font-mono text-[11px] text-ndim leading-relaxed">{`cd all-clear/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
MOCK_MODE=true ENVIRONMENT=test \\
  uvicorn app.main:app --reload --port 8000`}</pre>
                </div>
              </div>
            </div>

            {/* Why not the others */}
            <div className="mt-5 rounded-card border border-nline bg-panel/60 p-5 shadow-dark-glass">
              <p className="eyebrow text-ndim mb-4">Why not the others?</p>
              <div className="space-y-3 text-sm text-ndim leading-relaxed">
                <div className="flex gap-2">
                  <span className="text-sev2 shrink-0 mt-0.5">–</span>
                  <div>
                    <span className="text-nink font-medium">HTTPS + PAT</span> — works fine, but tokens expire and each person needs to generate one manually. Adds friction before day one.
                  </div>
                </div>
                <div className="flex gap-2">
                  <span className="text-sev2 shrink-0 mt-0.5">–</span>
                  <div>
                    <span className="text-nink font-medium">SSH Keys</span> — most secure long-term, but requires per-machine key generation and corporate networks often block port 22. Adds 10+ minutes of setup per person.
                  </div>
                </div>
              </div>
            </div>

            {/* Footer note */}
            <p className="mt-5 text-center font-mono text-[10px] text-ndim/60 uppercase tracking-wider">
              All Clear · EstablishedCorp/all-clear · {new Date().getFullYear()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
