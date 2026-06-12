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

.PREREQS  az login; contributor + user-access-admin (for the role assignment) on rg-allclear.
#>

param(
  [string]$Subscription = "098ef2f6-cea4-4839-8093-ef90622e1b8c",
  [string]$ResourceGroup = "rg-allclear",
  [string]$Location = "eastus2",
  [string]$Account = "allclear-foundry",
  [string]$SubDomain = "allclear-foundry-kt5fw24guxoxy",
  [string]$Project = "allclear-redteam",
  [string]$ApiVersion = "2025-04-01-preview"
)

$ErrorActionPreference = "Stop"
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
az rest --method put --url "$($base)?api-version=$ApiVersion" --body "@$t1" --headers "Content-Type=application/json" | Out-Null
Remove-Item $t1

Write-Host "2/4  Creating project '$Project' ..."
$proj = @{
  location = $Location
  identity = @{ type = "SystemAssigned" }
  properties = @{ displayName = "All Clear Red Team"; description = "AI red teaming + safety evals for the All Clear incident-triage agent." }
} | ConvertTo-Json -Depth 6
$t2 = New-TemporaryFile; $proj | Out-File $t2 -Encoding utf8
az rest --method put --url "$base/projects/$($Project)?api-version=$ApiVersion" --body "@$t2" --headers "Content-Type=application/json" | Out-Null
Remove-Item $t2

Write-Host "3/4  Granting signed-in user the 'Azure AI User' data-plane role ..."
$me = az ad signed-in-user show --query id -o tsv
# Azure AI User
az role assignment create --assignee-object-id $me --assignee-principal-type User `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --scope "/subscriptions/$Subscription/resourceGroups/$ResourceGroup/providers/Microsoft.CognitiveServices/accounts/$Account" 2>$null | Out-Null

Write-Host "4/4  Resolving project endpoint ..."
$endpoint = "https://$SubDomain.services.ai.azure.com/api/projects/$Project"
Write-Host "`nProject endpoint:`n  $endpoint`n"
Write-Host "Use it:  `$env:AZURE_AI_PROJECT_ENDPOINT = `"$endpoint`""
