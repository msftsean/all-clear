# Azure Event Preflight

This is the facilitator checklist for the All Clear Azure stages. Complete it
before participants arrive and repeat the short checks on event day. The
baseline participant path is a shared, already-running backend plus an
individual APIM Consumption gateway. Individual full `azd up` deployments are
an optional deep dive, not a prerequisite for the timed workshop.

## 1. Facilitator preflight (24–48 hours before)

- [ ] Confirm the event subscription, tenant, target region, and billing owner.
- [ ] Choose one primary region (the load-tested path is `eastus`) and one
      fallback region for capacity incidents.
- [ ] Confirm the facilitator account can create resource groups, assign
      roles, and register providers, or arrange for a subscription admin to do
      those steps before the event.
- [ ] Create a facilitator resource group for the shared backend and record its
      name and expiry/deletion date.
- [ ] Deploy and smoke-test one shared backend with `azd up`, or retain a
      previously verified deployment. Record its HTTPS URL and `/api/health`
      response.
- [ ] Seed the shared AI Search `knowledge-base` index and verify one
      representative chat/signal request.
- [ ] Create or identify the Application Insights component that will receive
      APIM diagnostics.
- [ ] Record the shared backend URL, OpenAPI URL, APIM naming roster, fallback
      gateway URL, and the on-call facilitator's contact in the event sheet.
- [ ] Prepare a participant name list and deterministic suffixes such as
      `p01`–`p20`. APIM names are globally unique; never let participants
      guess names independently.
- [ ] Run the 20-participant APIM dress rehearsal below, then leave the
      gateways available only if the event requires them.

## 2. Permissions, RBAC, and identity

Each participant using the baseline path needs:

- Azure CLI and Azure Developer CLI installed, Docker running only for the
  optional full-deployment lane.
- `Reader` on the subscription or resource group to inspect the shared
  backend, plus `Contributor` on their own APIM resource group to create,
  import, update, and delete the gateway.
- Permission to create resource groups if participants create their own
  groups; otherwise staff creates the groups in advance.
- `Microsoft.ApiManagement/service/*` permissions for APIM operations, plus
  `Microsoft.Resources/subscriptions/resourceGroups/*` if they create their
  own resource group.
- For Application Insights logging, permission to create APIM loggers and
  diagnostics and access to the target Application Insights component. A
  facilitator can perform this step centrally.
- For JWT validation, an Entra app registration or other OIDC issuer, the
  tenant ID, issuer metadata URL, and agreed audience (for example
  `api://allclear`). A valid test token must be available before the stage.
- For managed-identity Azure OpenAI access in a full deployment, the Container
  App identity needs `Cognitive Services OpenAI User` on the OpenAI resource.
  Do not distribute API keys in participant materials.

Check access before the event:

```bash
az account show --query "{tenant:tenantId,subscription:id,user:user.name}" -o table
az group show --name "$SHARED_RG" --query "{name:name,location:location}" -o table
az provider show --namespace Microsoft.ApiManagement --query registrationState -o tsv
az role assignment list --assignee "$(az account show --query user.name -o tsv)" \
  --scope "/subscriptions/$(az account show --query id -o tsv)" \
  --include-inherited --query "[].{role:roleDefinitionName,scope:scope}" -o table
```

The role listing is evidence for review, not a substitute for the exact
resource-group assignment. A participant who cannot create or delete an APIM
instance must use a staff-created resource group or the pre-created gateway
fallback.

## 3. Subscription, quota, and capacity checks

Run these checks in the target subscription and region. Registration must be
`Registered`; quota output is a signal to escalate, not a guarantee that a
deployment will succeed.

```bash
az account list-locations --query "[?name=='eastus'].{name:name,displayName:displayName}" -o table
for ns in Microsoft.App Microsoft.CognitiveServices Microsoft.DocumentDB \
  Microsoft.Search Microsoft.ContainerRegistry Microsoft.KeyVault \
  Microsoft.OperationalInsights Microsoft.ApiManagement \
  Microsoft.Communication Microsoft.EventGrid Microsoft.Insights; do
  az provider show --namespace "$ns" --query "{namespace:namespace,state:registrationState}" -o table
done

az vm list-usage --location eastus \
  --query "[?contains(name.value, 'cores')].{name:name.localizedValue,current:currentValue,limit:limit}" -o table
```

If a provider is not `Registered`, the subscription administrator should run
the following before the event and wait for completion; participants should
not spend workshop time waiting for registration:

```bash
for ns in Microsoft.App Microsoft.CognitiveServices Microsoft.DocumentDB \
  Microsoft.Search Microsoft.ContainerRegistry Microsoft.KeyVault \
  Microsoft.OperationalInsights Microsoft.ApiManagement \
  Microsoft.Communication Microsoft.EventGrid Microsoft.Insights; do
  az provider register --namespace "$ns" --wait
done
```

Also check the Azure portal for subscription spending limits, regional
capacity advisories, Azure OpenAI model availability, and any policy denying
public ingress or resource creation. In the portal, review APIM, Container
Apps, Azure OpenAI, Cosmos DB, and AI Search quota/capacity for the selected
region. The documented event evidence is 20/20 Consumption APIM creates in
`eastus`, completing in about 3.5 minutes; this is empirical, not a
contractual quota guarantee.

## 4. Naming and provisioning expectations

Use a short, lowercase, globally unique APIM name with the assigned suffix:

```bash
APIM_NAME="acl-apim-${PARTICIPANT_ID}"   # example: acl-apim-p07
RG="rg-allclear-${PARTICIPANT_ID}"
LOC="eastus"
```

APIM names must be globally unique, 1–50 characters, and use only letters,
numbers, and hyphens. Keep the assigned suffix stable so the facilitator can
map the resource to a participant and clean it up.

Create with `--no-wait`, then poll. Expect approximately 2–5 minutes for
Consumption APIM; allow 10 minutes before treating it as a platform failure.
The full backend `azd up` path is materially longer: budget 15–30 minutes for
an already-registered subscription and 30–45 minutes when first-time
providers, Docker image pushes, OpenAI, Search, or Cosmos provisioning are
involved.

## 5. Shared-backend fallback

If a participant's `azd up` path is slow, quota-blocked, or unavailable, do
not spend the workshop window debugging provisioning. Give them the
facilitator's `SHARED_BACKEND_URL` and continue with Lab 08:

```bash
BACKEND_URL="$SHARED_BACKEND_URL"
curl --fail --max-time 10 "$BACKEND_URL/api/health"
```

The participant still creates and tests their own APIM gateway. The shared
backend is read-only for the lab; do not expose its credentials or allow
participants to delete its resource group. If APIM itself is unavailable,
pair the participant with a pre-created gateway or use the shared gateway for
the conceptual policy exercise.

The facilitator must keep the shared backend credentials and deployment
identity private. Participants receive only the HTTPS URL and the minimum
APIM permissions needed for their own gateway.

## 6. JWT and Application Insights readiness

Before the session, verify:

- [ ] OIDC discovery URL returns HTTP 200.
- [ ] The test token has the agreed issuer and audience.
- [ ] The issuer metadata URL is reachable from APIM and the signing keys
      endpoint is not blocked by tenant or network policy.
- [ ] A no-token request is expected to return 401 only after the JWT policy
      is applied; keep JWT optional until the baseline gateway call succeeds.
- [ ] The Application Insights component exists in the same subscription or
      has been granted the required access.
- [ ] The facilitator has permission to create an APIM logger and API
      diagnostic, and has the instrumentation key or connection string
      required by the chosen APIM logger configuration.
- [ ] APIM logger creation and API diagnostics are enabled for the rehearsal
      gateway, with sampling at 100% for the short event test.

## 7. 20-participant dress rehearsal

Use disposable resource groups and delete them after the run.

1. [ ] Assign `p01`–`p20` and verify no duplicate APIM names.
2. [ ] Confirm all participants can run `az account show`.
3. [ ] Confirm `Microsoft.ApiManagement` is registered.
4. [ ] Confirm the shared backend health endpoint returns 200.
5. [ ] Start 20 `az apim create --no-wait` operations in `eastus`.
6. [ ] Poll all 20 every 15 seconds.
7. [ ] Record submit failures, HTTP 429s, and terminal provisioning states.
8. [ ] Require all successful instances to reach `Succeeded` within 10 minutes.
9. [ ] Import the shared backend OpenAPI document into at least three gateways.
10. [ ] Call `/allclear/api/health` through each sampled gateway.
11. [ ] Send one non-sensitive test signal through each sampled gateway.
12. [ ] Confirm the response is not a direct-backend URL response.
13. [ ] Apply `rate-limit-by-key` to one gateway.
14. [ ] Confirm the policy returns 429 at its documented threshold.
15. [ ] Apply the JWT policy only after recording the valid test issuer/audience.
16. [ ] Confirm no-token traffic returns 401 and valid-token traffic succeeds.
17. [ ] Attach the Application Insights logger and API diagnostics.
18. [ ] Confirm requests, latency, and 401/429 response codes are queryable.
19. [ ] Capture names, URLs, timestamps, and failures in the event log.
20. [ ] Delete every rehearsal APIM instance and resource group, then verify
      deletion.

If any participant cannot create a resource group, staff must pre-create the
group and grant the participant only the required APIM scope before step 5.

## 8. Cleanup and event-day stop conditions

At the end of the stage, delete participant gateways and resource groups, and
verify that deletion completes:

```bash
az group delete --name "$RG" --yes --no-wait
az group exists --name "$RG"
```

Repeat `az group exists` until it returns `false`; `--no-wait` only starts the
deletion. Keep a written list of every participant RG and APIM name so no
orphaned global resource survives the event.

Keep the shared backend until the facilitator confirms all demos are complete,
then delete it and its resource group. Stop provisioning attempts when the
subscription returns repeated 429s, a provider is not registered, or any
deployment exceeds the stated 10-minute APIM / 45-minute full-stack budget;
switch to the shared-backend or pre-created-gateway fallback instead.
