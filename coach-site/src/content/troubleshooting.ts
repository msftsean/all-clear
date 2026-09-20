import type { Section } from './types'

export const troubleshooting: Section = {
  id: 'troubleshooting',
  title: 'Troubleshooting',
  order: 5,
  summary: 'Resolve common exercise failures while preserving safety and auditability.',
  source: 'coach-guide/TROUBLESHOOTING.md',
  blocks: [
    { kind: 'troubleshoot', symptom: 'Two records describe the same event.', cause: 'Reports were triaged before corroboration was checked.', fix: 'Keep the clearest timeline, link duplicates, preserve original sources, and post one status update explaining the merge.' },
    { kind: 'troubleshoot', symptom: 'The group cannot agree on severity.', cause: 'Labels are being used without policy or evidence.', fix: 'Read the approved severity definitions, list confirmed scope and risk, choose the current level, and set a reassessment time.' },
    { kind: 'troubleshoot', symptom: 'An active incident has no visible owner or next update.', cause: 'The record was opened without a handoff.', fix: 'Assign the designated role, add the next update time, and state the immediate action on ClearBoard.' },
    { kind: 'troubleshoot', symptom: 'Voice intake cannot hear the caller.', cause: 'Browser permission, headset selection, or service availability.', fix: 'Check permissions and the selected input, then immediately offer text intake. Use an approved fictional transcript if voice remains unavailable.' },
    { kind: 'troubleshoot', symptom: 'A participant introduces a real safety concern.', cause: 'The exercise has crossed into a real-world situation.', fix: 'Pause immediately, contact the designated human responder or emergency service under local procedure, and protect privacy.' },
  ],
}
