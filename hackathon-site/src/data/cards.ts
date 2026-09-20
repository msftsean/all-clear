export interface Card {
  letter: string;
  slug: string;
  title: string;
  pill?: 'P1' | 'P2' | 'P3';
  message: string;
  build: string;
  skill: string;
  doneWhen: string[];
  routingKey: string;
  kb: string[];
}

export const cards: Card[] = [
  {
    letter: '01',
    slug: 'credential-spray',
    title: 'Credential spray',
    pill: 'P1',
    message: 'Authentication failures have climbed 18× across regions. Most attempts share a small rotating set of source networks.',
    build: 'Group the repeated alerts into one security incident, preserve the raw signal count, and assign the Identity queue with a 15-minute acknowledgement SLA.',
    skill: 'High-volume deduplication with an urgent ownership handoff.',
    doneWhen: [
      'Collapses matching signals into one incident without discarding evidence',
      'Sets severity P1 and starts the acknowledgement clock',
      'Creates a ClearBoard update naming the owner and next checkpoint',
    ],
    routingKey: 'Fingerprint: auth failures + shared source pattern + 10-minute window. Queue: Identity Security. Severity: P1. SLA: acknowledge in 15 minutes; publish an initial sitrep in 30 minutes.',
    kb: ['Credential attack containment checklist', 'Identity Security escalation roster', 'ClearBoard incident update format'],
  },
  {
    letter: '02',
    slug: 'checkout-latency',
    title: 'Checkout latency',
    pill: 'P2',
    message: 'Synthetic checks and customer reports show checkout completing in 11–16 seconds after the latest payments deploy.',
    build: 'Correlate the customer-impact and telemetry signals, open one incident for the regression, and route it to the Payments queue.',
    skill: 'Cross-source correlation with a customer-impact assessment.',
    doneWhen: [
      'Links monitoring, support, and deploy signals to one incident timeline',
      'Sets severity P2 with a one-hour mitigation target',
      'Records the rollback decision and customer impact in the sitrep',
    ],
    routingKey: 'Fingerprint: checkout latency + payments service + active release. Queue: Payments Reliability. Severity: P2. SLA: acknowledge in 30 minutes; mitigation target in 60 minutes.',
    kb: ['Payments rollback playbook', 'Customer-impact sizing guide', 'P2 communications checklist'],
  },
  {
    letter: '03',
    slug: 'possible-exposure',
    title: 'Possible data exposure',
    pill: 'P1',
    message: 'A partner reports that a signed export link was forwarded outside the approved recipient list.',
    build: 'Preserve the report as sensitive evidence, create a privacy incident, and prevent duplicate external reports from spawning separate cases.',
    skill: 'Safety-first triage for a potentially sensitive incident.',
    doneWhen: [
      'Classifies the report as restricted and limits the incident audience',
      'Routes to Privacy & Security with P1 handling',
      'Uses ClearBoard only for approved, non-sensitive status language',
    ],
    routingKey: 'Fingerprint: externally shared export link + partner report. Queue: Privacy & Security. Severity: P1. SLA: acknowledge in 15 minutes. Safety rule: never copy sensitive records into the public sitrep.',
    kb: ['Privacy incident containment', 'Restricted incident communications', 'Evidence preservation guide'],
  },
  {
    letter: '04',
    slug: 'warehouse-offline',
    title: 'Warehouse offline',
    pill: 'P2',
    message: 'Three fulfillment sites stopped sending scanner events within two minutes of a network policy rollout.',
    build: 'Deduplicate location-specific alerts into an operations incident and establish a safe fallback while Network investigates.',
    skill: 'Service restoration across a distributed operational queue.',
    doneWhen: [
      'Groups the site alerts under a single parent incident',
      'Assigns Network Operations and names the fulfillment liaison',
      'Publishes a clear operational workaround and next update time',
    ],
    routingKey: 'Fingerprint: scanner telemetry gap + policy rollout + multiple sites. Queue: Network Operations. Severity: P2. SLA: acknowledge in 30 minutes; operational update in 45 minutes.',
    kb: ['Fulfillment continuity playbook', 'Network change rollback procedure', 'Operations sitrep template'],
  },
  {
    letter: '05',
    slug: 'unsafe-content-report',
    title: 'Unsafe content report',
    pill: 'P1',
    message: 'Moderation reports flag a credible threat directed at a named location. The reporter may still be at risk.',
    build: 'Prioritize immediate safety, route to the Safety Response queue, and keep identifying details out of broad updates.',
    skill: 'Human-safety escalation with minimum necessary disclosure.',
    doneWhen: [
      'Marks the case urgent and assigns the on-call Safety Response lead',
      'Separates restricted details from the visible incident summary',
      'Provides a timed escalation checkpoint rather than speculative updates',
    ],
    routingKey: 'Fingerprint: credible threat + named target + active risk. Queue: Safety Response. Severity: P1. SLA: acknowledge immediately; follow the emergency escalation protocol. Safety rule: restricted details stay in the protected case record.',
    kb: ['Safety Response emergency protocol', 'Restricted-data handling', 'P1 leadership notification guide'],
  },
  {
    letter: '06',
    slug: 'api-error-noise',
    title: 'API error noise',
    pill: 'P3',
    message: 'The same upstream timeout generated 240 alerts across seven services, but customer success metrics remain stable.',
    build: 'Suppress duplicate alert noise, track the shared dependency, and avoid prematurely declaring a customer incident.',
    skill: 'Noise reduction with proportionate severity and observation.',
    doneWhen: [
      'Clusters duplicate alerts under an observation record',
      'Routes the dependency issue to Platform Observability',
      'Sets a re-evaluation trigger instead of opening a P1 incident',
    ],
    routingKey: 'Fingerprint: shared upstream timeout + stable customer indicators. Queue: Platform Observability. Severity: P3. SLA: acknowledge in four hours. Re-evaluate if error budget or customer impact crosses threshold.',
    kb: ['Alert deduplication policy', 'Dependency health investigation', 'Severity calibration guide'],
  },
];
