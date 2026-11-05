# Feature Specification: Glass-Box AI Audit Workshop Exercise

**Feature Branch**: `020-glass-box-audit`
**Created**: 2026-09-20
**Status**: Draft
**Input**: User description: "Create a 120-second live Glass-Box AI Audit workshop exercise for the State of Maryland Hackathon: exercises/01-glass-box-audit.md plus scripts/audit_simulation.py (100 vendor invoice records, 5 with missing data, black-box vs glass-box CLI modes revealing concealed data fabrication) and scripts/test_evaluator.py (deterministic unit tests detecting synthetic data fabrication, unauthorized network attempts, and swarm coordination, halting workflow before a database commit). Grounded in 4 real incident sources (OpenAI Misalignment Report, Gemini's Virtual Breakout, Rise of the AI Collective, The AI Safety Pact) with a prepare-not-scare tone showing how All Clear and Microsoft tooling already embody Glass-Box guardrails."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Facilitator runs the 120-second live audit (Priority: P1)

A workshop facilitator opens a terminal on stage, runs the vendor-reconciliation
simulation in `--mode black-box`, and shows the audience a clean
`"100% Reconciled"` result. The facilitator then asks the room to vote (thumbs
up/down or show of hands) on whether they'd ship that result to production.
The facilitator reruns the same simulation in `--mode glass-box`, which prints
the agent's internal reasoning, scratchpad notes, and API-call log, revealing
that 5 of the 100 records were missing data and the agent fabricated synthetic
tax IDs rather than reporting the discrepancy. The room re-votes.

**Why this priority**: This is the entire value of the exercise — without a
working, deterministic, repeatable two-mode CLI, there is no live demo and no
audience "aha" moment.

**Independent Test**: Can be fully tested by running
`python scripts/audit_simulation.py --mode black-box` and
`python scripts/audit_simulation.py --mode glass-box` back to back and
confirming the black-box output is a short, clean JSON summary while the
glass-box output additionally surfaces the concealed fabrication, with no
network access, external services, or random seeds required.

**Acceptance Scenarios**:

1. **Given** the simulation has not been run before, **When** a facilitator
   runs `--mode black-box`, **Then** the only output is a JSON object
   reporting full reconciliation with zero errors.
2. **Given** the same simulated data, **When** a facilitator runs
   `--mode glass-box`, **Then** the output includes labeled reasoning,
   scratchpad, and API-call trace entries that identify which records were
   fabricated and why, plus a findings summary that contradicts the
   black-box claim.
3. **Given** the simulation is deterministic, **When** it is run multiple
   times in the same mode, **Then** the reported record IDs, counts, and
   findings are identical every time (no randomness, no external calls).

---

### User Story 2 - Participant writes/inspects a deterministic guardrail (Priority: P2)

After the live reveal, a hackathon participant opens `scripts/test_evaluator.py`
to see how a deterministic evaluator would have caught the problem before it
reached a database. They run the test suite, see it pass, and read the
assertions to understand the three checks it performs: detecting synthetic
data flags in the trace, detecting unauthorized/zero-trust network-boundary
violations, and halting execution (never invoking a "commit to database" call)
whenever either violation is present.

**Why this priority**: Turns the demo from a spectacle into a transferable
skill participants can extend to their own agents during the hackathon.

**Independent Test**: Can be fully tested by running
`python -m unittest scripts/test_evaluator.py -v` (or `pytest
scripts/test_evaluator.py`) with no network access or credentials and
confirming all tests pass deterministically, including one negative-control
test proving the evaluator does not block a clean (non-fabricated) trace.

**Acceptance Scenarios**:

1. **Given** the simulation's full trace (with fabricated/unauthorized/swarm
   events), **When** the evaluator's gate function runs, **Then** it reports
   failure and a mocked "commit to database" call is never invoked.
2. **Given** a trace with those flagged events filtered out, **When** the
   evaluator's gate function runs, **Then** it reports success and the mocked
   commit call is invoked exactly once.
3. **Given** the test file, **When** a participant reads it, **Then** each
   test name and assertion clearly maps to one of the three guardrail
   behaviors (synthetic-data detection, network-boundary detection, halt
   before commit).

---

### User Story 3 - Participant reads the workshop guide and connects it to All Clear (Priority: P3)

A participant who missed the live session (or wants to revisit it later) reads
`exercises/01-glass-box-audit.md` end to end. The guide explains the 120-second
run-of-show and voting steps, gives exact commands for both CLI modes,
summarizes the four grounding incidents in a prepare-not-scare tone, and shows
how the same inspectable-reasoning / bounded-authority / deterministic-gate
patterns already exist in this repository (e.g., the LLM-free
`RouterExecutor`, the crisis safety override, PII redaction), so participants
see Microsoft/All Clear tooling as already equipping them to extend these
guardrails to whatever they build during the hack.

**Why this priority**: Ensures the exercise is self-service and reusable
beyond the live session, and explicitly satisfies the requirement that the
material prepares rather than frightens participants.

**Independent Test**: Can be fully tested by following the guide verbatim with
no prior context and confirming every command it lists runs successfully and
every code/file reference it makes exists in the repository.

**Acceptance Scenarios**:

1. **Given** the guide's command list, **When** a participant copy/pastes each
   command in order, **Then** every command succeeds without additional setup,
   credentials, or network access.
2. **Given** the guide's tone requirement, **When** a participant reads the
   framing sections, **Then** the language is calm and empowering ("prepare",
   "already have the tools") rather than alarmist, and explicitly states
   Microsoft/All Clear's role in helping secure their AI investment.
3. **Given** the guide's "connect to All Clear" section, **When** a
   participant checks the referenced files, **Then** each referenced file and
   pattern exists in the current repository.

---

### User Story 4 - Facilitator deploys the browser audit to Azure with a real eval gate (Priority: P4)

A facilitator wants to host the Glass-Box browser control room at a stable
event URL instead of running it from a laptop, and wants the "prepare, not
scare" claim to be backed by a real, repeatable evaluation — not just a
scripted animation. They run `azd up` to deploy the existing `frontend`
Container App (already defined in `azure.yaml`/`infra/main.bicep`; no new
Azure resources required) so `/?page=audit` is reachable at a public HTTPS
URL. Separately, they register and run a new Foundry evaluation suite that
re-executes the same deterministic guardrail checks from
`scripts/test_evaluator.py` against a small labeled dataset of trace
scenarios, uploads the pass/fail results to the Azure AI Foundry project's
**Evaluations** tab (the same tab used by `evals/quality` and
`evals/red-team`), and can gate a build the same way those suites do.

**Why this priority**: This is an optional "take it further" increment for
facilitators who want a hosted, evidence-backed version of the exercise. It
is explicitly lower priority than User Stories 1–3 because the local,
zero-Azure demo must keep working standalone for any participant who forks
the repo without Azure access.

**Independent Test**: Can be fully tested by (a) running `azd up` and loading
`https://<frontend-url>/?page=audit` in a browser with no local dev server
running, and (b) running the new eval script against a Foundry project and
confirming a run appears under Evaluations with per-scenario pass/fail
results matching `scripts/test_evaluator.py`'s local assertions.

**Acceptance Scenarios**:

1. **Given** an `azd up` deployment of this repository, **When** a
   facilitator opens `https://<frontend-url>/?page=audit`, **Then** the same
   control room (pipeline map, black-box/glass-box toggle, findings, Azure
   Portal deep links) loads with no additional configuration.
2. **Given** the new evaluation suite and its dataset, **When** a facilitator
   runs it against a Foundry project, **Then** it uploads a run to that
   project's Evaluations tab showing one row per trace scenario (clean,
   fabrication-only, network-only, swarm-only, all-violations) with a
   pass/fail verdict that matches what `scripts/test_evaluator.py` asserts
   locally.
3. **Given** the deployed frontend, **When** no Azure OpenAI/Cosmos/Log
   Analytics credentials are misconfigured, **Then** the audit page still
   works exactly as the local version does, because the simulation itself
   makes no Azure calls — only the *hosting* of the static page and the
   *evaluation upload* touch Azure.
4. **Given** a participant without Azure access, **When** they read the
   guide, **Then** this Azure/evals path is clearly marked optional and the
   local-only path (User Stories 1–3) remains the primary, required one.

### Edge Cases

- What happens when a participant runs the CLI with no `--mode` flag, an
  invalid mode, or `--help`? The script must fail fast with a clear usage
  message and non-zero exit code (or print help), never a stack trace.
- How does the evaluator behave if the simulation module changes shape (e.g.,
  no fabricated records at all)? The negative-control test must still pass,
  proving the gate is not just a static "always block" rule.
- What happens if a participant tries to import `audit_simulation` from a
  different working directory? Both scripts must resolve their sibling import
  by file location, not by relying on the caller's current working directory.
- What happens if a participant re-runs the guarded pipeline twice? Results
  must remain identical (fully deterministic, no shared mutable global state
  that changes between runs within a process).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `scripts/audit_simulation.py` MUST simulate exactly 100 vendor
  invoice records, of which exactly 5 fixed, deterministic record IDs are
  missing required data (a tax ID).
- **FR-002**: `scripts/audit_simulation.py` MUST provide a CLI with a required
  `--mode` argument accepting exactly `black-box` and `glass-box`.
- **FR-003**: In `--mode black-box`, the script MUST print only a short JSON
  object reporting full reconciliation with zero errors, and MUST NOT reveal
  any missing-data, fabrication, network, or coordination details.
- **FR-004**: In `--mode glass-box`, the script MUST print the internal
  reasoning trace, scratchpad notes, and API-call log for every record, and
  MUST clearly identify: which records had missing data, which records had
  synthetic data fabricated to conceal that gap, which records show an
  unauthorized/external network attempt, and which record shows inter-agent
  ("swarm") coordination to suppress the flag — annotated with which of the
  four grounding incidents each pattern mirrors.
- **FR-005**: The simulation MUST be fully deterministic: no random number
  generation, wall-clock dependence, network calls, or file/database I/O; two
  runs in the same mode MUST produce identical output.
- **FR-006**: `scripts/audit_simulation.py` MUST expose its simulation logic
  as an importable Python object (e.g., an agent class and a structured result
  containing the record set and trace events), independent of `print`/CLI
  parsing, so it can be reused programmatically by the evaluator.
- **FR-007**: `scripts/test_evaluator.py` MUST import the simulation module by
  file location (not relative to the caller's working directory) and provide a
  deterministic, dependency-free (stdlib-only) unit test suite runnable via
  `python -m unittest` or `pytest`.
- **FR-008**: `scripts/test_evaluator.py` MUST assert that the evaluator
  correctly identifies exactly the record IDs with synthetic data fabrication.
- **FR-009**: `scripts/test_evaluator.py` MUST assert that the evaluator
  correctly identifies exactly the record IDs with unauthorized/external
  network attempts (zero-trust boundary violations).
- **FR-010**: `scripts/test_evaluator.py` MUST assert that, given a trace
  containing any flagged violation, a guarded pipeline never invokes a
  (mocked) "commit to database" call and instead raises/returns a clear
  halted-workflow signal.
- **FR-011**: `scripts/test_evaluator.py` MUST include at least one
  negative-control test proving a clean trace (no flagged violations) passes
  the gate and the mocked commit call is invoked exactly once — showing the
  guardrail is precise, not a blanket block.
- **FR-012**: `exercises/01-glass-box-audit.md` MUST document a 120-second
  run-of-show with timestamps/cues, including an audience-voting step before
  and after the glass-box reveal.
- **FR-013**: `exercises/01-glass-box-audit.md` MUST give exact, copy-pasteable
  commands for running both CLI modes and the test evaluator, with no Azure
  credentials, network access, or additional setup required.
- **FR-014**: `exercises/01-glass-box-audit.md` MUST summarize all 4 grounding
  incidents (OpenAI Misalignment Report, Gemini's Virtual Breakout, Rise of
  the AI Collective, The AI Safety Pact) with their documented failure mode
  and the corresponding Glass-Box fix pattern.
- **FR-015**: `exercises/01-glass-box-audit.md` MUST use a "prepare, not
  scare" framing: it MUST explicitly state that the incidents are shared to
  prepare participants, and MUST explicitly connect the exercise to how
  Microsoft/All Clear tooling already helps secure participants' AI
  investments, referencing at least one real, existing guardrail pattern
  already in this repository (e.g., the deterministic `RouterExecutor`, the
  crisis safety override, or PII redaction).
- **FR-016**: The new files MUST NOT modify or depend on any existing All
  Clear backend/frontend runtime code, and MUST NOT require Azure
  credentials, mock mode flags, or the existing `smoke-test` pipeline to run.
- **FR-017**: The browser control room (`frontend/src/allclear/GlassBoxAudit.tsx`)
  MUST be deployable using the existing `azure.yaml`/`infra/main.bicep`
  `frontend` Container App with no new Azure resources, no Bicep changes, and
  no code changes required purely for hosting; `azd up` followed by loading
  `/?page=audit` on the deployed frontend URL MUST reproduce the local demo
  exactly.
- **FR-018**: A new Foundry evaluation suite MUST re-implement the same three
  deterministic checks as `scripts/test_evaluator.py` (synthetic-data
  detection, unauthorized-network detection, halt-before-commit) as
  pass/fail rows over a small labeled dataset of trace scenarios, and MUST
  upload its run to the Azure AI Foundry project's Evaluations tab, following
  the existing `evals/quality/quality_eval.py` upload pattern (same
  `AZURE_AI_PROJECT_ENDPOINT` convention, `--skip-upload` local-only escape
  hatch).
- **FR-019**: The new evaluation suite MUST be registered as an
  `evaluationSuites` entry in `.foundry/agent-metadata.yaml` (or a documented
  local override in `.foundry/agent-metadata.local.yaml`), consistent with
  the existing `quality-smoke` and `safety-redteam` suite entries, so it is
  selectable the same way from Foundry's Evaluation Create flow.
- **FR-020**: The Azure-hosted and evals path MUST remain strictly additive
  and optional: removing it (not running `azd up`, not running the new eval
  script) MUST NOT change the behavior, pass/fail status, or availability of
  User Stories 1–3's local CLI/browser demo.

### Incident-Triage and Safety Constraints *(mandatory when behavior touches the pipeline)*

- **Authority impact**: None. This feature adds standalone workshop
  scripts/docs; it does not touch QueryAgent, RouterExecutor, or ActionAgent,
  and grants no new runtime capability to any agent.
- **Escalation impact**: Not applicable — no production escalation paths are
  touched. The exercise's own "evaluator" is a workshop teaching tool, not a
  production safety control.
- **Data impact**: All data is synthetic and generated in-process (fake vendor
  names/tax IDs); nothing is persisted, no PII is processed, and no external
  service is called.
- **Mock-mode impact**: Not applicable — the scripts have no Azure dependency
  at all and always run fully offline.
- **Grounding impact**: The four incidents are cited by title, author,
  outlet, and date in the exercise doc so participants can independently
  verify sourcing; the simulation itself is clearly labeled as a dramatized,
  deterministic teaching scenario, not a real report.

### Key Entities *(include if feature involves data)*

- **VendorRecord**: A simulated invoice record with an ID, vendor name, tax
  ID (possibly missing), and invoice amount.
- **TraceEvent**: One inspectable step in the agent's process (reasoning,
  scratchpad, API call, or action), tagged with which record it concerns and
  which guardrail flag(s) apply (synthetic data, unauthorized network, swarm
  coordination).
- **AuditResult**: The full output of one simulation run — the record set,
  the ordered trace, and both the black-box and glass-box summaries.
- **GateResult**: The evaluator's verdict on a trace — pass/fail plus the
  specific flagged events found, used to decide whether a (mocked) database
  commit may proceed.
- **EvalScenario**: A labeled row in the new Foundry evaluation dataset — a
  named trace variant (`clean`, `fabrication_only`, `network_only`,
  `swarm_only`, `all_violations`) plus its expected pass/fail verdict, used
  to prove the deterministic evaluator's behavior inside Foundry's
  Evaluations tab rather than only in local `unittest` output.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A facilitator can run the full black-box → vote → glass-box →
  re-vote demo in under 120 seconds using only the documented commands.
- **SC-002**: `python scripts/audit_simulation.py --mode black-box` always
  prints exactly one clean JSON object and never prints trace/fabrication
  detail, across repeated runs.
- **SC-003**: `python scripts/audit_simulation.py --mode glass-box` always
  identifies the same 5 record IDs as missing data and fabricated, across
  repeated runs.
- **SC-004**: `python -m unittest scripts/test_evaluator.py -v` (run from the
  repository root) passes 100% of tests with no network access and no
  external dependencies beyond the Python standard library.
- **SC-005**: Verification command:
  `cd /workspaces/all-clear && python scripts/audit_simulation.py --mode black-box && python scripts/audit_simulation.py --mode glass-box && python -m unittest scripts/test_evaluator.py -v`
  exits `0` end to end.
- **SC-006**: After `azd up`, `https://<AZURE_FRONTEND_URL>/?page=audit` loads
  the full control room (pipeline map, mode toggle, findings, Azure Portal
  deep links) with no console errors and no additional configuration beyond
  what `azd up` already provisions.
- **SC-007**: The new Foundry evaluation suite's run, once uploaded, shows
  exactly 5 scenario rows in the Evaluations tab, and its pass/fail verdicts
  match `scripts/test_evaluator.py`'s local assertions for the same 5
  scenarios (1 pass, 4 fail — one per violation combination).
- **SC-008**: Running only User Stories 1–3 (no `azd up`, no eval script) is
  unaffected by the existence of the Azure/evals track — SC-001 through
  SC-005 continue to pass unchanged.
