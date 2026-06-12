import { useEffect, useId, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { HUB_LINKS } from '../data/nav';

/**
 * Accessible disclosure menu for hub navigation on small viewports.
 *
 * - A toggle <button> (visible only below the Tailwind `sm` breakpoint) with
 *   `aria-expanded`, `aria-controls`, and an accessible name.
 * - When open, renders a <nav aria-label="Mobile"> panel listing HUB_LINKS.
 * - Closes on route change (useLocation) and on Escape (returning focus to the
 *   toggle button).
 */
export default function MobileNav() {
  const [open, setOpen] = useState(false);
  const location = useLocation();
  const buttonRef = useRef<HTMLButtonElement>(null);
  const panelId = useId();

  // Close the panel whenever the route changes.
  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  // Close on Escape and return focus to the toggle button.
  useEffect(() => {
    if (!open) return;
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        setOpen(false);
        buttonRef.current?.focus();
      }
    }
    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [open]);

  return (
    <div className="sm:hidden">
      <button
        ref={buttonRef}
        type="button"
        aria-expanded={open}
        aria-controls={panelId}
        aria-label={open ? 'Close menu' : 'Open menu'}
        onClick={() => setOpen((prev) => !prev)}
        className="inline-flex items-center justify-center rounded p-2 text-maroon hover:text-gold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold transition-colors"
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          {open ? (
            <>
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </>
          ) : (
            <>
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </>
          )}
        </svg>
      </button>

      {open && (
        <nav
          id={panelId}
          aria-label="Mobile"
          className="absolute left-0 right-0 z-20 border-b border-deep-cream bg-cream shadow-lg"
        >
          <ul className="max-w-5xl mx-auto px-4 py-2 flex flex-col">
            {HUB_LINKS.map((link) => (
              <li key={link.to}>
                <Link
                  to={link.to}
                  className="block py-3 text-base font-medium text-ink/80 hover:text-maroon focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold rounded transition-colors"
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
}
