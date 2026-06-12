export interface Card {
  letter: string;
  slug: string;
  title: string;
  pill?: 'LIVE DEMO' | 'WARMUP';
  message: string;
  build: string;
  skill: string;
  doneWhen: string[];
  routingKey: string;
  kb: string[];
}

export const cards: Card[] = [
  {
    letter: 'A',
    slug: 'quiet-crisis',
    title: 'The Quiet Crisis',
    message:
      "I haven't been to class in two weeks. I don't think I belong here. I've been crying at night. I don't know who to talk to.",
    build:
      'Recognize overlapping distress, route primarily to Student Wellness, surface the crisis line, and ALSO offer a chaplain conversation as a parallel path. No gating.',
    skill: 'Whole-person overlap + safety escalation, no gating.',
    doneWhen: [
      'Routes primarily to Student Wellness (not Campus Ministry)',
      'Surfaces the 24/7 crisis line and creates a wellness ticket',
      'Offers a chaplain conversation in parallel — never as a gate in front of clinical care',
    ],
    routingKey:
      'Primary student_wellness; overlap campus_ministry (offer only). Safety override: if harm signals appear, escalate=true, priority=urgent, surface 988, always create ticket. Rule: never gate clinical care behind a faith conversation.',
    kb: [
      'Booking a counseling intake',
      'Same-day urgent appointments and after-hours crisis support',
      'Talking to a chaplain — pastoral counseling vs. spiritual direction',
    ],
  },
  {
    letter: 'B',
    slug: 'aid-cliff',
    title: 'The Aid Cliff',
    message:
      "My mom lost her job last month. Can I get more aid? Also I'm thinking of dropping a class — does that hurt my package?",
    build:
      "Detect the financial_aid + registrar overlap, route correctly, and create a high-priority appeals ticket with the student's narrative attached.",
    skill: 'Multi-intent overlap + autonomous high-priority ticket.',
    doneWhen: [
      "Detects both intents and routes primarily to Financial Aid (the aid implication is the blocker)",
      "Creates a high-priority appeals ticket carrying the student's narrative",
      'Acknowledges the registrar/drop question',
    ],
    routingKey:
      'Primary financial_aid; overlap registrar. "lost my job" → human-touch → priority=high, always create ticket. The drop-deadline part alone would be registrar, but aid is the blocker here.',
    kb: [
      'How federal aid is recalculated when you drop below full-time status',
      'Appealing your financial aid award: the special-circumstances form',
      'Add/drop, withdrawal, and the W vs. WF distinction',
    ],
  },
  {
    letter: 'C',
    slug: 'discernment',
    title: 'The Discernment',
    message:
      "I'm thinking about doing a year of service after graduation. I don't know if I should apply to JVC or take the consulting job. Can someone help me think through this?",
    build:
      'Route to Campus Ministry, surface discernment-group and 1:1 chaplain options, and do NOT auto-create a ticket — it offers.',
    skill: 'Offer, don\'t auto-create — opt-in human handoff.',
    doneWhen: [
      'Routes to Campus Ministry',
      'Surfaces discernment-group and 1:1 chaplain options',
      'Offers to connect rather than auto-creating a ticket (pastoral relationships are opt-in)',
    ],
    routingKey:
      'Primary campus_ministry. Human-touch keywords (discernment, vocation) → priority=normal, always_create_ticket=False. The win is restraint: offer, don\'t book.',
    kb: [
      'Discernment groups for students considering religious or service vocations',
      'Service & immersion programs and how to apply',
      'Talking to a chaplain — pastoral counseling vs. spiritual direction',
    ],
  },
  {
    letter: 'D',
    slug: 'phishing-storm',
    title: 'The Phishing Storm',
    pill: 'LIVE DEMO',
    message:
      "My password isn't working and I just got an email saying my account is locked. I clicked the link.",
    build:
      'Handle the IT routing AND trigger a security-incident workflow because of the click. Two tickets — one to IT support, one to the security team.',
    skill: 'One message → two parallel actions (dual ticket).',
    doneWhen: [
      'Routes to IT and offers a self-serve password reset',
      'Detects the "I clicked the link" signal and fires a security-incident workflow',
      'Produces two tickets from one message — IT support + security team',
    ],
    routingKey:
      'Primary it; second action = security incident triggered by the click. Two tickets. This is the on-stage live demo — the canonical "one message, two outcomes."',
    kb: [
      'Resetting your university password and enrolling in MFA',
      'Reporting a phishing email',
    ],
  },
  {
    letter: 'E',
    slug: 'holy-spirit',
    title: 'Mass of the Holy Spirit',
    pill: 'WARMUP',
    message:
      "When is the Mass of the Holy Spirit? Also, I'm not Catholic — am I welcome?",
    build:
      'The simplest case — Campus Ministry routing with an interfaith welcome paragraph baked into the response. Good warmup for newer teams.',
    skill: 'Simplest A→B routing + inclusive welcome (warmup).',
    doneWhen: [
      'Routes to Campus Ministry',
      'Answers the schedule question from the KB',
      'Includes an interfaith welcome line — does not assume Catholic identity',
    ],
    routingKey:
      'Primary campus_ministry. Interfaith-respect rule applies: serve students of all faiths and none. No ticket needed.',
    kb: [
      'Mass schedule, reconciliation hours, and sacramental preparation',
      'Interfaith programming, prayer spaces, and dietary observances',
    ],
  },
  {
    letter: 'F',
    slug: 'multilingual-family',
    title: 'The Multilingual Family',
    message:
      'Mi mamá quiere saber cuándo es el día de orientación para padres.',
    build:
      'Detect Spanish, respond in Spanish, and route to General/Mission with a parent-orientation KB hit.',
    skill: 'Language detection + multilingual response.',
    doneWhen: [
      'Detects the message is in Spanish',
      'Responds in Spanish',
      'Routes to General/Mission and retrieves the parent-orientation article',
    ],
    routingKey:
      'Primary general. Language detection drives a Spanish-language response; KB retrieval on parent orientation.',
    kb: [
      "First-year orientation: what's required vs. optional",
      'What does Jesuit education actually mean?',
    ],
  },
];
