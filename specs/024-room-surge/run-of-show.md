# Run of show: disclosed fallback — seven minutes

**Stage**: **TODAY 2026-11-17 13:00 Eastern**
**Branch**: `event/arlington-2026-11-18` | **Revision**: R6, 2026-11-17 12:42 ET
**Source**: [spec](spec.md), [plan/evidence/gates](plan.md), confirmed parent observations
**Status**: ✅ Disclosed mock reporting/browser/load PASS; ⛔ live AI/semantic NO-GO; physical cellular scan unverified
**Primary readiness**: `████░░░░░` **4/9**; fallback does not pass live gates.

## Five-line GO/NO-GO record

1. **MOCK FLOW: PASS** — 40 concurrent repeated-wording attempts, 40 accepted signals→4 disjoint incidents, A–D10 each, 40devices, zero failures/blocks/rate limits; p95 all40=0.213s, wall0.380s; not live semantics.
2. **LIVE AI/SEMANTICS: NO-GO** — original45 attempts: zero accepted, 2blocked, 43failed; selective2-response p95 invalid. Corrected private backend Failed12:17:52; no private frontend.
3. **BOARD/REVISION:** `https://allclear-sbuqtpuppifra-frontend.gentlesand-926708e1.eastus2.azurecontainerapps.io/surge` — mock=true; `allclear-sbuqtpuppifra-frontend--mocklabel1236` Healthy/Running,100%traffic; deployed browser proof PASS.
4. **READY TO TEST:** operator privately retrieves existing key from original audience backend Azure Portal Secrets, never URL; Set key/Open; attendees scan `/report`, choose A–D, use matching sample/Send; cards `/surge/cards?only=ABCD`.
5. **CLEANUP/LIMITS:** final protected CLOSED/0signals/0incidents, reports/audit retained; physical cellular scan NOT VERIFIED; no more infra; verified replay `/?demo=loaded` if mock flow fails.

Keep this five-line handoff intact: mock PASS never supersedes primary live NO-GO.

## Ready-to-test mock instructions

1. Open the board URL above; verify the visible **Mock** label and CLOSED state.
2. On the operator's private device, obtain the **existing coach key** from the
   **original audience backend →Azure Portal →Secrets**. Never place it in a
   URL, QR, slide, chat, shell recording or screenshot. Enter masked **Coach key
   →Set key →Open** under Operator controls.
3. Attendees scan the board QR, land on generic `/report`, choose **A–D**,
   select matching **Use sample report**, then **Send**. Disclose that repeated
   sample wording uses mock token-overlap dedup, not live model inference.
4. For printed/screen cards use
   `https://allclear-sbuqtpuppifra-frontend.gentlesand-926708e1.eastus2.azurecontainerapps.io/surge/cards?only=ABCD`.
   Actual physical cellular scanning remains unverified despite PNG QR/browser proof.
5. Close/drain/reset/close after the window; confirm zero tally. Replay:
   `https://allclear-sbuqtpuppifra-frontend.gentlesand-926708e1.eastus2.azurecontainerapps.io/?demo=loaded`.

**Deployment proof**: actual public bundle `index-DVUyNrL6.js`; immutable digest
`sha256:9a7eb0ed665c595e59c7fb7f13e89554b196a9a9eddc463bc9bc91e48a60cb56`.
Two isolated 390×844 Chromium contexts used generic report→A→sample→receipt;
board polled2 signals→1incident/2devices, all3 Surge pages labeled Mock, one
board +six printable PNG QRs, masked operator flow, zero JS errors/mobile
overflow and no URL-key/public-API key leak. This is browser proof, not physical
cellular, live AI, full accessibility or projector certification.

## Why the live path is closed for this showcase

Inherited policy correctly disables Cosmos public access/local auth. Private
network retry Succeeded after approved
`Microsoft.Network/AllowBringYourOwnPublicIpAddress` registration; SQL PE
Approved, DNS10.77.2.4/.5 and managed-identity roles verified. Nevertheless,
`allclear-surge-live-backend` terminal Failed at **12:17:52 ET**:
`ContainerAppOperationError`, empty provider error, no revision/FQDN/log stream;
private frontend never created. Correlation
`f851acdb-4556-456c-bbd4-71f5c7bd0a1e`.
The 12:10 cutoff passed. Do not debug/provision more infrastructure, bypass
policy or imply successful networking produced a usable live app.

## Before projection

- The disclosed **mock audience flow is verified** by T047/T048; use the exact
  sample steps above. Keep loaded replay ready, explicitly labeled replay;
  do not invite submissions merely because a replay renders.
- Mock report/board/cards must visibly disclose runtime mock mode from
  `/api/health`; use the neutral footer, not an unqualified AI-processing claim.
  A–D **Use sample report** prepopulates the actual scene text. Explain that
  repeated wording exercises offline token-overlap dedup; it does not prove
  semantic grouping of attendees' own paraphrases.
- Confirm exact frontend revision/mode and selected fallback at 12:45.
  Board CLOSED, no raw attendee text. Use masked Operator controls →Coach key
  →Set key privately; no key URL/QR/chat/log/screenshot. Protected key unchanged.
- Physical phone, projection/accessibility and full run-through passes are not
  certified by this document. Do not tick them from browser or unit results.

## Show clock (13:00–13:07 ET)

| Elapsed | Default: verified replay | Optional mock interaction, only after deployed proof |
|---|---|---|
| 0:00–0:45 | “This is a replay of the incident-triage flow; live Azure acceptance did not pass today.” | “This is mock mode, not live model inference or semantic acceptance.” |
| 0:45–1:15 | Explain many signals vs underlying incidents. No audience reporting invitation. | Explain A–D sample button; no names/phone numbers/personal details. |
| 1:15–2:30 | Run loaded replay and describe only visible fixture behavior. | Open deliberately; attendees use sample wording. Disclose repeated/mock/seeded inputs. |
| 2:30–3:15 | Show replay signal/incident counts, explicitly fixture counts. | Read actual observed room counts; never promise four incidents or invent missing metrics. |
| 3:15–4:00 | Explain zero-LLM RouterExecutor and three bounded action tools. | Same authority explanation; R is not guaranteed universally blocked. |
| 4:00–5:00 | Show only pre-reviewed safe decision evidence with source citations. | Close intake; use a pre-reviewed safe receipt, no raw attendee text/PII. |
| 5:00–6:30 | Explain value and remaining live validation honestly. | Explain mock flow limitation; no live throughput/semantic claim. |
| 6:30–7:00 | Bridge to tomorrow; leave intake closed. | Same; leave intake closed. |

## Stop conditions and cleanup

If frontend disclosure/revision/mode is uncertain, sample flow fails, requests
error/stall, or unsafe/raw output appears: close and switch to verified replay.
If replay fails, explain from verified artifacts; never claim failed live
acceptance succeeded or promise an untested voice/multilingual backup.

Card ID never controls routing. Samples are ordinary submitted text; no
threshold change/card buckets/pipeline shortcut. Existing crisis/SEV1/statutory/
PII escalation, audit and report preservation remain mandatory.

After each mock verification/show window: close →drain admitted work →reset
tally →close →repeated closed/zero checks. Reset never deletes incidents,
reports or audit; mock state is process-local, not proof of durable live records.
Clear private operator session on shared devices. Record exact frontend
revision, actual mock results and cleanup in [tasks.md](tasks.md).
