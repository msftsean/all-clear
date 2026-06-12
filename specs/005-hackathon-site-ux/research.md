# Phase 0 Research — 005 Hackathon Site UX

## Decisions

### D1 — Mobile menu mechanism

- **Decision**: Implement a controlled React component (`MobileNav.tsx`) using `useState` for open/closed plus a `<button>` toggle and a conditionally rendered `<nav>` panel.
- **Rationale**: We need `aria-expanded` reflecting state, Escape-to-close, focus return, and route-change close — all easier with explicit state than a CSS-only `<details>`. No new deps.
- **Alternatives considered**: `<details>/<summary>` (no built-in Escape/focus-return, harder ARIA semantics); a headless UI library (adds a dependency, violates NFR-004).

### D2 — Breakpoint strategy

- **Decision**: Toggle is `sm:hidden`; existing inline header nav stays `hidden sm:flex`. They are mutually exclusive at the Tailwind `sm` (640px) breakpoint.
- **Rationale**: Zero desktop regression (FR-004); reuses the breakpoint already in the header.

### D3 — Skip link + landmark target

- **Decision**: A `.skip-link` anchor as the first focusable element in `Layout`, targeting `#main-content` on the `<main>`. `.skip-link` is visually hidden until `:focus`.
- **Rationale**: Standard WCAG bypass-blocks technique; CSS-only visibility avoids layout shift.

### D4 — Focus-visible styling

- **Decision**: Global `:focus-visible` outline using the gold token in `index.css`, plus per-control Tailwind `focus-visible:ring` where a tighter ring is wanted.
- **Rationale**: Keyboard users get a consistent, on-brand indicator without affecting mouse users.

### D5 — 404 handling

- **Decision**: New `NotFound` page rendered by `<Route path="*">` inside the existing `Layout`. Optionally reuse it for unknown card slugs.
- **Rationale**: Keeps site chrome; SWA `navigationFallback` already serves index.html (200), so this is purely a client render improvement (FR-009).

## Open questions

None — all resolved; no NEEDS CLARIFICATION remain.
