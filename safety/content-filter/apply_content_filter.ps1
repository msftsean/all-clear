<#
.SYNOPSIS
  Creates the "allclear-guardrails" custom content filter (RAI policy) on the All Clear
  Azure OpenAI account and attaches it to the gpt-5.1 deployment.

  After this runs, the named filter is visible in the Azure AI Foundry / Azure OpenAI portal
  under  Guardrails + controls -> Content filters , and every call to the deployment is
  governed by it. This is how you SHOW the guardrails in Foundry instead of pointing at code.

.WHY THE THRESHOLDS ARE TUNED THIS WAY
  All Clear is a public-safety incident-triage agent. Real emergency signals legitimately
  mention violence ("power line down, sparking near a school") and self-harm ("a student
  said they want to hurt themselves"). Hard-blocking those at the INPUT would stop the agent
  from ever seeing them - including a person in crisis. So Violence/Selfharm on the *prompt*
  side are set to "High" (block only the most severe), and the app's own crisis-escalation
  guardrail routes the rest to a human. Jailbreak, Indirect Attack, Hate, Sexual, Profanity
  and protected material stay blocking. Platform filter + app guardrail working together.

.PREREQS
  az login; Contributor on the user-supplied resource group and Azure OpenAI account.
#>

param(
  [string]$Subscription,
  [Parameter(Mandatory = $true)][string]$ResourceGroup,
  [Parameter(Mandatory = $true)][string]$Account,
  [string]$PolicyName = "allclear-guardrails",
  [Parameter(Mandatory = $true)][string]$DeploymentName,
  [string]$ApiVersion = "2024-10-01"
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
$accountContextJson = az account show -o json 2>&1
if ($LASTEXITCODE -ne 0) {
  throw "No Azure CLI session is active. Run 'az login' and select the subscription you will use."
}
$accountContext = $accountContextJson | ConvertFrom-Json
if ([string]::IsNullOrWhiteSpace($Subscription)) {
  $Subscription = $accountContext.id
  Write-Host "Subscription not supplied; using the current Azure CLI subscription '$Subscription'."
}
Assert-NonPlaceholder $Subscription "Subscription"
Assert-NonPlaceholder $ResourceGroup "ResourceGroup"
Assert-NonPlaceholder $Account "Account"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$policyPath = Join-Path $here "allclear-guardrails.rai.json"
if (-not (Test-Path $policyPath)) {
  throw "Policy definition not found at '$policyPath'. Run this script from the repository checkout."
}
$policyBody = Get-Content $policyPath -Raw

$base = "https://management.azure.com/subscriptions/$Subscription/resourceGroups/$ResourceGroup/providers/Microsoft.CognitiveServices/accounts/$Account"

Write-Host "1/3  Creating custom content filter '$PolicyName' on $Account ..."
$tmp = New-TemporaryFile
try {
  $policyBody | Out-File -FilePath $tmp -Encoding utf8
  $raiUrl = "$base/raiPolicies/$PolicyName" + "?api-version=$ApiVersion"
  az rest --method put `
    --url $raiUrl `
    --body "@$($tmp.FullName)" `
    --headers "Content-Type=application/json" | Out-Null
  if ($LASTEXITCODE -ne 0) {
    throw "The content-filter request failed. Confirm Contributor access to account '$Account'."
  }
} finally {
  Remove-Item $tmp -ErrorAction SilentlyContinue
}

Write-Host "2/3  Attaching '$PolicyName' to deployment '$DeploymentName' ..."
$depJson = az cognitiveservices account deployment show -g $ResourceGroup -n $Account --deployment-name $DeploymentName --subscription $Subscription -o json 2>&1
if ($LASTEXITCODE -ne 0) {
  throw "Deployment '$DeploymentName' was not found on account '$Account'. Pass the deployment name with -DeploymentName."
}
$dep = $depJson | ConvertFrom-Json
$model = $dep.properties.model.name
$ver = $dep.properties.model.version
$skuName = $dep.sku.name
$skuCap = $dep.sku.capacity
$patch = @{
  properties = @{
    model = @{ format = "OpenAI"; name = $model; version = $ver }
    raiPolicyName = $PolicyName
  }
  sku = @{ name = $skuName; capacity = $skuCap }
} | ConvertTo-Json -Depth 6
$tmp2 = New-TemporaryFile
try {
  $patch | Out-File -FilePath $tmp2 -Encoding utf8
  $depUrl = "$base/deployments/$DeploymentName" + "?api-version=$ApiVersion"
  az rest --method put `
    --url $depUrl `
    --body "@$($tmp2.FullName)" `
    --headers "Content-Type=application/json" | Out-Null
  if ($LASTEXITCODE -ne 0) {
    throw "Attaching the content filter failed. Confirm deployment write access on account '$Account'."
  }
} finally {
  Remove-Item $tmp2 -ErrorAction SilentlyContinue
}

Write-Host "3/3  Verifying ..."
az cognitiveservices account deployment show -g $ResourceGroup -n $Account --deployment-name $DeploymentName --subscription $Subscription `
  --query "{deployment:name, raiPolicy:properties.raiPolicyName}" -o table

Write-Host "`nDone. Open the deployment in Azure AI Foundry / Azure OpenAI Studio ->"
Write-Host "Guardrails + controls -> Content filters to show '$PolicyName'."
