import type { Section } from './types'

export const prepare: Section = {
  id: 'prepare',
  title: 'Prepare',
  order: 1,
  summary: 'Set up an accessible, safe incident-triage exercise before the room arrives.',
  source: 'coach-guide/FACILITATION.md',
  blocks: [
    { kind: 'paragraph', text: 'Prepare a fictional All Clear exercise that lets facilitators demonstrate surge triage without exposing operational or personal data.' },
    { kind: 'checklist', title: 'Room and access', items: ['Projector, audio, and facilitator browser profile tested', 'Shared demo workspace opens directly to ClearBoard', 'Participants have accessibility accommodations and the exercise URL', 'Headsets are available; captions and a text alternative are enabled'] },
    { kind: 'checklist', title: 'Demo pre-flight', items: ['Use a clean workspace with fictional data only', 'Verify a signal can become an incident with linked reports', 'Confirm magnitude, severity, SLA, owner, and status are visible', 'Test the approved safety escalation path', 'Test text, voice, and phone fallback paths without live emergency calls'] },
    { kind: 'callout', tone: 'warn', title: 'Safety boundary', text: 'All Clear supports human judgment. If a real safety concern appears, pause the exercise and follow the organization’s emergency procedure.' },
  ],
}
