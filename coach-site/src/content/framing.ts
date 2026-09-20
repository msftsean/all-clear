import type { Section } from './types'

export const framing: Section = {
  id: 'framing',
  title: 'Framing',
  order: 3,
  summary: 'Open the exercise with a shared vocabulary for evidence, impact, and response.',
  source: 'coach-guide/incident-triage-framing.md',
  blocks: [
    { kind: 'heading', level: 2, text: 'The 60-second opening' },
    { kind: 'callout', tone: 'info', title: 'Turn noise into a shared picture', text: '“A signal is something that may matter. A report is what a person or system says happened. An incident is the coordinated record we open when the evidence and impact call for action. Today we will preserve the source, estimate magnitude, assign severity, meet the right SLA, and use ClearBoard for the next safe handoff.”' },
    { kind: 'heading', level: 2, text: 'Framing notes' },
    { kind: 'checklist', items: ['Keep signals, reports, and incidents distinct while linking related evidence', 'Describe magnitude with scope, location, time window, affected services or people, and confidence', 'Use published severity definitions and reassess when credible evidence changes', 'Treat ClearBoard as the accountable handoff: owner, status, timestamp, and next update', 'Use voice and phone as accessible intake paths that create the same auditable record'] },
    { kind: 'callout', tone: 'warn', title: 'Safety overrides pace', text: 'Do not role-play real trauma or treat the demonstration system as emergency services. Stop and use the designated human escalation procedure when needed.' },
  ],
}
