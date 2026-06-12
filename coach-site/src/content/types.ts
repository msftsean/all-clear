// Content model for the Coach Prep Companion Site.
//
// This is a static content site — the "data model" is the compile-time content/IA
// structure the components render. See specs/009-coach-prep-site/data-model.md.

/** A single renderable unit within a section. Discriminated union on `kind`. */
export type ContentBlock =
  | { kind: 'heading'; text: string; level: 2 | 3 }
  | { kind: 'paragraph'; text: string }
  | { kind: 'checklist'; title?: string; items: string[] }
  | { kind: 'callout'; tone: 'info' | 'warn' | 'success'; title?: string; text: string }
  | { kind: 'troubleshoot'; symptom: string; cause?: string; fix: string }
  | { kind: 'lane'; name: string; outcome: string; detail: string }
  | { kind: 'schedule'; rows: { start: string; end: string; block: string; lead: string; min: number }[] }
  | { kind: 'link'; label: string; href: string }

/** A coach-facing topic area rendered as one tab/section. */
export interface Section {
  /** Unique slug; used as nav anchor/route. One of the six fixed ids. */
  id: string
  /** Short nav label (e.g. "Prepare", "Troubleshooting"). */
  title: string
  /** 1–6; defines nav order (P1 stories first). */
  order: number
  /** One-line "what this section gives you". */
  summary: string
  /** The coach-guide/*.md (or HEADSTART) file this content derives from (drift control). */
  source: string
  /** Ordered renderable content. MUST be non-empty. */
  blocks: ContentBlock[]
}

/** UI-only ephemeral navigation state. */
export interface NavState {
  /** Current section; defaults to `prepare`. */
  activeSectionId: string
  /** Mobile nav toggle; defaults false; closes on selection. */
  mobileMenuOpen: boolean
}
