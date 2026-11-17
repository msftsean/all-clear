# All Clear Day-0 Head-Start

Use this guide to prepare the All Clear pro-dev track before the event. Choose
one of the three lanes below; the shared-backend and offline lanes do not
require an Azure subscription. This is a controlled demo application, not a
production incident system.

## Choose a lane

### Shared backend

Use the backend URL and access instructions supplied by the facilitator. Keep
signals synthetic and follow the event's demo-data rules. Do not send real
resident, student, patient, employee, or incident information.

### Self-serve `azd`

Use this lane only if you have an Azure subscription and are authorized to
provision the demo resources.

1. Install Python 3.11+, Node.js, Git, Azure Developer CLI (`azd`), and
   GitHub Copilot in VS Code or Codespaces.
2. Clone the repository and open its root in VS Code or Codespaces.
3. Sign in with `azd auth login`.
4. Run `azd up` and review all prompts before provisioning. The preprovision
   hook validates the local seed corpus. The postprovision hook attempts to
   seed Azure AI Search and prints a warning if it cannot complete; `azd up`
   can succeed even when index seeding is not confirmed.
5. Follow the postdeploy output for the backend URL, then verify its health
   endpoint before using the live lane.

The Search admin key is not exported by Bicep. If the postprovision
hook warns that seeding did not complete, configure the Search/OpenAI endpoint
variables and `AZURE_SEARCH_API_KEY` from approved local sources, then rerun
`bash scripts/quickstart.sh --no-smoke`. Do not commit the key or paste it into
prompts.

The current Container Apps template exposes the backend externally and this
application does not configure end-user authentication. Do not expose it to
untrusted users, restore conversation history or phone transcripts, or use
real sensitive data until verified identity, authorization, and ownership
controls are integrated.

### Offline mock lane

This lane needs no Azure credentials or network access. From the repository
root, run:

```bash
bash scripts/quickstart.sh --mock
```

The command runs the local mock incident pipeline and prints the literal
`✅ Scenario-ready` marker when it succeeds. It does not create an Azure
resource or contact a deployed service.

## Scenario-ready checklist

- [ ] Repository opens at the root in VS Code or Codespaces.
- [ ] Copilot is available in the editor; do not paste secrets or real personal
      data into prompts.
- [ ] For the offline lane, `bash scripts/quickstart.sh --mock` exits 0 and
      prints `✅ Scenario-ready`.
- [ ] For a provisioned lane, `python scripts/seed_search_index.py --dry-run`
      lists the canonical seed articles without Azure calls.
- [ ] For a deployed lane, `/api/health` returns HTTP 200 before the demo.
- [ ] Use synthetic All Clear signals and verify that each signal remains a
      report, while deduplication attaches reports rather than deleting them.

For CI-like local checks, run `npm run smoke-test` from the repository root.
It runs the backend test suite and frontend unit tests in mock/test mode.
