# All Clear Workshop Companion

A tab-based React and Tailwind CSS companion for teaching the All Clear incident-triage contract.

## Workshop Scope

The site follows one signal from intake to resolution and explains:

- **Signal, incident, report, and magnitude** as distinct domain objects
- The **QueryAgent -> RouterExecutor -> ActionAgent** pipeline
- Deterministic **dedup, SEV1-4, queue, SLA, and escalation** decisions
- Surge behavior through `ATTACH_TO_INCIDENT` and `OPEN_INCIDENT`
- **Bounded authority**, PII discipline, safety overrides, and cited situation reports
- Browser voice and phone as transports into the same signal contract
- **ClearBoard** as the live operating picture and all-clear terminal state

## Tech Stack

- React 18 with TypeScript
- Vite 5
- Tailwind CSS 3.4
- Fluent UI and Heroicons

## Local Development

Requires Node.js 18 or newer.

```bash
cd workshop-site
npm install
npm run dev
```

Open `http://localhost:5173`.

## Validation

```bash
npm run typecheck
npm run build
```

The production build is written to `dist/`.

## Structure

```text
workshop-site/
├── public/
│   └── staticwebapp.config.json
├── src/
│   ├── components/
│   ├── hooks/
│   ├── tabs/
│   ├── App.tsx
│   ├── index.css
│   └── main.tsx
├── index.html
├── package.json
└── tailwind.config.js
```

## Navigation and Accessibility

- Tab and Shift+Tab move through interactive controls.
- Left Arrow and Right Arrow move between workshop tabs.
- Home and End jump to the first and last tab.
- Every tab is connected to its panel with ARIA attributes.
- Diagrams include accessible titles and descriptions.
- The site honors reduced-motion preferences and includes a skip link.

## Deployment

The site is built as a static Vite application. `public/staticwebapp.config.json` is copied into `dist/` for Azure Static Web Apps deployment.
