# All Clear operations companion

This React/Vite site is the demo and operator runbook for All Clear, an incident-triage workspace. It explains how signals become deduplicated incidents, how queues use SEV1–SEV4/SLA rules, and how operators use ClearBoard, safety controls, and voice/phone intake during a live response.

```bash
npm install
npm run dev
npm run typecheck
npm run build
```

The site is static and can be deployed to any Vite-compatible host. Authentication and API health checks are represented as operator-facing runbook steps rather than hard-coded environment claims.
