import type { Section } from './types'

export const assess: Section = {
  id: 'assess',
  title: 'Debrief',
  order: 6,
  summary: 'Assess safe, explainable decisions and leave the room with clear next actions.',
  source: 'coach-guide/ASSESSMENT_RUBRIC.md + coach-guide/TALKING_POINTS.md',
  blocks: [
    { kind: 'heading', level: 2, text: 'What strong practice shows' },
    { kind: 'checklist', title: 'Demonstration criteria', items: ['Classifies signals, reports, and incidents correctly', 'Preserves source, time, confidence, scope, and impact', 'Explains a policy-aligned severity and response SLA', 'Uses ClearBoard to show owner, status, and next update', 'Escalates safety-critical content to the designated human procedure', 'Confirms voice and phone intake with an accessible alternative'] },
    { kind: 'callout', tone: 'success', title: 'A successful exercise', text: 'A fictional surge becomes one managed incident with linked evidence, stated magnitude, severity, SLA, ClearBoard owner, and safe next action.' },
    { kind: 'heading', level: 2, text: 'Debrief prompts' },
    { kind: 'checklist', items: ['What evidence supported the severity?', 'What remains uncertain about magnitude?', 'Who owns the next action and when is the next update?', 'What must be confirmed during a voice or phone report?', 'What safety procedure overrides ordinary triage?'] },
  ],
}
