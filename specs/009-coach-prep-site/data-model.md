# Phase 1 Data Model: Coach Prep Companion Site

This is a static content site — the "data model" is the **content/IA model** the components render. All
entities are compile-time TypeScript structures (no database, no runtime state).

## Entity: Section

A coach-facing topic area rendered as one tab/section.

| Field | Type | Notes / Validation |
|-------|------|--------------------|
| `id` | `string` (slug) | Unique; used as nav anchor/route. One of the six fixed ids. |
| `title` | `string` | Short nav label (e.g. "Prepare", "Troubleshooting"). |
| `order` | `number` | 1–6; defines nav order (P1 stories first). |
| `summary` | `string` | One-line "what this section gives you". |
| `source` | `string` | The `coach-guide/*.md` (or HEADSTART) file this content derives from (drift control). |
| `blocks` | `ContentBlock[]` | Ordered renderable content (see below). |

**Fixed sections (order):**
1. `prepare` ← `coach-guide/FACILITATION.md` (Room Setup, Technical, Materials, Pre-Flight)
2. `timeline` ← `coach-guide/FACILITATION.md` (7-Hour Timeline)
3. `framing` ← `coach-guide/ajcu-framing.md` (60-sec pitch, six-intent rationale)
4. `help` ← `docs/quickstart/HEADSTART.md` (three lanes, scenario-ready) + FACILITATION escalation playbook
5. `troubleshooting` ← `coach-guide/TROUBLESHOOTING.md` (symptom → fix)
6. `assess` ← `coach-guide/ASSESSMENT_RUBRIC.md` + `coach-guide/TALKING_POINTS.md`

## Entity: ContentBlock (discriminated union)

| Variant | Shape | Renders as |
|---------|-------|-----------|
| `heading` | `{ kind: 'heading'; text: string; level: 2|3 }` | Section sub-heading |
| `paragraph` | `{ kind: 'paragraph'; text: string }` | Prose paragraph |
| `checklist` | `{ kind: 'checklist'; title?: string; items: string[] }` | `Checklist` component (unchecked boxes) |
| `callout` | `{ kind: 'callout'; tone: 'info'|'warn'|'success'; text: string }` | `CalloutCard` |
| `troubleshoot` | `{ kind: 'troubleshoot'; symptom: string; cause?: string; fix: string }` | symptom → cause → fix row |
| `lane` | `{ kind: 'lane'; name: string; outcome: string; detail: string }` | Head-start lane card |
| `link` | `{ kind: 'link'; label: string; href: string }` | External/repo link (e.g. to HEADSTART) |

**Validation rules:**
- Every `Section.blocks` MUST be non-empty (a section must render content — supports SC-004).
- `Section.source` MUST name a real file in the repo (drift traceability; checked by a tiny content test).
- `checklist.items` and `troubleshoot.fix` MUST be non-empty strings.
- No block may contain student PII (none exists in source material — these are facilitation docs).

## Entity: NavState (UI-only, ephemeral)

| Field | Type | Notes |
|-------|------|-------|
| `activeSectionId` | `string` | Current section; defaults to `prepare`. |
| `mobileMenuOpen` | `boolean` | Mobile nav toggle; defaults `false`; closes on selection. |

State transitions: `select(id)` → sets `activeSectionId`, closes mobile menu. `toggleMenu()` flips
`mobileMenuOpen`. No persistence (no session/local storage required).

## Relationships

```
Site
 └── Section[1..6]  (ordered, fixed)
        └── ContentBlock[1..n]  (ordered, typed union)
NavState references Section.id (activeSectionId)
```

No cross-entity foreign keys beyond `activeSectionId → Section.id`. Content is immutable at runtime
(compile-time constants), so there are no create/update/delete operations — only navigation.
