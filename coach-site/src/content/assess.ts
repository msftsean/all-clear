import type { Section } from './types'

// Source of truth: coach-guide/ASSESSMENT_RUBRIC.md (criteria + scoring) and
// coach-guide/TALKING_POINTS.md (phase-transition messaging). Summarized faithfully,
// with links to the full guides for depth (FR-002, content-map.md).

export const assess: Section = {
  id: 'assess',
  title: 'Assess',
  order: 6,
  summary: 'What a strong team demo shows, plus phase-transition talking points for the 3-hour build.',
  source: 'coach-guide/ASSESSMENT_RUBRIC.md + coach-guide/TALKING_POINTS.md',
  blocks: [
    {
      kind: 'heading',
      level: 2,
      text: 'What a strong team demo shows',
    },
    {
      kind: 'paragraph',
      text:
        'The 3-hour AJCU workshop runs two build sprints (60 + 15 min) and ends with five 10-minute ' +
        'team demos. Evaluate each team demo against the six AJCU challenge cards, the six-intent ' +
        'routing taxonomy (financial_aid, registrar, campus_ministry, it, student_wellness, general), ' +
        'and the crisis-safety override behavior.',
    },
    {
      kind: 'checklist',
      title: 'Strong demo qualities',
      items: [
        'Correct intent routing across at least three of the six intents',
        'Crisis-safety override fires on harm signals (escalates to 988)',
        'At least one challenge card scenario working end-to-end',
        'Graceful handling of an ambiguous student message',
        'Team articulates what they built and what they would harden next',
        'Clear demo flow with minimal setup fumbles',
      ],
    },
    {
      kind: 'callout',
      tone: 'info',
      title: 'Qualitative over quantitative',
      text:
        'A team that routes two intents perfectly and handles a crisis message correctly is far ' +
        'stronger than a team that routes five intents but misses the safety override. Focus on ' +
        'correctness and understanding, not feature count.',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'Talking points for phase transitions',
    },
    {
      kind: 'paragraph',
      text:
        'Opening (1:00-1:08): "Today you will build and test a production-ready multi-agent AI system ' +
        'in three hours — not a toy, a foundation. Run azd up once, then spend the rest of the time ' +
        'building the six AJCU challenge scenarios."',
    },
    {
      kind: 'paragraph',
      text:
        'Before the live demo (1:08-1:22): "The pattern is three agents: triage, specialized ' +
        'departments, and a single action agent that writes tickets. Watch how intent routing and ' +
        'the crisis-safety override work in practice."',
    },
    {
      kind: 'paragraph',
      text:
        'Before Build sprint 1 (1:32-1:40): "You have 60 minutes. Pick a challenge card, build the ' +
        'intent routing for it, test with the quickstart script, and verify crisis messages escalate ' +
        'correctly. Get one scenario working end-to-end before you add more."',
    },
    {
      kind: 'paragraph',
      text:
        'Before Build sprint 2 (2:50): "You have 15 minutes to harden. Add a second intent, test an ' +
        'ambiguous message, or refine your crisis-safety phrasing. Polish what you will demo."',
    },
    {
      kind: 'paragraph',
      text:
        'Before team demos (3:05): "10 minutes per team. Show us what works, articulate what you ' +
        'built, and share one thing you would harden next if you had another hour."',
    },
    {
      kind: 'callout',
      tone: 'warn',
      title: 'Coach script for deployment blockers (30 seconds)',
      text:
        '“If your deployment fails, that’s normal in enterprise subscriptions. First, switch to ' +
        'service-principal auth. Second, verify provider registration. Third, if Cosmos capacity is ' +
        'constrained, move Cosmos to an allowed region like canadacentral while keeping your app ' +
        'region unchanged. You can still complete the lab objective with a backend-first deployment ' +
        'path.”',
    },
    {
      kind: 'paragraph',
      text:
        'Closing (3:55-4:00): "You built and tested a production multi-agent AI system in three hours. ' +
        'That is not a toy; that is a foundation you can extend. Take the challenge cards and the full ' +
        'lab sequence home — there is a full 8-lab deep-dive path if you want to go further."',
    },
    {
      kind: 'link',
      label: 'Full Assessment Rubric (coach-guide/ASSESSMENT_RUBRIC.md)',
      href: 'https://github.com/EstablishedCorp/47doors/blob/main/coach-guide/ASSESSMENT_RUBRIC.md',
    },
    {
      kind: 'link',
      label: 'Full Talking Points (coach-guide/TALKING_POINTS.md)',
      href: 'https://github.com/EstablishedCorp/47doors/blob/main/coach-guide/TALKING_POINTS.md',
    },
  ],
}
