import { useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';

/* -------------------------------------------------------------------------- */
/* Small presentational helpers — built only from existing theme tokens.       */
/* (maroon / deep-maroon / gold / cream / deep-cream / ink, font-mono, etc.)   */
/* -------------------------------------------------------------------------- */

/** Inline copy-to-clipboard code block, styled on the deep-maroon theme. */
function CodeBlock({ code, label }: { code: string; label?: string }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      /* Clipboard unavailable (e.g. insecure context) — fail silently. */
    }
  }

  return (
    <div className="mt-3">
      {label && (
        <p className="text-xs font-semibold uppercase tracking-wide text-ink/50 mb-1">
          {label}
        </p>
      )}
      <div className="relative group">
        <pre className="overflow-x-auto rounded-lg bg-deep-maroon text-cream font-mono text-xs sm:text-sm leading-relaxed p-4 pr-16 border border-maroon">
          <code>{code}</code>
        </pre>
        <button
          type="button"
          onClick={copy}
          aria-label={copied ? 'Copied' : 'Copy code'}
          className="absolute top-2 right-2 rounded px-2 py-1 text-xs font-medium bg-gold/90 text-deep-maroon hover:bg-gold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cream transition-colors"
        >
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
    </div>
  );
}

type CalloutTone = 'info' | 'warn' | 'danger';

const CALLOUT_STYLES: Record<CalloutTone, { wrap: string; badge: string; icon: ReactNode }> = {
  info: {
    wrap: 'bg-cream border-gold',
    badge: 'bg-gold/20 text-maroon',
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="16" x2="12" y2="12" />
        <line x1="12" y1="8" x2="12.01" y2="8" />
      </svg>
    ),
  },
  warn: {
    wrap: 'bg-light-gold/10 border-light-gold',
    badge: 'bg-light-gold/25 text-maroon',
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
        <line x1="12" y1="9" x2="12" y2="13" />
        <line x1="12" y1="17" x2="12.01" y2="17" />
      </svg>
    ),
  },
  danger: {
    wrap: 'bg-maroon/5 border-maroon',
    badge: 'bg-maroon/15 text-maroon',
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="10" />
        <line x1="15" y1="9" x2="9" y2="15" />
        <line x1="9" y1="9" x2="15" y2="15" />
      </svg>
    ),
  },
};

/** Alert / gotcha box. Left-accent border + tinted background, theme tokens only. */
function Callout({
  tone = 'info',
  title,
  children,
}: {
  tone?: CalloutTone;
  title: string;
  children: ReactNode;
}) {
  const s = CALLOUT_STYLES[tone];
  return (
    <div className={`mt-4 rounded-lg border-l-4 ${s.wrap} p-4 shadow-sm`}>
      <div className="flex items-start gap-3">
        <span className={`mt-0.5 inline-flex shrink-0 items-center justify-center rounded-full p-1 ${s.badge}`}>
          {s.icon}
        </span>
        <div className="min-w-0">
          <p className="font-serif font-bold text-maroon">{title}</p>
          <div className="mt-1 text-sm text-ink/80 leading-relaxed space-y-2">{children}</div>
        </div>
      </div>
    </div>
  );
}

/** Inline code chip for short tokens within prose. */
function Code({ children }: { children: ReactNode }) {
  return (
    <code className="font-mono text-[0.85em] bg-deep-cream text-maroon rounded px-1.5 py-0.5">
      {children}
    </code>
  );
}

/** A single numbered step in an ordered list. */
function Step({ n, title, children }: { n: number; title: string; children: ReactNode }) {
  return (
    <li className="bg-white rounded-xl border border-deep-cream p-5 shadow-sm">
      <div className="flex items-start gap-4">
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gold text-maroon font-bold text-sm shadow-sm">
          {n}
        </span>
        <div className="min-w-0 flex-1">
          <h3 className="font-serif font-bold text-maroon text-lg">{title}</h3>
          <div className="mt-2 text-ink/80 leading-relaxed space-y-2">{children}</div>
        </div>
      </div>
    </li>
  );
}

/* -------------------------------------------------------------------------- */
/* Page                                                                        */
/* -------------------------------------------------------------------------- */

export default function StudentRunbook() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl sm:text-4xl font-serif font-bold text-maroon gold-rule">
        Student Runbook
      </h1>
      <p className="text-ink/80 leading-relaxed -mt-2">
        A participant guide to running the 47 Doors AJCU agent app. Start{' '}
        <strong>local-first</strong> (no Azure credentials, fully deterministic), then{' '}
        <strong>deploy to Azure</strong> for the full live load. Follow the steps in order — every
        command is copy-paste ready.
      </p>

      <Callout tone="info" title="Two ways to run this app">
        <p>
          <strong>Part A</strong> runs everything offline in <Code>MOCK_MODE</Code> — perfect for
          your first run. <strong>Part B</strong> provisions real Azure resources with{' '}
          <Code>azd</Code>. Do Part A first to make sure your machine is set up.
        </p>
      </Callout>

      {/* ---------------------------------------------------------------- */}
      {/* PART A                                                            */}
      {/* ---------------------------------------------------------------- */}
      <section aria-labelledby="part-a" className="mt-12">
        <div className="flex items-center gap-3">
          <span className="rounded-full bg-maroon text-cream font-serif font-bold text-sm px-3 py-1">
            Part A
          </span>
          <h2 id="part-a" className="font-serif text-2xl font-bold text-maroon">
            Local mock mode
          </h2>
        </div>
        <p className="mt-2 text-ink/70">
          Zero Azure credentials, deterministic responses, works fully offline.
        </p>

        <ol className="mt-6 space-y-4">
          <Step n={1} title="Clone the repo & set up the backend venv">
            <p>
              Clone the repository, move into <Code>backend</Code>, create a virtual environment, and
              install the Python dependencies.
            </p>
            <CodeBlock
              code={`git clone https://github.com/EstablishedCorp/47doors.git
cd 47doors/backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt`}
            />
          </Step>

          <Step n={2} title="Run the mock quickstart">
            <p>
              Launch the backend in mock mode. This runs offline — safety overrides, routing, and PII
              redaction all fire; the voice feature self-hides because there's no real Realtime
              deployment.
            </p>
            <CodeBlock code={`MOCK_MODE=true PYTHONPATH=. uvicorn app.main:app --port 8000`} />
            <p>
              The API is now live at <Code>http://localhost:8000</Code>.
            </p>
          </Step>

          <Step n={3} title="Optional — run the frontend locally">
            <p>
              In a second terminal, start the frontend dev server. It proxies API calls to the backend
              you started in Step 2.
            </p>
            <CodeBlock
              code={`cd 47doors/frontend
npm install
npm run dev`}
            />
          </Step>

          <Step n={4} title="Know what mock mode does (and doesn't) do">
            <p>
              In mock mode <strong>no real LLM is called</strong> — responses are deterministic and
              repeatable. That makes it ideal for your first run, for demos, and for tests: you get the
              same answer every time without spending a single token.
            </p>
            <Callout tone="info" title="Good for first run">
              <p>
                If something behaves oddly later in Azure, come back here. Mock mode is your known-good
                baseline.
              </p>
            </Callout>
          </Step>
        </ol>
      </section>

      {/* ---------------------------------------------------------------- */}
      {/* PART B                                                            */}
      {/* ---------------------------------------------------------------- */}
      <section aria-labelledby="part-b" className="mt-14">
        <div className="flex items-center gap-3">
          <span className="rounded-full bg-maroon text-cream font-serif font-bold text-sm px-3 py-1">
            Part B
          </span>
          <h2 id="part-b" className="font-serif text-2xl font-bold text-maroon">
            Deploy to Azure with azd
          </h2>
        </div>
        <p className="mt-2 text-ink/70">
          Full live load — real Azure OpenAI, AI Search, and Container Apps.
        </p>

        <ol className="mt-6 space-y-4">
          <Step n={1} title="Check the prerequisites">
            <p>You'll need:</p>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                The Azure CLI (<Code>az</Code>) and the Azure Developer CLI (<Code>azd</Code>)
                installed.
              </li>
              <li>
                <strong>Owner</strong> access on a resource group (your sponsorship RG).
              </li>
            </ul>
          </Step>

          <Step n={2} title="Authenticate & select the subscription">
            <p>Sign in and pick the sponsorship subscription.</p>
            <CodeBlock
              code={`az login
# Select the sponsorship subscription:
az account set --subscription "<your-sponsorship-subscription-id>"`}
            />
          </Step>

          <Step n={3} title="Point azd at your existing resource group">
            <p>
              Participants are <strong>Owner on their RG only</strong> and{' '}
              <strong>Reader on the subscription</strong>, so <Code>azd</Code> must deploy{' '}
              <em>into</em> an existing RG rather than creating one. Create an env and set the targets.
            </p>
            <CodeBlock
              code={`azd env new <name>
azd env set AZURE_SUBSCRIPTION_ID <your-subscription-id>
azd env set AZURE_LOCATION eastus2
azd env set AZURE_RESOURCE_GROUP <your-rg>`}
            />
          </Step>

          <Step n={4} title="Provision & deploy with azd up">
            <p>
              One command provisions and deploys everything: Azure OpenAI (<Code>gpt-4.1</Code>,{' '}
              <Code>gpt-realtime</Code>, <Code>text-embedding-ada-002</Code>), AI Search, Container
              Apps, and the backend + frontend.
            </p>
            <CodeBlock code={`azd up`} />
          </Step>

          <Step n={5} title="Watch out for three gotchas">
            <p>These trip up almost everyone. Read them before you debug.</p>

            <Callout tone="warn" title="(a) OpenAI quota — counter names drop hyphens">
              <p>
                If a model deployment fails, you're probably out of quota for that model. Check usage —
                note that counter names <strong>drop hyphens</strong> (e.g. <Code>gpt4.1</Code>, not{' '}
                <Code>gpt-4.1</Code>).
              </p>
              <CodeBlock code={`az cognitiveservices usage list -l eastus2`} />
            </Callout>

            <Callout tone="danger" title="(b) Owner-on-RG vs Reader-on-subscription">
              <p>
                <Code>azd</Code> <strong>cannot create a resource group</strong> for you — you don't
                have subscription-level write access. It must target your <em>existing</em> RG. If you
                skipped Step 3, <Code>azd up</Code> will fail trying to create one.
              </p>
            </Callout>

            <Callout tone="warn" title="(c) Register the resource providers">
              <p>
                Make sure the required resource providers are <strong>Registered</strong> on your
                subscription before <Code>azd up</Code>. If a provider shows{' '}
                <Code>NotRegistered</Code>, ask your subscription admin to register it (Reader can't).
              </p>
              <CodeBlock
                code={`az provider list --query "[?registrationState=='NotRegistered'].namespace" -o table`}
              />
            </Callout>
          </Step>

          <Step n={6} title="Seed the knowledge base">
            <p>
              The AI Search index must be seeded with embeddings. The OpenAI account has{' '}
              <strong>local auth disabled</strong> (managed-identity only), so first grant{' '}
              <strong>yourself</strong> the <Code>Cognitive Services OpenAI User</Code> role on the
              OpenAI resource, then run the seeder using your <Code>az login</Code> identity (no OpenAI
              key needed).
            </p>
            <CodeBlock
              label="1. Grant yourself the role on the OpenAI resource"
              code={`az role assignment create \\
  --assignee "<your-user-object-id>" \\
  --role "Cognitive Services OpenAI User" \\
  --scope "<openai-resource-id>"`}
            />
            <CodeBlock
              label="2. Set the environment & run the seeder"
              code={`export AZURE_SEARCH_ENDPOINT="https://<your-search>.search.windows.net"
export AZURE_SEARCH_KEY="<your-search-admin-key>"
export AZURE_OPENAI_ENDPOINT="https://<your-openai>.openai.azure.com"
export AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-ada-002"
# No OpenAI key — embeddings use your az login identity.
python scripts/seed_search_index.py --index-name knowledge-base`}
            />
          </Step>

          <Step n={7} title="Select the agent framework runtime">
            <p>
              Set <Code>AGENT_RUNTIME=sdk</Code> to use the OpenAI Agents SDK runtime — this is the
              default for the deployment.
            </p>
            <CodeBlock code={`azd env set AGENT_RUNTIME sdk`} />
          </Step>

          <Step n={8} title="Test the live deployment">
            <p>
              Open the deployed frontend URL (<Code>azd</Code> prints it when it finishes). Try two
              messages:
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                A <strong>financial-aid question</strong> — confirm it routes to Financial Aid.
              </li>
              <li>
                A <strong>crisis-phrasing message</strong> — confirm the safety override escalates and
                surfaces the <Code>988</Code> crisis line.
              </li>
            </ul>
            <Callout tone="info" title="You're done">
              <p>
                If both behave correctly, your live deployment matches the mock baseline from Part A —
                you're ready to demo.
              </p>
            </Callout>
          </Step>
        </ol>
      </section>

      <div className="text-center mt-12">
        <Link to="/" className="text-maroon hover:text-gold transition-colors font-medium">
          ← Back to all cards
        </Link>
      </div>
    </div>
  );
}
