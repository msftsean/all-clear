import { ReactNode } from 'react'

// ---------------------------------------------------------------------------
// Presenter quick-reference: 3-hour run of show, the three lanes, and the
// say-it-verbatim talk tracks for Slide 10 (Three Lanes) and Slide 21 (Pick a
// Door). Built so a distracted presenter can glance and find their place fast.
// AJCU Pre-Conference Workshop — Fordham Lincoln Center, LAW 3-09, 2026-06-01.
// ---------------------------------------------------------------------------

const runOfShow = [
  { time: '1:00–1:08', block: 'Open & frame', lead: 'Sean', min: 8 },
  { time: '1:08–1:22', block: 'The pattern — three agents', lead: 'Sean', min: 14 },
  { time: '1:22–1:32', block: 'Live demo · Card D', lead: 'Jake', min: 10 },
  { time: '1:32–1:40', block: 'Form teams · pick a card', lead: 'All', min: 8 },
  { time: '1:40–2:40', block: 'Build sprint 1', lead: 'Teams + coaches', min: 60 },
  { time: '2:40–2:50', block: 'Break', lead: '—', min: 10 },
  { time: '2:50–3:05', block: 'Build sprint 2 · harden', lead: 'Teams + coaches', min: 15 },
  { time: '3:05–3:55', block: 'Demos · 5 × 10 min', lead: 'Teams', min: 50 },
  { time: '3:55–4:00', block: 'Close', lead: 'Sean', min: 5 },
]

const lanes = [
  {
    name: 'Mock',
    tag: '🟡 everyone starts here',
    verbatim:
      '"Start in Mock. Every team, minute one. It runs the entire app on your laptop with zero Azure credentials — completely offline and completely deterministic. You launch the backend in mock mode and you immediately have working routing, the safety overrides, and PII redaction all firing. No tokens spent, same answer every time. This is your known-good baseline — if anything ever looks weird in the cloud later, you come back here to see what ‘correct’ looks like."',
    plain: 'Local, offline, repeatable. Your first run and your safety net.',
    tradeoff: 'You’re proving the brain — the decisions — not the live plumbing.',
  },
  {
    name: 'Self-Serve',
    tag: '🔵 graduate to real Azure ⭐ default',
    verbatim:
      '"When the brain works, you graduate to Self-Serve. This is the real load: one command — azd up — provisions your own Azure OpenAI, AI Search, and Container Apps and deploys the app into your resource group. The whole point of today’s setup is that this is one command, not a lab. And here’s the tell that it worked: your live deployment should behave exactly like the mock baseline you already trust."',
    plain: 'azd up into your own sponsorship resource group — a real artifact you keep.',
    tradeoff: 'A few minutes of provisioning up front — but it’s yours, and it goes home to your campus on Monday.',
  },
  {
    name: 'Shared',
    tag: '🟢 hosted shortcut — confirm it’s live',
    verbatim:
      '"And if your team would rather not provision anything at all, there’s the Shared lane — a hosted backend that’s already up, so you write agent logic on top of a stack someone else is running. Fastest possible start; you just don’t own the environment."',
    plain: 'A pre-stood-up hosted backend; zero provisioning.',
    tradeoff: 'You share it, so you can’t take that exact instance home — that’s what Self-Serve is for.',
  },
]

const slide10Beats = [
  {
    h: 'Opening line (say this first)',
    lines: [
      '"We just saw the enemy on the last slide — 285 minutes of setup against 165 minutes of actual building. In a three-hour workshop, the configuration can eat more than the whole session. So we’re not going to let it. There are three lanes to a working agent, and your team just picks the one that fits."',
    ],
  },
  {
    h: 'Beat 1 — Frame it as on-ramps, not a tech choice',
    lines: [
      '"These aren’t three different products. They’re three on-ramps to the same finish line — a working agent by 3:00. The difference is only how much cloud you want under you while you build. Let me give you all three in one breath, fastest-start to most-control."',
    ],
  },
  {
    h: 'Transition (say this last)',
    lines: [
      '"Three lanes, one finish line. Most of you will start in Mock to get the decisions right, then push to your own Azure with azd up. Your coaches will steer you. Let’s talk about what you get to skip — and what you absolutely keep."',
    ],
  },
]

const slide10IfAsked = [
  ['"Which lane should my team use?"', 'Start in Mock — everyone — to confirm your logic. Then run azd up for the live version. Shared is only if you want to skip provisioning entirely.'],
  ['"Why mock first instead of just deploying?"', 'Because mock is deterministic and free. You get your routing and safety right with zero tokens and zero cloud variables, then deploy with confidence — live should match the baseline.'],
  ['"What does azd up actually stand up?"', 'Azure OpenAI with the GPT-4.1, realtime, and embedding models, AI Search, and Container Apps, plus the backend and frontend — in one command, into your own resource group.'],
  ['"What if azd up fails?" (only if pressed)', 'Almost always one of three things — model quota, resource-group permissions, or an unregistered provider. Your coach has the runbook with the exact fix for each. You won’t lose momentum — your mock baseline is still running.'],
]

interface Card {
  letter: string
  title: string
  badge?: string
  pattern: string
  verbatim: string
}

const cards: Card[] = [
  {
    letter: 'A',
    title: 'The Quiet Crisis',
    pattern: 'Whole-person overlap + a safety escalation, with no gating.',
    verbatim:
      '"A — the Quiet Crisis. The pattern: whole-person overlap plus a safety escalation, with no gating. A first-year writes: ‘I haven’t been to class in two weeks. I don’t think I belong here. I’ve been crying at night. I don’t know who to talk to.’ This student never actually asks for help — that’s the point. Your agent has to recognize distress that isn’t labeled, route primarily to Student Wellness, surface the crisis line, and offer a chaplain as a parallel path. Never make a student earn clinical care by passing through a faith conversation first. Parallel paths, not gates."',
  },
  {
    letter: 'B',
    title: 'The Aid Cliff',
    pattern: 'Multi-intent overlap + an autonomous, high-priority ticket.',
    verbatim:
      '"B — the Aid Cliff. The pattern: multi-intent overlap plus an autonomous, high-priority ticket. ‘My mom lost her job last month. Can I get more aid? Also I’m thinking of dropping a class — does that hurt my package?’ Two offices, one student, one breath. The agent sees the overlap the student can’t: it routes to financial aid as the blocker and files a high-priority appeals ticket with the student’s story attached. Drop the wrong class and you lose the package — so the agent routes on consequence, not keywords."',
  },
  {
    letter: 'C',
    title: 'The Discernment',
    pattern: 'Offer, don’t auto-create — an opt-in human handoff.',
    verbatim:
      '"C — the Discernment. The pattern: offer, don’t auto-create — an opt-in human handoff. A senior: ‘I’m thinking about a year of service after graduation. JVC, or take the consulting job? Can someone help me think it through?’ This isn’t a ticket — it’s a conversation a human should have. The agent routes to Campus Ministry, surfaces discernment groups and a 1:1 chaplain, and does NOT auto-create a ticket — it offers one. The restraint is the cura personalis. It offers a person; it doesn’t file paperwork on someone’s vocation."',
  },
  {
    letter: 'D',
    title: 'The Phishing Storm',
    badge: '🟢 LIVE DEMO',
    pattern: 'One message, two parallel actions — a dual ticket.',
    verbatim:
      '"D — the Phishing Storm — the one you just watched run live. The pattern: one message, two parallel actions — a dual ticket. ‘My password isn’t working and I just got an email saying my account is locked. I clicked the link.’ One message, two emergencies. The agent can’t stop at the obvious one — it handles the IT reset and fires a security-incident workflow because of the click. Two tickets: one to IT, one to security. ‘I clicked the link’ changes everything — the agent acts on the second signal even though the student only asked about the first."',
  },
  {
    letter: 'E',
    title: 'Mass of the Holy Spirit',
    badge: '🟡 WARMUP',
    pattern: 'The simplest A-to-B routing, plus an inclusive welcome.',
    verbatim:
      '"E — Mass of the Holy Spirit — the warmup. The pattern: the simplest A-to-B routing, plus an inclusive welcome. ‘When is the Mass of the Holy Spirit? Also, I’m not Catholic — am I welcome?’ The simplest case, and the one that says the most about who we are: Campus Ministry routing with an interfaith welcome baked right into the response. Campus Ministry serves students of all faiths and none — that welcome isn’t a nicety, it’s the rule. If your team is newer, start here."',
  },
  {
    letter: 'F',
    title: 'The Multilingual Family',
    pattern: 'Language detection + a multilingual response.',
    verbatim:
      '"F — the Multilingual Family. The pattern: language detection plus a multilingual response. ‘Mi mamá quiere saber cuándo es el día de orientación para padres.’ The student isn’t the only person the university serves. The agent detects Spanish, answers in Spanish, and routes to General/Mission with a parent-orientation article. Cura personalis includes the family — the agent meets the parent in their language, not ours."',
  },
]

const slide21IfAsked = [
  ['"Can two teams take the same card?"', 'Sure — you’ll be amazed how different two agents are for the same message. But try to spread across the doors so we see all six patterns at demo time.'],
  ['"Is Card D off-limits since it was the live demo?"', 'Take it if you want — seeing it run doesn’t mean it’s easy. D has the richest logic on the board: two parallel actions from one message.'],
  ['"Which is the easiest to start with?"', 'E, the warmup — simplest routing plus the interfaith welcome. Get a clean win there, then reach for B or D for the harder builds.'],
  ['"How ‘done’ does it need to be?"', 'Working beats perfect. If your routing is right and your escalation actually fires on stage — observed, not described — you’ve nailed the rubric.'],
]

function Verbatim({ children }: { children: ReactNode }) {
  return (
    <blockquote className="border-l-4 border-iu-crimson/60 bg-iu-crimson/5 pl-4 pr-3 py-2 my-2 text-dark-text italic leading-relaxed rounded-r">
      {children}
    </blockquote>
  )
}

function SectionTitle({ children, sub }: { children: ReactNode; sub?: string }) {
  return (
    <div className="mb-4 mt-12 first:mt-0">
      <h3 className="text-2xl font-semibold tracking-tight text-dark-text">{children}</h3>
      {sub && <p className="text-ink/60 mt-1">{sub}</p>}
    </div>
  )
}

function IfAsked({ items }: { items: string[][] }) {
  return (
    <div className="mt-5 bg-surface-muted rounded-xl p-5">
      <p className="font-semibold text-dark-text mb-3">🛟 If asked / safety net</p>
      <dl className="space-y-3">
        {items.map(([q, a]) => (
          <div key={q}>
            <dt className="font-medium text-brand">{q}</dt>
            <dd className="text-ink/75 leading-relaxed">→ {a}</dd>
          </div>
        ))}
      </dl>
    </div>
  )
}

export default function RunOfShow() {
  return (
    <div role="tabpanel" id="run-of-show-panel" aria-labelledby="run-of-show-tab">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-3xl font-semibold tracking-tight text-dark-text mb-2">
          Run of Show & Talk Track
        </h2>
        <p className="text-xl text-ink/70 mb-6">
          Presenter quick-reference — for when you get distracted. AJCU Pre-Conference
          Workshop · Fordham Lincoln Center, LAW 3-09 · Mon Jun 1, 2026 · 1:00–4:00 PM.
        </p>

        <div className="callout border-brand/30 bg-brand/5 mb-10">
          <p className="text-dark-text leading-relaxed">
            <strong>azd-first.</strong> Provision once, then build. Everyone starts in
            <strong> Mock</strong> (offline, deterministic, zero credentials) to get the
            decisions right, then graduates to <strong>Self-Serve</strong> with one
            command — <code className="px-1 bg-surface-muted rounded">azd up</code> — into
            their own resource group. The bulk of the afternoon is two build sprints and
            team demos, not configuration.
          </p>
        </div>

        {/* ---- Live demo cheat-sheet (Card D) ---- */}
        <div className="callout border-iu-crimson/40 bg-iu-crimson/5 mb-10">
          <p className="text-sm font-bold uppercase tracking-wider text-iu-crimson mb-2">
            🎤 Live Demo · Card D — Phishing Storm <span className="font-medium normal-case tracking-normal text-ink/60">(1:22–1:32 · Jake drives)</span>
          </p>
          <p className="text-dark-text leading-relaxed mb-3">
            Open the live app and type this <strong>exact</strong> message into the chat:
          </p>
          <blockquote className="border-l-4 border-iu-crimson/60 bg-white/70 pl-4 pr-3 py-3 my-2 text-dark-text rounded-r font-mono text-sm">
            My password isn&apos;t working and I just got an email saying my account is
            locked. I clicked the link.
          </blockquote>
          <p className="text-dark-text leading-relaxed mt-3">
            <strong>What the room sees</strong> (verified live, deterministic): routes to
            <strong> IT</strong> → <strong>creates a ticket</strong> → returns
            <strong> 3 knowledge articles</strong>. The teaching point: one message, the
            agent acts on the second signal — <em>&ldquo;I clicked the link&rdquo;</em> —
            not just the obvious password reset.
          </p>
          <p className="text-dark-text leading-relaxed mt-3">
            <strong>Backup safety beat</strong> (optional, shows the override): type
            <em> &ldquo;I want to kill myself&rdquo;</em> → escalates to a human + the
            <strong> 988</strong> line, and never answers a crisis with self-service
            articles.
          </p>
          <div className="mt-4 grid sm:grid-cols-2 gap-3 text-sm">
            <div className="bg-white/60 rounded-lg p-3">
              <p className="font-semibold text-dark-text mb-1">🔗 Live app</p>
              <a
                href="https://frontdoor-x5wif2k353lda-frontend.calmdune-4c8e6d87.eastus2.azurecontainerapps.io"
                className="text-brand underline break-all"
                target="_blank"
                rel="noreferrer"
              >
                frontdoor-x5wif2k353lda-frontend…azurecontainerapps.io
              </a>
            </div>
            <div className="bg-white/60 rounded-lg p-3">
              <p className="font-semibold text-iu-crimson mb-1">⚠️ Do NOT type live</p>
              <p className="text-ink/75 leading-relaxed">
                The <strong>Mass of the Holy Spirit</strong> (Card E) or Spanish lines —
                the live shared router sends them to IT. Demo <strong>Card D</strong> only.
              </p>
            </div>
          </div>
        </div>

        {/* ---- Run of show table ---- */}
        <SectionTitle sub="Source of truth for timing — also on the participant site.">
          3-Hour Run of Show
        </SectionTitle>
        <div className="overflow-x-auto rounded-xl border border-border shadow-sm">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-surface-muted text-left text-dark-text">
                <th className="py-2.5 px-4 font-semibold">Time</th>
                <th className="py-2.5 px-4 font-semibold">Block</th>
                <th className="py-2.5 px-4 font-semibold">Lead</th>
                <th className="py-2.5 px-4 font-semibold text-right">Min</th>
              </tr>
            </thead>
            <tbody>
              {runOfShow.map((r) => (
                <tr key={r.time} className="border-t border-border">
                  <td className="py-2.5 px-4 font-mono text-ink/70 whitespace-nowrap">{r.time}</td>
                  <td className="py-2.5 px-4 text-dark-text font-medium">{r.block}</td>
                  <td className="py-2.5 px-4 text-ink/70">{r.lead}</td>
                  <td className="py-2.5 px-4 text-right text-ink/70">{r.min}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* ---- Three lanes ---- */}
        <SectionTitle sub="Three on-ramps, one finish line — a working agent by 3:00.">
          Three Lanes to Scenario-Ready
        </SectionTitle>
        <div className="space-y-4">
          {lanes.map((lane) => (
            <div key={lane.name} className="bg-surface border border-border rounded-xl p-5 shadow-sm">
              <div className="flex flex-wrap items-baseline gap-2 mb-1">
                <h4 className="text-lg font-semibold text-dark-text">{lane.name}</h4>
                <span className="text-xs text-ink/60">{lane.tag}</span>
              </div>
              <Verbatim>{lane.verbatim}</Verbatim>
              <p className="text-sm text-ink/75 mt-2">
                <strong className="text-dark-text">What it is:</strong> {lane.plain}
              </p>
              <p className="text-sm text-ink/75">
                <strong className="text-dark-text">Trade-off:</strong> {lane.tradeoff}
              </p>
            </div>
          ))}
        </div>
        <div className="callout border-iu-crimson/30 bg-iu-crimson/5 mt-4">
          <p className="text-dark-text leading-relaxed text-sm">
            <strong>⚠️ Confirm before stage:</strong> the <strong>Shared</strong> lane is
            the one detail the Student Runbook doesn’t document (it walks Mock → azd
            up). Check with Jake / Cloudforce at the top of the session: if a hosted shared
            backend is live for the room, keep the Shared beat; if not, present this as
            <strong> two lanes — Mock, then your own azd</strong>.
          </p>
        </div>

        {/* ---- Slide 10 talk track ---- */}
        <SectionTitle sub="~2.5 min · THE SOLUTION · 10 — “Three Lanes to Scenario-Ready.” If behind, cut the Shared beat to one sentence.">
          Slide 10 — Verbatim Talk Track
        </SectionTitle>
        {slide10Beats.map((b) => (
          <div key={b.h} className="mb-3">
            <p className="font-semibold text-dark-text">{b.h}</p>
            {b.lines.map((l, i) => (
              <Verbatim key={i}>{l}</Verbatim>
            ))}
          </div>
        ))}
        <p className="text-sm text-ink/70 mt-3">
          Then deliver each lane (Mock → Self-Serve → Shared) using the cards above —
          verbatim line, then “what it is,” then the trade-off.
        </p>
        <IfAsked items={slide10IfAsked} />

        {/* ---- Slide 21 talk track ---- */}
        <SectionTitle sub="~2.5 min · “Your Turn. Pick a Door.” Speak each card in ~20–25 sec. Name the pattern for every card even if you trim.">
          Slide 21 — Verbatim Talk Track
        </SectionTitle>
        <div className="mb-3">
          <p className="font-semibold text-dark-text">Frame the slide (say this to set it up)</p>
          <Verbatim>
            "Every card is one real student message — that’s the door. The agent
            behind it is the routing-and-escalation logic your team builds so that message
            reaches the right office, the right way. You’re not building six apps.
            You’re building one agent’s judgment, proven against the one scenario
            you pick. Six doors, and behind each one a different lesson in how an agent
            should decide."
          </Verbatim>
          <p className="font-semibold text-dark-text mt-3">Opening line (say this first)</p>
          <Verbatim>
            "Here’s where it becomes yours. Six real student messages — six doors. You
            already watched Card D run live a few minutes ago. Now your team picks one and
            builds the agent that answers it the way a Jesuit university should."
          </Verbatim>
        </div>

        <div className="space-y-4 mt-4">
          {cards.map((c) => (
            <div key={c.letter} className="bg-surface border border-border rounded-xl p-5 shadow-sm">
              <div className="flex flex-wrap items-baseline gap-2 mb-1">
                <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-brand text-surface font-bold text-sm shrink-0">
                  {c.letter}
                </span>
                <h4 className="text-lg font-semibold text-dark-text">{c.title}</h4>
                {c.badge && (
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-iu-crimson/10 text-iu-crimson">
                    {c.badge}
                  </span>
                )}
              </div>
              <p className="text-sm text-ink/70 mb-1">
                <strong className="text-dark-text">Pattern:</strong> {c.pattern}
              </p>
              <Verbatim>{c.verbatim}</Verbatim>
            </div>
          ))}
        </div>

        <div className="mb-3 mt-4">
          <p className="font-semibold text-dark-text">Transition (say this last)</p>
          <Verbatim>
            "You just saw D run live, and E is your gentlest warmup if you’re new. So
            pick your door — A, B, C, E, or F, or take on D yourselves. Six doors, five
            teams, one working agent by 3:00. Pick your door, and build the agent behind
            it."
          </Verbatim>
        </div>
        <IfAsked items={slide21IfAsked} />
      </div>
    </div>
  )
}
