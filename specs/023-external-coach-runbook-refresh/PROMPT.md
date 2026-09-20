# Refresh the All Clear external coach runbook

You are working in `Public-sector-hacks-Org/all-clear-coaches-runbook`, a
separate sanitized public React/Vite static site for external coaches and
judges. The guide is stale: `docs/RED-TEAM-EVALUATION.md` still says the final
local verification was on **September 10, 2026**, and roughly 10 days of
upstream All Clear work should now be reflected at a high level without leaking
internal-only details.

Before changing anything, read **`README.md`** and
**`docs/EXTERNAL-SHARING-REVIEW.md`** and preserve this repo's public-safe
boundary:

- no credentials, secrets, private endpoints, or internal hostnames
- no internal route names, feature codenames, internal file paths, or exact
  phone numbers
- no unsupported product-status claims for placeholder runbooks
- keep the guide abstract, synthetic, and external-safe

Then make these concrete edits:

1. **Add a glass-box vs black-box coaching talking point**
   - Edit `src/content.ts` and add one new stage cue (or expand an existing
     cue) so coaches explicitly reward inspectable evidence, honest
     uncertainty, and recoverable design over polished unsupported output.
   - Suggested direction: add a cue like **Reveal** with wording along the
     lines of: *contrast a polished answer with the evidence behind it; if the
     system cannot show support for a claim, reward the safe stop and explicit
     uncertainty over unsupported success.*

2. **Add one visible public-safe scenario/talking point**
   - Edit `src/App.tsx` and add one scenario card or equivalent callout in the
     scenarios/evaluation flow about an apparent success that needs evidence
     review before trust is earned.
   - Keep it generic and coach-facing. Good public-safe shape:
     - label: `AUDIT TRANSPARENCY`
     - title: `Polished answer, missing evidence`
     - example prompt: *"The system says the review is complete, but the team
       cannot trace one part of the result back to the source material."*
     - emphasis: judges should reward honest boundaries and recoverable design,
       not theatrical autonomy.
   - Do **not** mention internal scripts, file paths, vendor/invoice counts, or
     internal exercise mechanics.

3. **Clarify the live voice safety boundary**
   - Edit `src/App.tsx` so the coach-charter and/or safety boundary makes clear
     that a demo deployment may include a real inbound voice-answering path
     without weakening the existing "no outbound / no dispatch" claim.
   - Preserve the current boundary language and add this sentence verbatim or
     meaning-equivalent:

     > Demo deployments may include a real inbound voice channel where the
     > system answers a caller, but All Clear does not initiate outbound
     > contact, notify the public, or dispatch responders; those actions remain
     > under human authority.

4. **Refresh the verification evidence**
   - Run the repo's real validation flow with `npm test`.
   - Update `docs/RED-TEAM-EVALUATION.md` so it no longer says "Final local
     verification on September 10, 2026". Replace that with today's actual
     verification date and the real results from the rerun.
   - Keep the evidence truthful: if counts or wording changed, record the real
     output rather than copying the old numbers.

5. **Capture screenshots if this repo normally does so**
   - Run `npm run screenshots` if the local environment supports the repo's
     existing screenshot workflow.
   - Note any regenerated screenshot evidence consistently with the repo's
     existing documentation style.

6. **Leave intentional unknowns alone**
   - Review the `other-runbooks` placeholder section, but do **not** change the
     "Workforce Navigator" or "Constituent Connect" placeholder status unless
     you have explicit separate product direction. Their current status is
     unknown; do not invent URLs, availability, or readiness claims.

Implementation notes:

- Make the smallest cohesive set of changes that updates the public guidance and
  keeps the repo internally consistent.
- If any unit or e2e assertions depend on the old exact wording, update them
  narrowly so they still verify the public boundary and the new inbound-voice
  clarification.
- Do not add new external destinations beyond the repo's existing allowlist
  model.

## Definition of done

- [ ] `npm run typecheck` passes
- [ ] `npm run test:unit` passes
- [ ] `npm run build` passes
- [ ] `npm run test:security` passes
- [ ] `npm run test:links` passes
- [ ] `npm run test:e2e` passes
- [ ] `docs/RED-TEAM-EVALUATION.md` has today's actual verification date and
      refreshed evidence from the real rerun
- [ ] `src/content.ts` and `src/App.tsx` reflect the glass-box coaching refresh
      and the inbound-voice clarification
- [ ] the `other-runbooks` placeholders remain unchanged unless separately
      instructed
- [ ] the repo still satisfies its sanitization/public-sharing boundary from
      `README.md` and `docs/EXTERNAL-SHARING-REVIEW.md`
