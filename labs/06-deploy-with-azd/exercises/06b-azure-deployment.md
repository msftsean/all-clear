# Exercise 06b: Azure Deployment

**Duration:** 60 minutes
**Objective:** Deploy your containerized application to Azure using Azure Developer CLI (azd)

---

## Overview

In this exercise, you will use Azure Developer CLI to provision Azure infrastructure and deploy All Clear with a single command. By the end, your All Clear incident-triage pipeline will be running in Azure Container Apps.

---

## Prerequisites

- [ ] Exercise 06a completed (local Docker test successful)
- [ ] Azure subscription with Contributor access
- [ ] Azure CLI installed (`az --version`)
- [ ] Azure Developer CLI installed (`azd version`)

---

## Task 1: Install Azure Developer CLI (10 minutes)

### 1.1 Check if azd is Installed

```bash
azd version
```

If installed, you'll see output like:

```
azd version 1.5.0 (commit abc123)
```

### 1.2 Install azd (if needed)

**Windows (PowerShell as Administrator):**

```powershell
winget install microsoft.azd
```

**macOS:**

```bash
brew tap azure/azd && brew install azd
```

**Linux:**

```bash
curl -fsSL https://aka.ms/install-azd.sh | bash
```

### 1.3 Verify Installation

```bash
azd version
```

**Checkpoint:** azd version command shows version number.

---

## Task 2: Authenticate with Azure (5 minutes)

### 2.1 Login to Azure

```bash
azd auth login
```

This opens a browser window. Sign in with your Azure credentials.

**Expected:** After successful login:

```
Logged in to Azure.
```

If interactive login fails with `AADSTS53003`, use service principal auth:

```bash
az login --service-principal \
  -u <AZURE_CLIENT_ID> \
  -p <AZURE_CLIENT_SECRET> \
  --tenant <AZURE_TENANT_ID>

az account set --subscription <AZURE_SUBSCRIPTION_ID>

azd auth login \
  --client-id <AZURE_CLIENT_ID> \
  --client-secret <AZURE_CLIENT_SECRET> \
  --tenant-id <AZURE_TENANT_ID> \
  --no-prompt
```

### 2.2 Verify Azure CLI Authentication (Optional)

```bash
az account show
```

**Expected:** Shows your Azure subscription details.

### 2.3 Set Subscription (if multiple)

If you have multiple subscriptions:

```bash
# List subscriptions
az account list --output table

# Set the correct one
az account set --subscription "<subscription-name-or-id>"
```

**Checkpoint:** `azd auth login` succeeds and shows correct account.

---

## Task 3: Configure azd Environment (10 minutes)

### 3.1 Review azure.yaml

Verify the `azure.yaml` file exists in your project root:

```bash
cat azure.yaml
```

**Expected contents:**

```yaml
name: all-clear
metadata:
  template: all-clear@0.1.0

services:
  backend:
    project: ./backend
    language: python
    host: containerapp
    docker:
      path: Dockerfile
      remoteBuild: true

  frontend:
    project: ./frontend
    language: js
    host: containerapp
    docker:
      path: Dockerfile
      remoteBuild: true

infra:
  provider: bicep
  path: ./infra
  module: main
```

### 3.2 Initialize azd (if needed)

If you haven't initialized azd in this project:

```bash
azd init
```

Follow the prompts to confirm project settings.

### 3.3 Create a New Environment

```bash
# Create a development environment
azd env new dev
```

### 3.4 Set Environment Variables

```bash
# Set Azure region
azd env set AZURE_LOCATION southcentralus

# Set required deployment scope
azd env set AZURE_SUBSCRIPTION_ID <your-subscription-id>
azd env set AZURE_RESOURCE_GROUP <your-resource-group>

# View current environment
azd env get-values
```

### 3.5 Choose a Unique Name

Azure resource names must be globally unique. Set a unique prefix:

```bash
# Use your initials or team name
azd env set AZURE_ENV_NAME allclear-<your-initials>
```

### Voice & Phone Configuration (Optional)

If your deployment includes voice or phone features, add these to your Container App configuration:

```env
# Voice (browser)
VOICE_ENABLED=true
AZURE_OPENAI_REALTIME_DEPLOYMENT=gpt-realtime

# Phone (requires ACS resource — coach will demo this)
PHONE_ENABLED=true
AZURE_ACS_ENDPOINT=https://your-acs.communication.azure.com
ACS_PHONE_NUMBER=+15551234567
PHONE_CALLBACK_BASE_URL=https://your-app.azurecontainerapps.io
```

> **Note:** Phone requires a public HTTPS URL for Event Grid webhooks. Your Container App URL works for this. Voice works with the same Azure OpenAI endpoint—just needs the Realtime deployment.

**Checkpoint:** `azd env get-values` shows your configuration.

---

## Task 4: Provision Infrastructure (15 minutes)

### 4.1 Preview Infrastructure (Optional)

Before provisioning, you can preview what will be created:

```bash
azd provision --preview
```

This shows the Bicep deployment plan without executing it.

### 4.2 Run azd up

The `azd up` command provisions infrastructure AND deploys All Clear:

```bash
azd up
```

For scripted runs (Codespaces/CI), prefer:

```bash
azd up --no-prompt
```

### 4.3 Monitor Provisioning Progress

The command will show progress:

```
Provisioning Azure resources (azd provision)

Provisioning Azure resources can take some time.

  (✓) Done: Resource group: rg-<azd-env>
  (✓) Done: Log Analytics workspace: <prefix>-logs
  (✓) Done: Container Apps Environment: <prefix>-env
  (✓) Done: Container Registry: <prefix-without-dashes>acr
  (✓) Done: Azure OpenAI: <prefix>-openai
  ...

Deploying services (azd deploy)

  (✓) Done: Building container image
  (✓) Done: Pushing to registry
  (✓) Done: Service backend

SUCCESS: All Clear was provisioned and deployed to Azure.
```

**Note:** This process takes 10-15 minutes on first run.

### 4.4 Handle Provisioning Errors

If provisioning fails:

```bash
# Check detailed error
azd provision --debug

# Common issues:
# - Subscription doesn't have required resource providers
# - Region doesn't support certain services
# - Quota limits exceeded
```

If you see `MissingSubscriptionRegistration`, ask a subscription admin to run:

```bash
az provider register -n Microsoft.App --subscription <sub-id> --wait
az provider register -n Microsoft.Web --subscription <sub-id> --wait
```

If Cosmos fails due regional capacity, use a dedicated Cosmos region (for example `canadacentral`) separate from the app hosting region.

**Checkpoint:** `azd up` completes with "SUCCESS" message.

---

## Task 5: Verify Deployment (10 minutes)

### 5.1 Get Service Endpoints

```bash
azd show
```

**Expected output:**

```
Showing deployed resources for environment: dev

Service           Endpoint
backend           https://<prefix>-backend.<region>.azurecontainerapps.io
```

### 5.2 Store Backend URL

```bash
# Get the backend URL
BACKEND_URL=$(azd env get-value AZURE_CONTAINERAPP_URL)
echo "Backend URL: $BACKEND_URL"
```

### 5.3 Test Health Endpoint

```bash
# Test the health endpoint
curl -s "$BACKEND_URL/api/health" | jq .
```

**Expected response:**

```json
{
  "status": "healthy",
  "mock_mode": false,
  "domain": "all-clear-incident-triage"
}
```

### 5.4 Test Signals Endpoint

```bash
# Test the signals API
curl -s -X POST "$BACKEND_URL/api/signals" \
  -H "Content-Type: application/json" \
  -d '{"message": "Power line down across Main St", "channel": "submitted-report"}' | jq .
```

**Expected:** JSON `PipelineResult` with classification, routing, action, an `AC-####` incident id, SEV1 severity, and queue `field-operations` for this example signal.

### Verify Voice & Phone (Optional)

```bash
# Voice health
curl https://your-app.azurecontainerapps.io/api/realtime/health

# Phone health
curl https://your-app.azurecontainerapps.io/api/phone/health
```

Both should return `{"available": true}` when properly configured, or `{"available": true, "mock_mode": true}` if running in mock mode.

### 5.5 Access Frontend (Optional)

Open the frontend URL from `azd show` or `azd env get-value AZURE_FRONTEND_URL`. The frontend is also deployed as an Azure Container App in the real All Clear `azure.yaml`.

### 5.6 Verify in Azure Portal

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Find your resource group from `azd env get-value AZURE_RESOURCE_GROUP`
3. Verify all resources are created:
   - Container Apps Environment
   - Container App (backend)
   - Container Registry
   - Log Analytics Workspace

- frontend Container App (optional)

**Additional Resources for Voice/Phone (Optional):**
- Azure OpenAI: `gpt-realtime` deployment (for voice)
- Azure Communication Services resource (for phone)
- Event Grid system topic + webhook subscription pointing to `/api/phone/incoming`
- Managed Identity: `Cognitive Services OpenAI User` role on the OpenAI resource

**Checkpoint:** Health endpoint returns 200 with healthy status.

---

## Task 6: View Logs and Monitoring (10 minutes)

### 6.1 Stream Container Logs

```bash
# Get resource group and backend Container App name
RG=$(azd env get-value AZURE_RESOURCE_GROUP)
BACKEND_APP=$(az containerapp list --resource-group "$RG" --query '[?tags."azd-service-name"==`backend`].name | [0]' -o tsv)

# Stream logs from backend
az containerapp logs show \
  --name "$BACKEND_APP" \
  --resource-group "$RG" \
  --follow
```

Press `Ctrl+C` to stop streaming.

### 6.2 View System Logs

```bash
az containerapp logs show \
  --name "$BACKEND_APP" \
  --resource-group "$RG" \
  --type system
```

### 6.3 Check Container Status

```bash
az containerapp show \
  --name "$BACKEND_APP" \
  --resource-group "$RG" \
  --query "properties.runningStatus"
```

**Expected:** `"Running"`

### 6.4 View Metrics in Portal

1. Go to Azure Portal
2. Navigate to your Container App
3. Click "Metrics" in the left menu
4. View:
   - Requests per second
   - Response time
   - CPU/Memory usage

### 6.5 Search Logs in Log Analytics

1. Go to Azure Portal
2. Find your Log Analytics workspace
3. Click "Logs"
4. Run a KQL query:

```kusto
ContainerAppConsoleLogs_CL
| where ContainerAppName_s contains "backend"
| project TimeGenerated, Log_s
| order by TimeGenerated desc
| take 50
```

**Checkpoint:** Can view container logs and verify application is running.

---

## Task 7: Make a Code Change and Redeploy (Optional)

### 7.1 Make a Small Change

Edit `backend/app/api/routes.py` to temporarily add a build marker to the health response:

```python
@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "mock_mode": settings.use_mock_services,
        "domain": "all-clear-incident-triage",
        "build": "lab06-redeploy"
    }
```

### 7.2 Redeploy

```bash
# Deploy only (no infrastructure changes)
azd deploy
```

This is faster than `azd up` because it only rebuilds and deploys the container.

### 7.3 Verify the Change

```bash
curl -s "$BACKEND_URL/api/health" | jq .build
```

**Expected:** `"lab06-redeploy"`

---

## Task 8: Clean Up (When Done with Lab)

### 8.1 Delete All Resources

**Warning:** This permanently deletes all Azure resources!

```bash
azd down
```

Confirm when prompted.

### 8.2 Verify Deletion

```bash
az group show --name $RG 2>/dev/null || echo "Resource group deleted"
```

---

## Verification Checklist

Before completing Lab 06, confirm:

- [ ] `azd auth login` succeeded
- [ ] `azd up` completed without errors
- [ ] `azd show` displays service endpoints
- [ ] Health endpoint returns `{"status": "healthy", ...}`
- [ ] Can view container logs in Azure
- [ ] Container shows "Running" status
- [ ] (Optional) Redeploy works after code change

---

## Troubleshooting Guide

### Issue: "azd up" fails with authentication error

```bash
# Re-authenticate
azd auth logout
azd auth login

# Also ensure Azure CLI is authenticated
az login
```

### Issue: Container fails health check

```bash
# Check container logs
az containerapp logs show \
  --name "$BACKEND_APP" \
  --resource-group "$RG" \
  --type console

# Verify the app starts correctly by checking startup logs
```

### Issue: "Quota exceeded" error

```bash
# Try a different region
azd env set AZURE_LOCATION westus2
azd up
```

### Issue: Build fails in Azure Container Registry

```bash
# Verify Docker builds locally first
docker compose build

# Check ACR build logs
az acr task logs --registry <acr-name>
```

### Issue: Environment variables not set in Container App

```bash
# Check current environment variables
az containerapp show \
  --name "$BACKEND_APP" \
  --resource-group "$RG" \
  --query "properties.template.containers[0].env"

# Update manually if needed
az containerapp update \
  --name "$BACKEND_APP" \
  --resource-group "$RG" \
  --set-env-vars "KEY=value"
```

---

## Summary

You have successfully:

1. Installed and authenticated Azure Developer CLI
2. Configured an azd environment
3. Provisioned Azure infrastructure with `azd up`
4. Deployed your containerized application
5. Verified the deployment with health checks
6. Accessed monitoring and logs

Your All Clear incident-triage system is now running in production on Azure Container Apps.

---

## Key Commands Reference

| Command                 | Purpose                        |
| ----------------------- | ------------------------------ |
| `azd auth login`        | Authenticate with Azure        |
| `azd env new <name>`    | Create new environment         |
| `azd env set KEY value` | Set environment variable       |
| `azd up`                | Provision and deploy           |
| `azd provision`         | Only provision infrastructure  |
| `azd deploy`            | Only deploy application        |
| `azd show`              | Show deployed resources        |
| `azd env get-values`    | Show all environment variables |
| `azd down`              | Delete all resources           |

---

## Congratulations!

You have completed Lab 06 and successfully deployed your All Clear incident-triage pipeline to Azure. The All Clear pipeline is now:

- Running in Azure Container Apps
- Accessible via public HTTPS endpoint
- Monitored with health checks and logging
- Ready for production use

This completes the boot camp deployment labs!
