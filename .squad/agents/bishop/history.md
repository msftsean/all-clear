# History

## Project Context

All Clear is a bounded-authority incident-triage accelerator requested by
MARYLAND ADMIN 01.

## Learnings

### 2026-09-20 — External coach guide wording vs live inbound phone

The new ACS phone capability is a **real inbound-only communication channel**:
the deployed app can answer a human caller on the provisioned number, but the
current public claim about not sending outbound communications or dispatching
responders is still technically true as written. That said, external coaches
or judges could reasonably overread "does not send outbound communications" as
"does not communicate live at all," so public-facing coach material should add
one plain-language sentence clarifying that live voice demos may include the
system answering an inbound call while all notification/dispatch/public-action
authority remains human-held.

### 2026-09-20 — Event Readiness Review (facilitated, gate: PASS)

Reviewed the squad's preserved event-readiness work (originally started under
the retired Apollo-cast roster, carried forward without rework) plus new
verifier findings:

- **Event path (Storm/Forge):** `docs/event-readiness/DELIVERY_PLAN.md` now
  locks the Arlington Day 2, 465-minute S0-S6 path with executable completion
  evidence per stage and an explicit optional/cut list. Confirmed against
  `labs/README.md` and each lab's self-paced duration/prerequisites.
- **Azure preflight (Kitty):** `docs/event-readiness/AZURE_PREFLIGHT.md`
  covers RBAC, provider registration, quota/capacity, naming, JWT/App
  Insights readiness, shared-backend fallback, and a 20-participant dress
  rehearsal + cleanup checklist. Reviewed independently of the original
  (Haise) author per reviewer-lockout convention.
- **Readiness verifier (Beast):** `scripts/curriculum-readiness.mjs` +
  `npm run curriculum:verify` is the automated gate; its own tests
  (`tests/curriculum/curriculum-readiness.test.mjs`) pass 3/3.
- **Missing exercises (Forge):** Lab 09 bounded `participant_extension/`
  closes the environment-variable-only completion gap; the MCP red-team probe
  (Lab 07) and model-continuity exercise (Lab 05) are deterministic, offline,
  and correctly scoped as optional/take-home.

**Gate outcome:** Reran the verifier after fixing 3 findings (a false-positive
in the env-var completion-gate check, a broken `01c-agent-orchestration.md`
link, and a stale `shared/constitution.md` reference in the surge scenario
README) — now exits 0. Backend `tests/test_failover` (22 passed),
`tests/test_schemas.py`, and `verify_model_continuity.py` all pass. Lab 09
starter + completion tests pass with and without the shortcut env var (the
gate now requires the real extension). **Verdict: GO** — the accelerator is
event-ready for the required S0-S6 path; Labs 02/06/07/08, voice/phone, and
Exercise 05y remain explicitly optional per the delivery plan.

### 2026-09-20 — T031 Glass-Box Audit Correction Verification

Coordinator corrected exercises/01-glass-box-audit.md (lines 331–335) to accurately state that `AZURE_AI_PROJECT_ENDPOINT` missing causes `glass_box_eval.py` to exit with code 2, not warn/fallback. Verified accuracy against `evals/glass-box-audit/glass_box_eval.py` lines 215–217: script returns 2 on missing env var. Marked T031 done and annotated with verification evidence.

### 2026-09-20 — Event-Day Readiness Final Gate (Phase 4)

Final merge recommendation for `020-glass-box-audit` is **GO-WITH-CAVEATS**,
not a clean GO and not a NO-GO.

- Treat the decision as a weighted synthesis, not a single-suite verdict:
  strong green signals were the double-confirmed 347/347 backend pass, clean
  frontend build, zero-console regression sweep, live Azure health, and the
  deterministic 5/5 glass-box guardrail pass.
- Deployment-fix evidence matters more than an initial failure: two genuine
  infra defects (ignored `azd` parameter overrides and an empty ACS secret)
  were found, fixed on-branch, and then verified live, which increases
  confidence in the branch rather than lowering it.
- Distinguish **merge readiness** from **demo-proof readiness**. The branch can
  be mergeable while still carrying event-day follow-up items.
- Explicitly flag anomalies that did not produce unsafe output but still show
  behavior drift: the quality eval's `q09` informational transcript request was
  misrouted as incident action, and one sexual-content probe was acknowledged
  as an incident instead of being hard-blocked.
- Call out missing evidence plainly: no real PSTN call was completed end to
  end, and live quality/red-team numeric thresholds were not fully proven in
  Azure because judge/project auth was unavailable.

### 2026-11-17 — Room Surge R2 architecture and event gates

Refreshed only spec 024 artifacts for **today 13:00 ET** on
`event/arlington-2026-11-18`; setup-plan had already run for feature 024.
Patch `e1eca20` is applied; observed baseline is 15 focused /364 full backend,
5 Surge UI tests and frontend build passing, plus actual local mobile-route/
board/QR smoke. These do not certify accessibility, real phones or live semantics.

Real mock HTTP rehearsal yielded 43 signals →43 incidents, two blocked,
zero failed, p95 0.22s: broad bag-of-words paraphrases do not collapse as already
documented in FR-005. Do not infer broken live semantic dedup or lower the global
threshold. Current rehearsal verifier can falsely pass zero/cross-event coverage
and ignores errors in final exit criteria; plan focused tests/hardening first.

User authorized a live Azure test after exact target/access/configuration gates,
not secret changes or internal redteam-app reuse. Missing azd environment,
recorded frontend DNS failure and expired TAP leave audience readiness blocked;
deployed coach key is UNKNOWN, not proven blank. Human auth/Kitty inventory are
prerequisites. Preserve private key delivery, one process/replica, bounded
authority, every report/audit record, and close/drain/reset semantics.

Plan gates require tested checkpoint → approved audience release and
rollback capture → authorized 40-worker live evidence → real phones/projection/
accessibility and seven-minute fallback rehearsal → closed/zero tally and
12:30 freeze. No runtime/Azure change, subagent, commit or push in this pass.

Subsequent target decision: user selected a **separate audience app** in
MCAPS-2026-segayle (`9f8986ed-ceb2-414d-8fcb-46d5cfc70618`) for today;
corporate-tenant TAP/membership repair is deferred. Kitty's approved-subscription
inventory and local ignored `.azure\deployment-plan.md` are pending. New-resource
scope and explicit new-coach-secret permission remain separate; approval prompt
was unavailable, so no secret permission granted. Existing secrets and private
redteam adapter remain off limits. Docker CLI/azd exist but local Linux daemon
is down; plan operator-started Docker or explicitly approved/capacity-checked
ACR remote build. Add minimal masked non-URL coach entry before public release;
do not mistake current query-key stripping for secure delivery.

**10:15 ET permission supersession:** user explicitly approved NEW separate
audience resources and NEW app-scoped secrets including coach key in MCAPS 2026:
“yes create away. the goal is to get this complete.” Earlier unavailable
approval is superseded; no repeated elicitation for ordinary isolated creation.
Existing app secrets/private adapter remain off limits. Spec 024 R3 records
parent GitHub publication FIRST, then implementation and azure-validate/
preflight/deploy handoff. Technical inventory/build/live gates remain unverified;
this documentation pass still performs no runtime/cloud write or commit/push.

**10:18 ET execution coordination:** Forge owns only known verifier false-pass
fixes, protected `--key-env` input, small masked board operator entry and focused
tests; no new packages, card grouping, threshold or mock changes. Parent started
Docker Desktop PID 30064; engine responsiveness still needs proof. Kitty may
prepare configuration but must wait for code tests/build before deployment or
public exposure. Repeated old CNE login screenshot does not change today's
approved MCAPS 2026 path or require choosing those historical-tenant accounts.

**10:20 ET integration correction:** plan Technical Context now uses canonical
column-zero Spec Kit labels `**Language/Version**:`, `**Primary Dependencies**:`,
`**Storage**:` and `**Project Type**:` so update-agent-context can parse them.
Parent owns regenerated Copilot instructions and publication. Docker blocker
resolved: daemon 29.9.3/linux verified by `docker version` + `docker info`;
T020c marked complete. Image build, code tests and deployment remain unverified.

**10:23 ET delivered-code evidence:** Forge implemented known verifier fixes,
`--key-env NAME` (default SURGE_COACH_KEY), and masked Operator controls /Coach
key /Set key. Eleven new verifier tests; 26 focused and 6 UI tests pass;
typecheck/build pass. Parent full backend 375 passed in 8.15s; context updater
succeeded. G3 complete, live gate not done. CLI confirms selected subscription
Enabled in actual tenant `16b3c013-d300-468d-ac64-7eda0820b6d3`; old CNE/MCP
auth context must not be called MCAPS inaccessibility. Correct CLI resource
inventory and parent publication remain pending. No app/cloud writes by Bishop.

**Final local browser proof:** keyed isolated mock integration PASS: missing
key 403; masked Coach key /Set key →Open; mobile report A→board polls 1 signal;
local QR PNG. Observer saw no key URL or coach header on public calls.
Reset verified closed/signals=0/incidents=0 and both helpers stopped. This is
operator-path proof, not live semantic acceptance or real-phone/accessibility
certification. Parent can publish the Spec Kit checkpoint with this evidence.
