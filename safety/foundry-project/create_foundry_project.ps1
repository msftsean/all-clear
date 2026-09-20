<#
.SYNOPSIS
  Provisions an Azure AI Foundry project to host All Clear's AI Red Teaming results.

  All Clear was deployed on plain Azure OpenAI accounts (no Foundry project existed). The
  AI Red Teaming Agent uploads its scan to a Foundry *project*, which must live in a region
  where the red-teaming / safety-evaluation service runs:
      East US 2, North Central US, France Central, Sweden Central, Switzerland West.
  (The backend target can be anywhere - it is called over HTTPS.)

  Creates an AIServices account (kind=AIServices, project management on) + a project, then
  grants the signed-in user the data-plane "Azure AI User" role so they can run scans and
  view results. Prints the project endpoint to use as AZURE_AI_PROJECT_ENDPOINT.

.PREREQS  az login; Contributor + User Access Administrator (for the role assignment) on the
          user-supplied resource group.
#>

param(
  [string]$Subscription,
  [Parameter(Mandatory = $true)][string]$ResourceGroup,
  [Parameter(Mandatory = $true)][string]$Account,
  [Parameter(Mandatory = $true)][string]$Project,
  [ValidateSet("eastus2", "northcentralus", "francecentral", "swedencentral", "switzerlandwest")]
  [string]$Location = "eastus2",
  [string]$SubDomain,
  [string]$ApiVersion = "2025-04-01-preview"
)

$ErrorActionPreference = "Stop"

function Assert-NonPlaceholder([string]$Value, [string]$Name) {
  if ([string]::IsNullOrWhiteSpace($Value) -or $Value -match "<[^>]+>|YOUR_|REPLACE_ME") {
    throw "$Name is required and must be a real value. See -? for examples."
  }
}

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
  throw "Azure CLI (az) is required. Install it, then run 'az login' before retrying."
}

try {
  $accountJson = az account show -o json 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "No Azure CLI session is active. Run 'az login' and select the subscription you will use."
  }
  $accountContext = $accountJson | ConvertFrom-Json
} catch {
  throw "Unable to read the Azure CLI account context. Run 'az login', then retry. Details: $($_.Exception.Message)"
}

if ([string]::IsNullOrWhiteSpace($Subscription)) {
  $Subscription = $accountContext.id
  Write-Host "Subscription not supplied; using the current Azure CLI subscription '$Subscription'."
}
Assert-NonPlaceholder $Subscription "Subscription"
Assert-NonPlaceholder $ResourceGroup "ResourceGroup"
Assert-NonPlaceholder $Account "Account"
Assert-NonPlaceholder $Project "Project"

if ([string]::IsNullOrWhiteSpace($SubDomain)) {
  $SubDomain = $Account.ToLowerInvariant()
  Write-Host "SubDomain not supplied; deriving it from Account as '$SubDomain'."
}
Assert-NonPlaceholder $SubDomain "SubDomain"

$subscriptionContext = az account show --subscription $Subscription -o json 2>&1
if ($LASTEXITCODE -ne 0) {
  throw "Subscription '$Subscription' was not found or is not accessible. Run 'az account list' and pass an accessible subscription ID."
}
$null = $subscriptionContext | ConvertFrom-Json

$base = "https://management.azure.com/subscriptions/$Subscription/resourceGroups/$ResourceGroup/providers/Microsoft.CognitiveServices/accounts/$Account"

Write-Host "1/4  Creating AIServices (Foundry) account '$Account' in $Location ..."
$acct = @{
  location = $Location
  kind     = "AIServices"
  sku      = @{ name = "S0" }
  identity = @{ type = "SystemAssigned" }
  properties = @{ allowProjectManagement = $true; customSubDomainName = $SubDomain }
} | ConvertTo-Json -Depth 6
$t1 = New-TemporaryFile; $acct | Out-File $t1 -Encoding utf8
try {
  az rest --method put --url "$($base)?api-version=$ApiVersion" --body "@$t1" --headers "Content-Type=application/json" | Out-Null
  if ($LASTEXITCODE -ne 0) {
    throw "The Foundry account request failed. Confirm Contributor access to resource group '$ResourceGroup'."
  }
} finally {
  Remove-Item $t1 -ErrorAction SilentlyContinue
}

Write-Host "2/4  Creating project '$Project' ..."
$proj = @{
  location = $Location
  identity = @{ type = "SystemAssigned" }
  properties = @{ displayName = "All Clear Red Team"; description = "AI red teaming + safety evals for the All Clear incident-triage agent." }
} | ConvertTo-Json -Depth 6
$t2 = New-TemporaryFile; $proj | Out-File $t2 -Encoding utf8
try {
  az rest --method put --url "$base/projects/$($Project)?api-version=$ApiVersion" --body "@$t2" --headers "Content-Type=application/json" | Out-Null
  if ($LASTEXITCODE -ne 0) {
    throw "The Foundry project request failed. Confirm that project management is allowed on the account."
  }
} finally {
  Remove-Item $t2 -ErrorAction SilentlyContinue
}

Write-Host "3/4  Granting signed-in user the 'Azure AI User' data-plane role ..."
$me = az ad signed-in-user show --query id -o tsv
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($me)) {
  throw "Unable to resolve the signed-in user. Run 'az login' with a user identity, then retry."
}
# Azure AI User
az role assignment create --assignee-object-id $me --assignee-principal-type User `
  --role "Azure AI User" `
  --scope "/subscriptions/$Subscription/resourceGroups/$ResourceGroup/providers/Microsoft.CognitiveServices/accounts/$Account" | Out-Null
if ($LASTEXITCODE -ne 0) {
  throw "Role assignment failed. An administrator must grant your identity Azure AI User on the Foundry account."
}

Write-Host "4/4  Resolving project endpoint ..."
$endpoint = "https://$SubDomain.services.ai.azure.com/api/projects/$Project"
Write-Host "`nProject endpoint:`n  $endpoint`n"
Write-Host "Use it:  `$env:AZURE_AI_PROJECT_ENDPOINT = `"$endpoint`""
