import type { Section } from './types'

// Source of truth: coach-guide/TROUBLESHOOTING.md → common Lab 00+ issues as
// symptom → cause → quick fix (each fix under 5 minutes). Faithful to the guide (FR-002).

export const troubleshooting: Section = {
  id: 'troubleshooting',
  title: 'Troubleshooting',
  order: 5,
  summary: 'Common setup failures with under-5-minute fixes, including Azure conditional access.',
  source: 'coach-guide/TROUBLESHOOTING.md',
  blocks: [
    {
      kind: 'paragraph',
      text:
        'Quick reference for resolving common participant issues. Each fix should take under five ' +
        'minutes. Scan for the symptom, confirm the cause, apply the fix.',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'Lab 00: Environment Setup',
    },
    {
      kind: 'troubleshoot',
      symptom:
        'SyntaxError or ModuleNotFoundError running Python scripts; messages about an unsupported Python version.',
      cause: 'Participant has Python < 3.11, or the system defaults to an older version.',
      fix:
        'Check with python --version (or python3 --version). If < 3.11, install Python 3.11+ from ' +
        'python.org. On Windows, ensure 3.11+ is first in PATH or use py -3.11 explicitly.',
    },
    {
      kind: 'troubleshoot',
      symptom: 'npm install fails with syntax errors, ES module errors, or ERR_REQUIRE_ESM.',
      cause: 'Node.js version < 18 installed.',
      fix: 'Check node --version. Install Node 18+ via nvm (nvm install 18 && nvm use 18) or from nodejs.org.',
    },
    {
      kind: 'troubleshoot',
      symptom: 'ModuleNotFoundError for installed packages; the wrong Python interpreter is used.',
      cause: 'Packages were installed but the virtual environment is not activated.',
      fix:
        'Activate the venv — Windows: .venv\\Scripts\\activate; macOS/Linux: source .venv/bin/activate. ' +
        'Confirm the prompt shows the (.venv) prefix.',
    },
    {
      kind: 'troubleshoot',
      symptom:
        'Chat returns "Service temporarily unavailable"; console shows ERR_CONNECTION_REFUSED to localhost:8000; HTTP 502 on the forwarded 5173 URL in Codespaces.',
      cause:
        'VITE_API_BASE_URL in frontend/.env is set to http://localhost:8000. In Codespaces the browser ' +
        'runs outside the container and cannot reach localhost:8000 directly.',
      fix:
        'Edit frontend/.env and clear the value (VITE_API_BASE_URL=), restart the Vite dev server, and ' +
        'hard-refresh. With it empty, API calls use relative paths and are proxied by Vite to the backend.',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'Lab 02: MCP Integration & Azure access',
    },
    {
      kind: 'troubleshoot',
      symptom:
        'Login page shows "You don’t have access to this resource" with error code AADSTS53003; az login and azd auth login fail in Codespaces.',
      cause: 'Tenant Conditional Access blocks user-interactive Azure CLI login in this context.',
      fix:
        'Pivot to service principal auth immediately to preserve lab timing: az login --service-principal ' +
        '-u <AZURE_CLIENT_ID> -p <AZURE_CLIENT_SECRET> --tenant <AZURE_TENANT_ID>, set the subscription, ' +
        'then azd auth login --client-id … --client-secret … --tenant-id … --no-prompt. Ensure the SP ' +
        'has RBAC on the subscription/resource group.',
    },
    {
      kind: 'troubleshoot',
      symptom: 'npx -y @azure/mcp@latest --version fails with an engine mismatch on Node 18.',
      cause: '@azure/mcp currently requires Node.js >= 20.',
      fix:
        'Switch Node versions before re-running checks: source /usr/local/share/nvm/nvm.sh, then ' +
        'nvm install 20 && nvm use 20, and retry the MCP checks / Lab 02 verification.',
    },
    {
      kind: 'troubleshoot',
      symptom: '@azure queries return nothing; "No results found".',
      cause: 'Azure resource context not configured, or the service principal is missing permissions.',
      fix:
        'Verify the subscription is set (az account show), confirm the resource group has resources, ' +
        'and ensure the SP has the Reader role. Test directly with az resource list.',
    },
    {
      kind: 'heading',
      level: 2,
      text: 'Lab 06: Deployment',
    },
    {
      kind: 'troubleshoot',
      symptom: 'azd up fails with MissingSubscriptionRegistration for Microsoft.App or Microsoft.Web.',
      cause: 'Required resource providers are not registered for the subscription.',
      fix:
        'Ask a subscription admin to run az provider register -n Microsoft.App --subscription <SUB_ID> ' +
        '--wait (and the same for Microsoft.Web), then retry azd up once registration reaches Registered.',
    },
    {
      kind: 'troubleshoot',
      symptom: 'Cosmos deployment fails with ServiceUnavailable / high demand in the region.',
      cause: 'Subscription region access or temporary capacity constraints.',
      fix:
        'Use an allowed Cosmos region (for example canadacentral) and set its location separately in ' +
        'Bicep, keeping the app hosting region unchanged. If blocked during labs, deploy in mock mode ' +
        'first, then re-enable Cosmos in an allowed region.',
    },
    {
      kind: 'troubleshoot',
      symptom: 'azd up fails; provisioning errors; "deployment failed".',
      cause: 'Azure resource conflicts, quota limits, or template errors.',
      fix:
        'Check azd show --debug, verify subscription quota, ensure unique resource names, and if needed ' +
        'reset with azd down && azd up.',
    },
    {
      kind: 'callout',
      tone: 'warn',
      title: 'When several participants hit the same wall',
      text:
        'Switch to the Timeline section’s Coach Escalation Playbook: conditional access → service ' +
        'principal, no SP visibility → RBAC, MissingSubscriptionRegistration → register providers, ' +
        'Cosmos capacity → allowed region, and keep teams moving with the backend-first path.',
    },
    {
      kind: 'link',
      label: 'Full Troubleshooting guide (coach-guide/TROUBLESHOOTING.md)',
      href: 'https://github.com/EstablishedCorp/47doors/blob/main/coach-guide/TROUBLESHOOTING.md',
    },
  ],
}
