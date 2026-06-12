# DESIGN.md: All Clear Frontend

Visual ground truth for all frontend work. The reference render is `docs/design/briefing-room-reference.html`; open it before building anything. If code and this document disagree, this document wins. Use the system, not pixel-copying.

## Concept

**Two worlds in one frame.** The conversation lives on warm paper (the human side: callers, supervisors, the agent's voice). The operational picture lives on night glass (the machine side: map, incidents, confidence, drafts). The split is the identity; never blend the two palettes inside one panel.

## Tokens

### Color: paper world (conversation column)

```
--paper:     #F2EDE3   /* column background */
--paper2:    #FFFDF7   /* bubbles, input */
--paperline: #E0D8C8   /* borders, dashed rules */
--inkwarm:   #2E2A22   /* primary text */
--midwarm:   #6E6657   /* secondary text, labels */
--voice:     #B0541F   /* live-audio accent: waveform, mic, channel tags ONLY */
```

### Color: night world (canvas)

```
--night:  #10161F   /* canvas background */
--panel:  #161E2A   /* cards */
--nline:  #27324A   /* borders, tracks */
--nink:   #C6D2E4   /* primary text */
--ndim:   #7C8CA6   /* labels, secondary */
```

### Color: status (both worlds)

```
--sev1:  #E25555
--sev2:  #E59A3A
--sev3:  #5B8FE8   /* also SEV4 at reduced emphasis */
--clear: #37C281
```

**Hard rules:**
- `--clear` green is RESERVED. It appears only in the brand mark, the publish/approve action, and the all-clear terminal state. Never as a generic success color, never on charts except the citations metric, never decorative. The board going green must mean something.
- Severity owns color. Nothing else in the UI competes with SEV hues for attention.
- `--voice` orange marks live audio only (waveform, mic button, INBOUND·PHONE tags). Not links, not warnings.

## Typography

```
--display: 'Archivo'        weights 500/600/700
--body:    'Inter'          weights 400/500/600
--data:    'JetBrains Mono' weights 400/500
```

- **Archivo**: brand mark, the agent's voice lines in chat (13.5px, weight 500, letter-spacing -0.005em), card titles if promoted. Used with restraint; it is the personality, not the workhorse.
- **Inter**: all UI chrome, body copy, buttons, human messages.
- **JetBrains Mono**: everything machine-generated or machine-read: incident IDs (AC-####), chips, confidence numbers, similarity scores, timestamps, channel tags, card eyebrows, audit references. The rule: if RouterExecutor or the audit log produced it, it renders in mono. This is how users learn to distinguish agent fact from interface chrome.
- Scale: 10px mono eyebrows/labels, 11-12px secondary, 13-13.5px body, 18px brand, 20px detail headers. Sentence case everywhere except mono eyebrows (uppercase, letter-spacing .08-.12em).

## Layout

- Desktop: two-column grid, `430px` fixed conversation column left, fluid canvas right. Canvas is a 2-col card grid (`gap:14px`), wide cards span both.
- Mobile (<980px): conversation only; canvas cards become pinnable sheets summoned from messages (do not cram the split onto a phone).
- Radii: 10px cards, 12px chat bubbles (3px on the speaker corner), 4-6px chips/buttons. Borders 1px solid; dashed borders are reserved for system whispers and receipt rules.

## Signature components

1. **Waveform-to-chips.** Live caller audio renders as bars in `--voice`; as QueryAgent classifies, structured chips (intent, entities, severity cues, confidence) materialize under the transcript. Speech visibly becoming structure is the product thesis in one component.
2. **Generative canvas cards.** Every card carries a mono eyebrow with its title AND its provenance (`pinned by: "give me a sitrep"` / `auto`). Cards the conversation creates say so.
3. **Decision receipt.** Imported from the Triage Desk direction: an expandable, dash-ruled trace per incident (QueryAgent → Router → ActionAgent rows: who, model or "deterministic · no LLM", what, the numbers, citations as mono pills) ending at the authority-boundary pause with approve/edit actions. Lives in a slide-over on the canvas.
4. **The approval gate.** Anything customer-facing or regulator-facing ends in a paused state with `Approve & publish` (the only `--clear` button). Approvals note the 15-minute undo window.

## Motion

- Waveform animation and the LIVE blink are the only ambient motion. Cluster merges and card pins may animate once (250-350ms ease-out); nothing loops except the waveform.
- `prefers-reduced-motion`: waveform freezes at 50%, blink stops, merges become instant. Already implemented in the reference; preserve it.

## Voice and copy

- The agent speaks plainly and owns its boundaries: "It needs your approval before it goes out, that's my boundary, not a bug." Never apologetic, never vague.
- Magnitude is communicated as community, not data: "You're the 14th caller about the Oak Street line."
- Buttons say what happens: `Approve & publish`, `Show sources`, `Edit draft`. An action keeps its name through the whole flow.
- Errors and empty states give direction, not mood. No exclamation marks in operational copy.

## Engineering notes

- React 18 + Vite + Tailwind: map tokens above into `tailwind.config` theme extensions; do not hardcode hexes in components.
- Map: react-leaflet + OSM tiles with the GeoJSON-outline fallback when tiles are unreachable.
- Every interactive element gets a stable `data-testid` (Barton's Playwright suite depends on them).
- Fonts via Google Fonts with `font-display: swap`; system-ui fallbacks declared.
- Accessibility floor: visible keyboard focus (2px `--sev3` ring), AA contrast in both worlds (verified for the token pairs above), all status conveyed by text+color, never color alone.
