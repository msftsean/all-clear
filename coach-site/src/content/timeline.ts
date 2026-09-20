import type { Section } from './types'

export const timeline: Section = {
  id: 'timeline',
  title: 'Timeline',
  order: 2,
  summary: 'A 90-minute path from surge triage to a reliable ClearBoard handoff.',
  source: 'coach-guide/FACILITATION.md',
  blocks: [
    { kind: 'heading', level: 2, text: 'Run of show' },
    { kind: 'schedule', rows: [
      { start: '0:00', end: '0:10', block: 'Frame the exercise', lead: 'Facilitator', min: 10 },
      { start: '0:10', end: '0:25', block: 'Live surge triage', lead: 'Facilitator + room', min: 15 },
      { start: '0:25', end: '0:40', block: 'Severity and SLA', lead: 'Facilitator', min: 15 },
      { start: '0:40', end: '1:00', block: 'ClearBoard practice', lead: 'Participants', min: 20 },
      { start: '1:00', end: '1:15', block: 'Voice and phone intake', lead: 'Facilitator', min: 15 },
      { start: '1:15', end: '1:25', block: 'Safety rehearsal', lead: 'Facilitator + room', min: 10 },
      { start: '1:25', end: '1:30', block: 'Debrief', lead: 'Facilitator', min: 5 },
    ] },
    { kind: 'heading', level: 2, text: 'Surge triage prompts' },
    { kind: 'checklist', items: ['Is this a signal, an incident, or a report?', 'What evidence is known, missing, or duplicated?', 'What is the magnitude: scope, location, time, and affected services or people?', 'What is the next safe action, and who owns it?'] },
    { kind: 'callout', tone: 'info', title: 'Protect the essentials', text: 'If time is short, protect triage, severity and SLA, ClearBoard handoff, and the safety rehearsal. Use a fictional transcript if voice or phone is unavailable.' },
  ],
}
