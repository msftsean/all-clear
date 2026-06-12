import type { Section } from './types'

// Source of truth: coach-guide/FACILITATION.md → "Room Setup Checklist"
// (Physical Environment, Technical Environment, Materials, Pre-Flight Verification).
// Presented faithfully as scannable, unchecked lists (FR-002).

export const prepare: Section = {
  id: 'prepare',
  title: 'Prepare',
  order: 1,
  summary: 'Room, tech, materials, and pre-flight checklists to complete before participants arrive.',
  source: 'coach-guide/FACILITATION.md',
  blocks: [
    {
      kind: 'paragraph',
      text:
        'The 47 Doors AJCU workshop runs a focused three-hour session (1:00–4:00 PM). Participants ' +
        'have no time to fight configuration, so the path is azd-first: run azd up once and the ' +
        'knowledge base is baked in by the postprovision hook, then teams spend the rest of the ' +
        'session building and testing the six AJCU challenge scenarios. Work through these ' +
        'checklists before participants arrive so the room, network, and Azure access are ready ' +
        'and the first azd up succeeds on time.',
    },
    {
      kind: 'callout',
      tone: 'info',
      title: 'Complete before participants arrive',
      text:
        'These are the "Room Setup Checklist" items from the facilitation guide. The boxes are a ' +
        'reference, not a saved state — print or tick them off in your own copy.',
    },
    {
      kind: 'checklist',
      title: 'Physical Environment',
      items: [
        'Projector/screen tested and working',
        'Whiteboard markers available (at least 3 colors)',
        'Power strips at each table cluster',
        'Seating arranged in pairs or small groups (3–4 per table)',
        'Facilitator station near power and screen access',
        'Water/refreshments station identified',
      ],
    },
    {
      kind: 'checklist',
      title: 'Technical Environment',
      items: [
        'Wi-Fi credentials posted visibly',
        'Test internet connectivity from multiple locations in the room',
        'Azure subscription access verified for all participants',
        'GitHub Codespaces quota confirmed (if using cloud dev)',
        'Backup hotspot available for connectivity issues',
        'Shared screen/demo machine ready with all labs pre-loaded',
      ],
    },
    {
      kind: 'checklist',
      title: 'Materials',
      items: [
        'Printed quick-reference cards (optional but helpful)',
        'Sticky notes for "parking lot" questions',
        'Name tags or table tents',
        'Feedback forms ready (digital or paper)',
      ],
    },
    {
      kind: 'checklist',
      title: 'Pre-Flight Verification',
      items: [
        'Run azd up end-to-end on a fresh account',
        'Verify Azure OpenAI endpoints are responding',
        'Confirm Azure AI Search index is accessible',
        'Test the azd deployment flow end-to-end',
      ],
    },
    {
      kind: 'callout',
      tone: 'success',
      title: 'Head start the night before',
      text:
        'Encourage participants to do the 10-minute Day-0 steps (open Codespaces, sign in to ' +
        'Copilot, optionally azd auth login) ahead of time. See the Help Participants section for ' +
        'the three cold-start lanes that keep teams out of setup limbo.',
    },
  ],
}
