export interface HubLink {
  to: string;
  label: string;
}

export const HUB_LINKS: readonly HubLink[] = [
  { to: '/workflow', label: 'Workflow' },
  { to: '/queues', label: 'Queues' },
  { to: '/policy', label: 'Policy' },
  { to: '/shift-plan', label: 'Shift plan' },
  { to: '/runbook', label: 'Runbook' },
];
