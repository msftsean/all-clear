import type { Section } from './types'

// Source of truth: coach-guide/ajcu-framing.md → "The 60-second mission pitch"
// and the "Framing notes" (the six-intent rationale). Pitch quoted faithfully (FR-002).

export const framing: Section = {
  id: 'framing',
  title: 'Framing',
  order: 3,
  summary: 'The 60-second mission pitch and the six-intent rationale to open the build sprint.',
  source: 'coach-guide/ajcu-framing.md',
  blocks: [
    {
      kind: 'paragraph',
      text:
        'Use the 60-second mission pitch to open the build sprint. It sets up the Jesuit framing ' +
        '(cura personalis) and the six-intent taxonomy the teams will build against.',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'The 60-second mission pitch',
    },
    {
      kind: 'callout',
      tone: 'info',
      title: 'The door behind the door',
      text:
        '“Every Jesuit university already has 47 doors. The Bursar, the Registrar, IT, Counseling, ' +
        'Campus Ministry, your advisor, your RA, your dean. A student in distress doesn’t know which ' +
        'door is the right one, and cura personalis breaks down at the front desk. Today you’re ' +
        'going to build the door behind the door. One agent, one conversation, that knows when to ' +
        'send a student to financial aid, when to send them to a chaplain, and when — quietly, ' +
        'urgently — to send them to the counseling center. The agent doesn’t replace any of those ' +
        'offices. It makes sure the student actually gets to the right one. By 1:30 you’ll have a ' +
        'working prototype. By the end of the conference you’ll have a pattern you can take back to ' +
        'your campus.”',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'Framing notes',
    },
    {
      kind: 'paragraph',
      text:
        'Why these six intents. Financial Aid, Registrar, Campus Ministry, IT, Student Wellness, and ' +
        'General / Mission mirror the offices a Jesuit student actually encounters in their first 90 ' +
        'days. Campus Ministry is a first-class peer to IT and the Registrar — not an afterthought — ' +
        'because at Jesuit schools it materially shapes the student experience.',
    },
    {
      kind: 'paragraph',
      text:
        'Cura personalis at the routing layer. The escalation rules encode care for the whole ' +
        'person: Student Wellness and Financial Aid create tickets autonomously when distress ' +
        'signals appear (the cost of a missed ticket is high), while Campus Ministry offers to ' +
        'connect a student with a chaplain rather than booking on their behalf — pastoral ' +
        'relationships should be opt-in.',
    },
    {
      kind: 'paragraph',
      text:
        'Never gate clinical care behind a faith conversation. When a message is an ambiguous mix of ' +
        'distress and meaning, route to Student Wellness first and offer chaplaincy in parallel ' +
        '(Challenge A).',
    },
    {
      kind: 'paragraph',
      text:
        'The live demo. Challenge D (“The Phishing Storm”) is the on-stage moment — the canonical ' +
        '“one message, two outcomes”: IT routing and a parallel security-incident ticket from a ' +
        'single sentence.',
    },
    {
      kind: 'link',
      label: 'Full framing notes (coach-guide/ajcu-framing.md)',
      href: 'https://github.com/EstablishedCorp/47doors/blob/main/coach-guide/ajcu-framing.md',
    },
  ],
}
