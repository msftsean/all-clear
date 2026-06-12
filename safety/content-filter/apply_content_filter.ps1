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
  az login;  contributor on rg-allclear in the Cloudforce subscription.
#>

param(
  [string]$Subscription = "098ef2f6-cea4-4839-8093-ef90622e1b8c",
  [string]$ResourceGroup = "rg-allclear",
  [string]$Account = "allclear-kt5fw24guxoxy-openai",
  [string]$PolicyName = "allclear-guardrails",
  [string]$DeploymentName = "gpt-5.1",
  [string]$ApiVersion = "2024-10-01"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$policyBody = Get-Content (Join-Path $here "allclear-guardrails.rai.json") -Raw

$base = "https://management.azure.com/subscriptions/$Subscription/resourceGroups/$ResourceGroup/providers/Microsoft.CognitiveServices/accounts/$Account"

Write-Host "1/3  Creating custom content filter '$PolicyName' on $Account ..."
$tmp = New-TemporaryFile
$policyBody | Out-File -FilePath $tmp -Encoding utf8
$raiUrl = "$base/raiPolicies/$PolicyName" + "?api-version=$ApiVersion"
az rest --method put `
  --url $raiUrl `
  --body "@$($tmp.FullName)" `
  --headers "Content-Type=application/json" | Out-Null
Remove-Item $tmp

Write-Host "2/3  Attaching '$PolicyName' to deployment '$DeploymentName' ..."
$dep = az cognitiveservices account deployment show -g $ResourceGroup -n $Account --deployment-name $DeploymentName --subscription $Subscription -o json | ConvertFrom-Json
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
$patch | Out-File -FilePath $tmp2 -Encoding utf8
$depUrl = "$base/deployments/$DeploymentName" + "?api-version=$ApiVersion"
az rest --method put `
  --url $depUrl `
  --body "@$($tmp2.FullName)" `
  --headers "Content-Type=application/json" | Out-Null
Remove-Item $tmp2

Write-Host "3/3  Verifying ..."
az cognitiveservices account deployment show -g $ResourceGroup -n $Account --deployment-name $DeploymentName --subscription $Subscription `
  --query "{deployment:name, raiPolicy:properties.raiPolicyName}" -o table

Write-Host "`nDone. Open the deployment in Azure AI Foundry / Azure OpenAI Studio ->"
Write-Host "Guardrails + controls -> Content filters to show '$PolicyName'."
