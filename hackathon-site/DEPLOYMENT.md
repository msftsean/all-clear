# Deploying the Hackathon Site to Azure Static Web Apps

Two GitHub Actions workflows are provided. Pick one.

| Workflow | Auth | Stored in repo | Best when |
|---|---|---|---|
| `deploy-hackathon-swa.yml` | SWA **deployment token** | 1 secret | Simplest; fine for a workshop |
| `deploy-hackathon-swa-oidc.yml` | **GitHub OIDC** federated login | only non-secret IDs | No long-lived secrets; preferred |

Both build `hackathon-site/` and publish `dist/`. Neither requires interactive
`az login` from your Codespace, so they are unaffected by the Conditional Access
(AADSTS53003) block.

---

## Option A — Token (fastest)

1. In the Azure Portal, open the Static Web App → **Manage deployment token** → copy it.
2. GitHub → repo **Settings → Secrets and variables → Actions → New repository secret**:
   - Name: `AZURE_STATIC_WEB_APPS_API_TOKEN_HACKATHON_SITE`
   - Value: *(the token)*
3. Push to `main`. `deploy-hackathon-swa.yml` builds + deploys.

---

## Option B — OIDC (no stored secret)

GitHub Actions exchanges a short-lived OIDC token for an Azure token via a
**federated credential** on an Entra app registration. The SWA deployment token
is fetched at runtime with `az`, so nothing long-lived is stored.

Run these **once**, from a trusted network/device that can `az login`
(your corp machine on VPN — *not* the Codespace, which the CA policy blocks):

```bash
# 0. Sign in (corp network) and select the subscription
az login
az account set --subscription "<SUBSCRIPTION_ID>"

# 1. Create the app registration
appId=$(az ad app create --display-name "47doors-hackathon-deploy" --query appId -o tsv)

# 2. Create a service principal for it
az ad sp create --id "$appId"

# 3. Add a federated credential bound to this repo's main branch
az ad app federated-credential create --id "$appId" --parameters '{
  "name": "github-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:EstablishedCorp/47doors:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'

# 4. Grant it Contributor on the resource group holding the SWA
subId=$(az account show --query id -o tsv)
az role assignment create \
  --assignee "$appId" \
  --role "Contributor" \
  --scope "/subscriptions/$subId/resourceGroups/<RESOURCE_GROUP>"

echo "AZURE_CLIENT_ID=$appId"
echo "AZURE_TENANT_ID=$(az account show --query tenantId -o tsv)"
echo "AZURE_SUBSCRIPTION_ID=$subId"
```

Then in GitHub → **Settings → Secrets and variables → Actions**:

- **Secrets** (tab "Secrets"):
  - `AZURE_CLIENT_ID` = the `appId` printed above
  - `AZURE_TENANT_ID` = printed above
  - `AZURE_SUBSCRIPTION_ID` = printed above
- **Variables** (tab "Variables"):
  - `SWA_NAME` = your Static Web App resource name
  - `SWA_RESOURCE_GROUP` = its resource group

Push to `main` (or run the workflow manually via **Actions → Deploy Hackathon
Site to Azure SWA (OIDC) → Run workflow**). Until `AZURE_CLIENT_ID` is set, the
OIDC workflow safely no-ops with a warning.

> If you don't yet have a Static Web App resource, create one first:
> `az staticwebapp create --name <SWA_NAME> --resource-group <RESOURCE_GROUP> --location <region>`
> (or via the Portal). No GitHub integration step is needed — these workflows push
> content directly.

---

## Option B (Portal GUI) — OIDC without any `az login`

Use this if interactive `az login` is blocked by Conditional Access (AADSTS53003).
Do everything from a browser on a trusted/corp device.

**A. App registration** — Entra ID → App registrations → **New registration** →
name `47doors-hackathon-deploy` → Register. Copy **Application (client) ID** and
**Directory (tenant) ID**.

**B. Federated credential** — that app → Certificates & secrets → **Federated
credentials** → **Add credential** → scenario **GitHub Actions deploying Azure
resources**:
- Organization `EstablishedCorp`, Repository `47doors`
- Entity type **Environment**, Environment `production`, Name `github-47doors-production`

> ⚠️ Must be **Environment = `production`**, not Branch. The deploy job sets
> `environment: production`, so the OIDC subject is
> `repo:EstablishedCorp/47doors:environment:production`. A Branch-scoped
> credential will fail `azure/login` with `AADSTS70025`.

**C. Role assignment** — Resource group (holding the SWA) → Access control (IAM)
→ Add role assignment → **Contributor** → assign to the
`47doors-hackathon-deploy` service principal.

**D. Create the SWA if needed** — Create a resource → Static Web App → Free plan
→ Deployment source **Other** (skip GitHub linking) → Create. Note name + RG.

**E. GitHub config** — repo Settings → Secrets and variables → Actions:
- Secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`
- Variables: `SWA_NAME`, `SWA_RESOURCE_GROUP`

Then run the **"Deploy Hackathon Site to Azure SWA (OIDC)"** workflow.

### Troubleshooting the OIDC run

| Symptom (step that fails) | Cause | Fix |
| --- | --- | --- |
| `azure/login` fails `AADSTS70025` | No federated credential on the SP yet | Add the **Environment = `production`** credential (step B) |
| `azure/login` fails `AADSTS700213`/subject mismatch | Credential scoped to Branch, not Environment | Recreate as **Environment `production`** |
| `Fetch SWA deployment token` fails: `ERROR: Static site was '' not found in subscription.` | `SWA_NAME` / `SWA_RESOURCE_GROUP` **Variables** are empty/missing | Set both repo **Variables** (step E). The SWA *resource name* is on the Static Web App's Portal **Overview** page — it is usually **not** the auto-generated `*.azurestaticapps.net` hostname prefix |
| `Fetch SWA deployment token` fails: authorization/`AuthorizationFailed` on `Microsoft.Web/staticSites/listSecrets/action`, **even though** the SP has an active Contributor role on the SWA | **Wrong target resource** — `SWA_NAME` / `SWA_RESOURCE_GROUP` Variables pointed at a resource group that does not exist (e.g. `rg-47doors-ajcu-hackathon` instead of the real `rg-ajcu-hackathon`), so `az` queried the wrong path and returned an authorization error | The workflow now **auto-discovers** the SWA by its production hostname (`SWA_HOSTNAME`, default `white-ground-0c80a6f10.7.azurestaticapps.net`) and ignores the Variables when discovery succeeds. The `Discover the SWA by hostname` step prints every SWA the SP can see with its real name + resource group. If discovery fails, set the Variables to the real values shown there. |
| `Discover the SWA by hostname` lists no Static Web Apps / cannot find the hostname | The login subscription (`AZURE_SUBSCRIPTION_ID`) does not contain the SWA | Confirm the SWA's subscription on its Portal **Overview** page and set `AZURE_SUBSCRIPTION_ID` to that subscription's ID. For this project the SWA lives in **Cloudforce Sponsorship** (`098ef2f6-cea4-4839-8093-ef90622e1b8c`), resource group `rg-ajcu-hackathon`. |
| `Fetch SWA deployment token` fails: authorization/`AuthorizationFailed` (SP genuinely missing the role in the correct subscription) | SP lacks RBAC on the SWA's resource group | Assign **active Contributor** to the SP on that resource group (step C). Note: a *Privileged Identity Management* **eligible** assignment does NOT work for a service principal — it must be an active assignment |

> Re-run as a **fresh "Run workflow" on `main`**, not a re-run of an old attempt —
> re-runs replay the old commit/config.

### Diagnosing the CA block (admins)

Entra ID → Monitoring → **Sign-in logs** → filter by Correlation ID from the
error → open the row → **Conditional Access** tab shows the failing policy
(usually a trusted-locations/network condition, because a cloud egress IP is not
trusted). Fix by excluding the Azure CLI app for the build identity, adding the
build network as a Named location, or simply using OIDC/token deploy above.

