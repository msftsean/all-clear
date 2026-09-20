import type { Section } from './types'

export const help: Section = {
  id: 'help',
  title: 'Facilitate',
  order: 4,
  summary: 'Prompts and interventions that keep triage focused, inclusive, and safe.',
  source: 'coach-guide/FACILITATION.md + coach-guide/TROUBLESHOOTING.md',
  blocks: [
    { kind: 'heading', level: 2, text: 'Use the right intervention' },
    { kind: 'lane', name: 'Productive analysis', outcome: 'Observe and deepen the evidence', detail: 'Participants are separating facts from assumptions and checking ClearBoard. Ask: “What evidence would change your severity?”' },
    { kind: 'lane', name: 'Drift or duplication', outcome: 'Link the records and name the owner', detail: 'Participants are creating parallel incidents or debating labels without acting. Ask: “What is the safest reversible next action?”' },
    { kind: 'lane', name: 'Safety-critical content', outcome: 'Pause and escalate to a human responder', detail: 'Follow the organization’s emergency procedure. Do not diagnose, promise confidentiality, or continue the exercise as though it were fictional.' },
    { kind: 'heading', level: 2, text: 'Voice and phone checklist' },
    { kind: 'checklist', items: ['Confirm location, callback method, and immediate safety information', 'Repeat essential details and label unverified information', 'Offer a text alternative; do not require speech for support', 'Create the same traceable ClearBoard record as text intake', 'Use an approved transcript if the demonstration connection fails'] },
  ],
}
