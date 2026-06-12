import type { Section } from './types'

// Source of truth: coach-guide/FACILITATION.md (Coach Escalation Playbook) plus
// the event run-of-show provided by the organizers. The run-of-show reflects the
// current 1:00–4:00 PM session format; escalation steps are transcribed faithfully.

export const timeline: Section = {
  id: 'timeline',
  title: 'Timeline',
  order: 2,
  summary: 'The 1:00–4:00 PM run of show plus the Azure-access escalation playbook for blocked participants.',
  source: 'coach-guide/FACILITATION.md',
  blocks: [
    {
      kind: 'heading',
      level: 2,
      text: 'Run of Show (1:00 – 4:00 PM)',
    },
    {
      kind: 'paragraph',
      text:
        'The three-hour session: frame the problem, show the pattern and a live demo, form teams, ' +
        'then two build sprints bracketing a break, team demos, and a close. Protect Build sprint 1 — ' +
        'it is the 60-minute core of the day.',
    },
    {
      kind: 'schedule',
      rows: [
        { start: '1:00', end: '1:08', block: 'Open & frame', lead: 'Sean', min: 8 },
        { start: '1:08', end: '1:22', block: 'The pattern — three agents', lead: 'Sean', min: 14 },
        { start: '1:22', end: '1:32', block: 'Live demo · Card E', lead: 'Sean', min: 10 },
        { start: '1:32', end: '1:40', block: 'Form teams · pick a card', lead: 'All', min: 8 },
        { start: '1:40', end: '2:40', block: 'Build sprint 1', lead: 'Teams + coaches', min: 60 },
        { start: '2:40', end: '2:50', block: 'Break', lead: '—', min: 10 },
        { start: '2:50', end: '3:05', block: 'Build sprint 2 · harden', lead: 'Teams + coaches', min: 15 },
        { start: '3:05', end: '3:55', block: 'Demos · 5 × 10 min', lead: 'Teams', min: 50 },
        { start: '3:55', end: '4:00', block: 'Close', lead: 'Sean', min: 5 },
      ],
    },
    {
      kind: 'callout',
      tone: 'info',
      title: 'If you fall behind',
      text:
        'Protect Build sprint 1 and the team demo slots first. Absorb the slip by compressing the open, ' +
        'the harden sprint, and the break to their minimums before you touch the demos.',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'Coach Escalation Playbook (Enterprise Azure Environments)',
    },
    {
      kind: 'paragraph',
      text:
        'Use this rapid triage sequence when multiple participants are blocked by Azure access issues:',
    },
    {
      kind: 'callout',
      tone: 'warn',
      title: '1 · Conditional Access block (AADSTS53003)',
      text: 'Switch affected participants to the service principal auth workflow.',
    },
    {
      kind: 'callout',
      tone: 'warn',
      title: '2 · No subscription visibility for the service principal',
      text: 'Confirm the RBAC assignment at subscription or resource-group scope.',
    },
    {
      kind: 'callout',
      tone: 'warn',
      title: '3 · MissingSubscriptionRegistration during azd up',
      text: 'Ask a subscription admin to register Microsoft.App and Microsoft.Web.',
    },
    {
      kind: 'callout',
      tone: 'warn',
      title: '4 · Cosmos regional capacity errors',
      text:
        'Move Cosmos to an allowed region (for example canadacentral) and keep the app hosting ' +
        'region unchanged.',
    },
    {
      kind: 'callout',
      tone: 'info',
      title: '5 · Lab continuity strategy',
      text:
        'Keep participants progressing with the backend-first deployment path; the static frontend ' +
        'deployment can be a follow-on step.',
    },
  ],
}
