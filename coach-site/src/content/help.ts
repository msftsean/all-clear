import type { Section } from './types'

// Source of truth: docs/quickstart/HEADSTART.md → "Pick your lane" (the three
// cold-start lanes) and "You are scenario-ready when…". Links out to the full
// guide for depth (FR-002, content-map.md).

export const help: Section = {
  id: 'help',
  title: 'Help Participants',
  order: 4,
  summary: 'The three cold-start lanes and the "scenario-ready" definition that keep blocked teams moving.',
  source: 'docs/quickstart/HEADSTART.md',
  blocks: [
    {
      kind: 'paragraph',
      text:
        'The head-start guide gets a cold team from zero to scenario-ready in minutes — the ' +
        'knowledge base is seeded and intent routing works out of the box — so their time goes to ' +
        'the six AJCU challenge scenarios, not setup. When a participant is stuck, point them at ' +
        'the first lane that fits.',
    },
    {
      kind: 'callout',
      tone: 'info',
      title: 'Day-0 (before the room) — 10 minutes',
      text:
        'Open GitHub Codespaces on the repo (Python 3.11, Node, and dependencies are preinstalled), ' +
        'sign in to GitHub Copilot in the Codespace, and — self-serve lane only — run azd auth login ' +
        'so azd can provision later.',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'Pick your lane',
    },
    {
      kind: 'paragraph',
      text: 'There are three ways to reach scenario-ready. Pick the first one that fits.',
    },
    {
      kind: 'lane',
      name: '🟢 Shared backend (coach-provisioned)',
      outcome: 'No Azure needed — uses the shared stack',
      detail:
        'Use when the coach has provisioned a shared stack and shared an AI Search + OpenAI ' +
        'endpoint/keys out-of-band (never committed). Put the values in a local .env, then run ' +
        'bash scripts/quickstart.sh — it seeds the index, verifies it, and runs the backend smoke ' +
        'check idempotently.',
    },
    {
      kind: 'lane',
      name: '🔵 Self-serve azd (your own stack)',
      outcome: 'Yes — needs your subscription',
      detail:
        'Use when a team wants its own Azure stack. Run azd up: it provisions infra and auto-seeds ' +
        'the index via the postprovision hook, so the knowledge base is seeded and searchable when ' +
        'provisioning finishes. The seed hook is non-fatal — if it hiccups, provisioning still ' +
        'succeeds and prints the exact manual re-run command.',
    },
    {
      kind: 'lane',
      name: '🟡 Mock / offline (zero Azure credentials)',
      outcome: 'No Azure needed at all',
      detail:
        'Use when a participant is blocked on Azure access (Conditional Access, quota). Run ' +
        'bash scripts/quickstart.sh --mock to validate the mock pipeline (intent classification + KB ' +
        'search) and the backend /api/health endpoint with USE_MOCK_MODE=true — no credentials required.',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'You are scenario-ready when…',
    },
    {
      kind: 'callout',
      tone: 'success',
      title: 'Definition of scenario-ready',
      text:
        'Live lanes: bash scripts/quickstart.sh exits 0 and prints the ✅ Scenario-ready banner, the ' +
        'verify step reports the seeded document count and a working keyword search, and the backend ' +
        'smoke check shows ✓ PASS. Mock lane: bash scripts/quickstart.sh --mock exits 0 with all ' +
        'three mock checks ✓ PASS. When the banner shows Scenario-ready, the knowledge base is ' +
        'seeded and intent routing works — go straight to the six AJCU challenge scenarios.',
    },
    {
      kind: 'link',
      label: 'Full Head-Start guide (docs/quickstart/HEADSTART.md)',
      href: 'https://github.com/EstablishedCorp/47doors/blob/main/docs/quickstart/HEADSTART.md',
    },
  ],
}
