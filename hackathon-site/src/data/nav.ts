// Canonical hub navigation link set.
// Shared between the desktop header nav (Layout) and the mobile nav (MobileNav)
// to prevent drift. Order must match the existing header order.
export interface HubLink {
  /** Router path, e.g. `/pattern`. */
  to: string;
  /** Visible label, e.g. `Pattern`. */
  label: string;
}

export const HUB_LINKS: readonly HubLink[] = [
  { to: '/pattern', label: 'Pattern' },
  { to: '/intents', label: 'Intents' },
  { to: '/rules', label: 'Rules' },
  { to: '/run-of-show', label: 'Schedule' },
  { to: '/runbook', label: 'Student Runbook' },
];
