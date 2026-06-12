# Provisioning the Docs, Workshop & Coach Static Web Apps

This repo deploys **four** independent Azure Static Web Apps (SWAs):

| # | Site | Source folder | Deploy workflow | Token secret |
|---|------|---------------|-----------------|--------------|
| 1 | Hackathon reference site | `hackathon-site/` | `deploy-hackathon-swa.yml` (+ OIDC variant) | `AZURE_STATIC_WEB_APPS_API_TOKEN` |
| 2 | **Docs / runbook** (AAD login-gated) | `docs/` | `deploy-docs-swa.yml` | `AZURE_STATIC_WEB_APPS_API_TOKEN_DOCS` |
| 3 | **Workshop companion** (public) | `workshop-site/` | `deploy-workshop-swa.yml` | `AZURE_STATIC_WEB_APPS_API_TOKEN_WORKSHOP` |
| 4 | **Coach prep companion** (public) | `coach-site/` | `deploy-coach-swa.yml` | `AZURE_STATIC_WEB_APPS_API_TOKEN_COACH` |

> **Every SWA has a unique deployment token.** Never reuse one token across SWAs —
> doing so deploys one site's content into another. Sites 2, 3 and 4 each use their
> own secret name above, distinct from the hackathon site.

## Live deployment URLs

| Site | Status | URL |
|------|--------|-----|
| Hackathon reference | ✅ live | https://white-ground-0c80a6f10.7.azurestaticapps.net |
| Docs / runbook | provisioned (AAD-gated) | _set after first deploy_ |
| Workshop companion | provisioned | _set after first deploy_ |
| Coach prep companion | ✅ live | https://gray-ground-07a6ae510.7.azurestaticapps.net |

> The coach site was the first of the new SWAs to deploy end-to-end via
> `deploy-coach-swa.yml` once `AZURE_STATIC_WEB_APPS_API_TOKEN_COACH` was set.
> Fill in the docs and workshop URLs (from each SWA's **Overview** blade) after
> their first successful deploy.

The site **URL is created when the Azure resource is created** (the portal shows it,
or the CLI prints `defaultHostname`).

> **On Codespaces / no `az`?** Use the **Azure Portal runbook** directly below — it
> needs nothing but a browser. The `az` CLI steps further down are an equivalent
> alternative for anyone who can run the CLI. Both end the same way: a per-site
> **deployment token** pasted into a GitHub repo secret, after which our existing
> workflows build and deploy.

---

## Azure Portal runbook (Codespaces-friendly, no `az`)

This is the recommended path when Conditional Access blocks `az`/`azd` from the
Codespace. **Do all of this in the browser.** Repeat it once per site you want to
publish, using the matching name + secret from this table:

| Site | SWA resource name (suggested) | GitHub repo secret to set | Source folder |
|------|-------------------------------|---------------------------|---------------|
| Docs | `swa-47doors-docs` | `AZURE_STATIC_WEB_APPS_API_TOKEN_DOCS` | `docs/` |
| Workshop | `swa-47doors-workshop` | `AZURE_STATIC_WEB_APPS_API_TOKEN_WORKSHOP` | `workshop-site/` |
| Coach | `swa-47doors-coach` | `AZURE_STATIC_WEB_APPS_API_TOKEN_COACH` | `coach-site/` |

### 1. Create the Static Web App

1. Go to the [Azure Portal](https://portal.azure.com) → search **Static Web Apps** →
   **Create**.
2. **Basics** tab:
   - **Subscription:** Cloudforce Sponsorship (`098ef2f6-cea4-4839-8093-ef90622e1b8c`).
   - **Resource Group:** `rg-ajcu-hackathon` (same RG as the hackathon site).
   - **Name:** the resource name from the table above (e.g. `swa-47doors-coach`).
   - **Plan type:** **Free** is fine for the public **Workshop** and **Coach** sites.
     Choose **Standard** for **Docs** (it uses a custom Entra app registration — see
     §3 below).
   - **Region:** pick the closest (e.g. **East US 2**).
3. **Deployment details** — this is the important part:
   - **Source:** choose **`Other`** (NOT "GitHub").
   - ⚠️ Do **not** pick GitHub here. Picking GitHub makes Azure commit a *new,
     competing* workflow file into the repo. We already have hand-written workflows
     (`deploy-*-swa.yml`); the **Other** option mints a deployment token without
     touching the repo, and our workflows use that token.
4. Click **Review + create** → **Create**. Wait for "Your deployment is complete".

### 2. Copy the deployment token → GitHub secret

1. Open the new Static Web App resource → left nav **Overview**. The **URL** shown
   here (e.g. `https://nice-pebble-0abc123.azurestaticapps.net`) is the **site URL**.
2. Left nav → **Settings → Configuration** (or **Overview → Manage deployment
   token**) → **Manage deployment token** → **Copy** the token value.
3. In GitHub: **`EstablishedCorp/47doors` → Settings → Secrets and variables →
   Actions → New repository secret**.
   - **Name:** the exact secret from the table (e.g. `AZURE_STATIC_WEB_APPS_API_TOKEN_COACH`).
   - **Secret:** paste the token. **Add secret.**

> **One token per site — never reuse.** Each SWA's token only deploys into that SWA.
> Pasting the wrong token deploys one site's content into another.

### 3. (Docs site only) Configure Entra (AAD) login — or every visitor gets 401

`docs/staticwebapp.config.json` gates `/*` behind Azure AD and references a custom
app registration. In the portal:

1. **Microsoft Entra ID → App registrations → New registration.** Add redirect URI
   `https://<your-docs-hostname>/.auth/login/aad/callback` (Web platform). Note the
   **Application (client) ID**. Create a **client secret** under *Certificates &
   secrets* and copy its value.
2. Back on the docs SWA → **Settings → Environment variables / Configuration** → add
   application settings **`AZURE_CLIENT_ID`** and **`AZURE_CLIENT_SECRET`** with those
   values → **Save**.

> **Want docs public instead** (skip §3)? Replace the `auth` + `routes` blocks in
> `docs/staticwebapp.config.json` with a single anonymous catch-all
> (`{ "route": "/*", "allowedRoles": ["anonymous"] }`), drop the `auth` section, and
> a Free-plan SWA works.

### 4. Trigger the deploy

The token is all the workflow needs. Kick it off either way:

- **GitHub UI:** **Actions** tab → pick the workflow (`Deploy Docs/Workshop/Coach
  Site to Azure Static Web Apps`) → **Run workflow** → branch `main` → **Run**.
- **Or** push any commit touching that site's source folder on `main`.

The run will now run the **Checkout** + **Build and Deploy** steps (previously
skipped by the guard) and publish to your SWA. Refresh the SWA **Overview** URL.

---

## `az` CLI alternative (only if you can run the CLI)

The sections below do exactly the same thing from a shell with Azure access.

## Prerequisites

```bash
az login
az account set --subscription 098ef2f6-cea4-4839-8093-ef90622e1b8c   # Cloudforce Sponsorship
RG=rg-ajcu-hackathon                                                  # same RG as the hackathon SWA
LOCATION=eastus2
```

You also need the GitHub CLI (`gh auth login`) to set repo secrets, or use the
GitHub UI: **Settings → Secrets and variables → Actions → New repository secret**.

---

## Site 2 — Docs SWA (login-gated)

### 1. Create the resource (prints the URL)

```bash
az staticwebapp create \
  --name swa-47doors-docs \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --sku Standard \
  --query "defaultHostname" -o tsv
```

The printed `defaultHostname` (e.g. `something-12345.azurestaticapps.net`) is the
**docs site URL** → `https://<defaultHostname>`.

> Standard SKU is required because the docs site uses a custom AAD app
> registration (see step 3). If you do not need a custom registration, the SWA's
> built-in AAD works on Free SKU too — but the bundled `staticwebapp.config.json`
> references `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` settings.

### 2. Capture the deployment token into the repo secret

```bash
TOKEN=$(az staticwebapp secrets list \
  --name swa-47doors-docs --resource-group "$RG" \
  --query "properties.apiKey" -o tsv)

gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN_DOCS --body "$TOKEN" \
  --repo EstablishedCorp/47doors
```

### 3. (Docs only) Configure AAD app settings — REQUIRED or every visitor gets 401

`docs/staticwebapp.config.json` gates `/*` behind Azure AD login and references a
custom app registration. Set its client id/secret as SWA application settings:

```bash
az staticwebapp appsettings set \
  --name swa-47doors-docs --resource-group "$RG" \
  --setting-names \
    AZURE_CLIENT_ID="<entra-app-client-id>" \
    AZURE_CLIENT_SECRET="<entra-app-client-secret>"
```

Create the Entra app registration first (Azure Portal → Microsoft Entra ID → App
registrations → New), add the SWA redirect URI
`https://<defaultHostname>/.auth/login/aad/callback`, and create a client secret.

> **Want the docs site public instead?** Replace the `auth` + `routes` blocks in
> `docs/staticwebapp.config.json` with a single anonymous catch-all
> (`{ "route": "/*", "allowedRoles": ["anonymous"] }`) and drop the `auth` section.
> Then you can skip step 3 and use the Free SKU.

### 4. Deploy

```bash
# Trigger the workflow (any push touching docs/, or manually):
gh workflow run deploy-docs-swa.yml --repo EstablishedCorp/47doors
```

---

## Site 3 — Workshop SWA (public)

### 1. Create the resource (prints the URL)

```bash
az staticwebapp create \
  --name swa-47doors-workshop \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --query "defaultHostname" -o tsv
```

The printed `defaultHostname` is the **workshop site URL** → `https://<defaultHostname>`.

### 2. Capture the deployment token into the repo secret

```bash
TOKEN=$(az staticwebapp secrets list \
  --name swa-47doors-workshop --resource-group "$RG" \
  --query "properties.apiKey" -o tsv)

gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN_WORKSHOP --body "$TOKEN" \
  --repo EstablishedCorp/47doors
```

### 3. Deploy

```bash
gh workflow run deploy-workshop-swa.yml --repo EstablishedCorp/47doors
```

The workshop workflow builds the Vite app (`app_location: workshop-site`,
`output_location: dist`) and uploads it. `staticwebapp.config.json` lives in
`workshop-site/public/` so Vite copies it into `dist/`.

---

## Site 4 — Coach SWA (public)

The coach prep companion site (`coach-site/`) is public, like the workshop site,
and uses its **own** deployment token. Never reuse the workshop (or any other)
token here — that would deploy one site's content into another.

### 1. Create the resource (prints the URL)

```bash
az staticwebapp create \
  --name swa-47doors-coach \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --query "defaultHostname" -o tsv
```

The printed `defaultHostname` is the **coach site URL** → `https://<defaultHostname>`.

### 2. Capture the deployment token into the repo secret

```bash
TOKEN=$(az staticwebapp secrets list \
  --name swa-47doors-coach --resource-group "$RG" \
  --query "properties.apiKey" -o tsv)

gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN_COACH --body "$TOKEN" \
  --repo EstablishedCorp/47doors
```

### 3. Deploy

```bash
gh workflow run deploy-coach-swa.yml --repo EstablishedCorp/47doors
```

The coach workflow builds the Vite app (`app_location: coach-site`,
`output_location: dist`) and uploads it. `staticwebapp.config.json` lives in
`coach-site/public/` so Vite copies it into `dist/`. Until the
`AZURE_STATIC_WEB_APPS_API_TOKEN_COACH` secret is set, the workflow **no-ops with
a warning** (the guard step), so merging is safe before Azure is provisioned.

---

## Verifying

```bash
# List all SWAs + their URLs in the resource group:
az staticwebapp list --resource-group "$RG" \
  --query "[].{name:name, url:defaultHostname}" -o table
```

Then open each `https://<url>`:

- **Workshop** → loads the public companion site immediately.
- **Docs** → redirects to a Microsoft sign-in, then loads after auth.

Until the token secrets are set, both workflows **no-op with a warning** (the guard
step), so merging this change is safe before Azure is provisioned.
