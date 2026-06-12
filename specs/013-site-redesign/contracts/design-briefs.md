# Per-Site Design Briefs (DESIGN.md targets)

Target visual systems for each in-scope site. Each is anchored to a named reference of the kind catalogued on `styles.refero.design` (search the name there to pull its full DESIGN.md). Acceptance gate for every site: `npx impeccable detect <site>/src` = **0 anti-patterns**, plus existing build/typecheck/e2e green and WCAG AA preserved. Presentation-only — no content changes.

---

## P1 — workshop-site (executive briefing)

**Register / references**: Linear · Vercel · Stripe — calm, restrained, premium enterprise.
**Baseline tells (30)**: `border-l-4` side-tabs across 7 tab files; `text-gray-600 on bg-blue-50` (gray-on-color).

**Palette (Tailwind theme.extend.colors)** — keep brand recognizability, reduce shout:
- `ink: '#1B1B1F'` (primary text, near-black not pure)
- `surface: '#FFFFFF'`, `surface-muted: '#F7F8FA'` (replace flat `#F3F2F1`)
- `border: '#E6E8EC'` (hairline)
- `brand: '#0F6CBD'` (slightly deeper, calmer than `#0078D4`) — used sparingly
- `accent: '#990000'` (IU crimson) — DEMOTED to rare emphasis only (≤1 use per view)
- Avoid pure black `#000` and gray-on-color body text.

**Type**: keep system `Segoe UI` stack but establish a clear scale (e.g. text-3xl/xl/base with consistent leading); avoid flat hierarchy. Headings `font-semibold tracking-tight`.

**Components**:
- Cards: `border border-border rounded-xl bg-surface shadow-sm` (soft elevation) — NO `border-l-4`.
- Where a left accent conveyed category, replace with a small heading label or a 1px `border-t-2 border-brand/60` top rule, or a soft `bg-brand/5` fill.
- Contrast fix: body text on tinted backgrounds → `text-ink/80` (dark) instead of `text-gray-600`.
- Spacing: increase section padding/whitespace; avoid monotonous equal gaps (vary rhythm).

**Motion**: subtle `transition-colors`/`transition-shadow` on interactive elements; no bounce/elastic.

---

## P2 — coach-site (coach prep, pastoral)

**Register / references**: Notion · Headspace · Cal.com — warm, calm, human, supportive.
**Baseline tells (3)**: `border-l-4` in `App.tsx`, `ContentBlocks.tsx`, `index.css`.
**Audience problem**: inherits workshop's cold Microsoft-blue Fluent palette — wrong tone for *cura personalis*.

**Palette (replace Microsoft Fluent tokens)**:
- `ink: '#2B2622'` (warm near-black)
- `paper: '#FBF8F4'` (warm off-white background), `surface: '#FFFFFF'`
- `border: '#ECE6DD'` (warm hairline)
- `brand: '#B25B34'` (warm terracotta) OR `#3F7E6E` (calm sage) as primary accent — pick terracotta for warmth
- `accent-soft: '#F3E7DE'` (soft fill for callouts)
- Drop `microsoft-blue` as the primary brand color (FR-007).

**Type**: humanist sans for warmth — body `'Söhne', 'Inter Tight', system-ui` is acceptable but PREFER a non-Inter humanist face such as `'Figtree'` or `'Nunito Sans'` for friendliness; headings slightly rounded, `font-semibold`.

**Components**:
- Callouts (ContentBlocks): replace `border-l-4` with soft-fill `bg-accent-soft rounded-lg p-4` + an icon, preserving info/warn/success tones via warm hues.
- Cards: `rounded-2xl` (gentle), `border border-border`, soft `shadow-sm`.
- Keep skip link, single `<main>`, `aria-current`, focus-visible (a11y e2e must stay green).
- Section `source:` declarations and all text UNCHANGED.

**Motion**: gentle `transition` on hover/active; calm, no aggressive easing.

---

## P3 — hackathon-site (architecture reference)

**Register / references**: Stripe Press · The Browser Company · Linear Docs — editorial-academic, refined.
**Baseline tells (1)**: `border-l-4` in `index.css`.
**Identity to KEEP**: maroon `#791A3E` / gold `#B8860B` / cream `#F5F0E8` + Playfair Display serif headings.

**Palette**: keep existing tokens; ensure body text uses `ink #1A1A1A` on cream/white at AA; gold reserved for accents/rules, not body text.

**Type**: KEEP `Playfair Display` serif for display/headings. Replace overused **Inter** body with a warmer text face — `'Source Serif 4'` (editorial) or humanist sans `'Geist'`/`'Söhne'`; keep `JetBrains Mono` for code.

**Components**:
- Remove the `border-l-4` rule in `index.css`; replace any accented card with a refined treatment: thin `border border-deep-cream` + serif label, or a top `border-t border-gold/50` rule.
- Preserve the editorial feel (generous measure, drop caps optional, rules between sections).

**Motion**: minimal; editorial calm.

---

## Shared anti-pattern checklist (must all pass `detect = 0`)

- ❌ No `border-l-4` (side-tab) anywhere.
- ❌ No gradient text on headings; no purple/violet or cyan-on-dark AI palettes.
- ❌ No gray text on colored backgrounds (use darker shade of bg or near-white).
- ❌ Avoid Inter/Roboto as the sole/over-used body font; ensure a real type hierarchy.
- ❌ No pure `#000`/`#fff` body pairs where a tinted near-black/off-white reads better.
- ❌ No nested cards, monotonous spacing, everything-centered layout.
- ✅ Hairline borders + soft elevation; varied spacing rhythm; AA contrast; subtle motion only.
