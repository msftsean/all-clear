# All Clear — Incident Triage Reference

A static, mobile-first reference site for incident responders. It demonstrates how to turn surge signals into deduplicated incidents, route work to accountable queues, apply severity and SLA policy, publish safe sitreps, and keep ClearBoard current.

## Quick start

```bash
cd hackathon-site
npm install
npm run dev
```

## Validate

```bash
npm run typecheck
npm run build
npm run test:e2e
```

## Routes

| Path | Purpose |
| --- | --- |
| `/` | ClearBoard landing page and six incident scenarios |
| `/incidents/:slug` | Scenario detail with triage references |
| `/workflow` | Signal-to-response triage workflow |
| `/queues` | Accountable response queues |
| `/policy` | Severity, SLA, safety, and sitrep guardrails |
| `/shift-plan` | First-response operational cadence |
| `/runbook` | Operator triage runbook |

## Stack

Vite, React 18, TypeScript, Tailwind CSS, React Router, and Playwright. The application is a static SPA; `staticwebapp.config.json` provides the navigation fallback for deep links.

## Content model

`src/data/cards.ts` contains the six scenarios. Each scenario includes its incoming signal, expected incident outcome, ownership, severity/SLA guidance, and reference material.
