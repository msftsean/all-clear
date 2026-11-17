# 🛡️ All Clear red-team presenter guide

**Revision:** 04 · 2026-10-01 | **Status:** 🟢 `[██████]` Published and verified on the existing Azure Static Web App

**Open the guide:** https://brave-forest-0ad7d0f0f.2.azurestaticapps.net/
**Open the on-stage script:** https://brave-forest-0ad7d0f0f.2.azurestaticapps.net/script.html

This standalone, public Azure Static Web Apps guide is a **presentation and learning aid**, not the All Clear application or a live dashboard. It adapts the supplied slide deck's white/silver canvas, blue trusted-information boundary and red untrusted-input warnings into responsive CSS without embedding slide imagery. Open `site/index.html` to preview; no build or package install is required.

## 🎤 What to show

The **Demo script** tab follows all 19 speaker-note sections of the available `Red_Teaming_Your_AI.pptx` with read-aloud passages and conditional fallbacks. The guide maps each slide range to Sean's screen, action, evidence and missing-result line. Charles owns a separate demo and talk track; no joint clock or handoff is assumed. Slide 19 is the shared final close. **Attachment gap:** the separately named `Red_Teaming_Your_AI_—_Adversarial_Testing_for_Deployments.pptx` was not present at the expected path; the similarly titled `Red Teaming Your AI — Adversarial Testing for Deployments.pptx` in Downloads has only 18 slides and different notes. Confirm the intended 19-slide file before publication.

The completed **native Foundry red-team run** `redteam-run-ckeumngo` has a reviewed 107-record export: 95 evaluator passes and 12 evaluator-reported successful attacks (11.21% aggregate reported ASR). These are review flags, **not 12 confirmed vulnerabilities**. Exported prompts are redacted, all numeric score fields are 0.0, and complete target/configuration and full application coverage are not established. The planned fresh CLI run is separate; its tested launch/status commands remain an unresolved **private operator prerequisite**.

The two deliberately seeded application regressions (unauthorized retrieval and poisoned sitrep) belong to the **private synthetic adapter**; its independent suite passed 6/6 remotely and the deployed HTTP path was probed separately. The **separate, tool-free Foundry prompt agent** returned 2/2 reported passed in a supplementary batch evaluation. Neither figure substitutes for the native run or proves a full All Clear pipeline baseline.

Never show the historical vulnerable revision as current. The adapter was last verified healthy, internal-only and in safe mode; check it again before the demo. The public site cannot reach it. Use the separate private `DEMO_RUNBOOK.md` for operator-only probe instructions and `DEMO_RESULTS.md` for exact revision, image digest, timestamps and scope. No literal canaries, deployment tokens or live records belong in this site.

## ☁️ Deployment

The target is the **Free-tier** `allclear-redteam-runbook-20261001` SWA in `rg-allclear-redteam-20261001`, East US 2, subscription `MCAPS-2026-segayle`. It has no GitHub workflow or API. Only the `site/` directory was published with the SWA CLI; this README and `.azure/` plan remain unpublished (both return 404). The deployment token was held in process memory only, never printed or saved. On 2026-10-01, independent HTTPS fetches confirmed both public pages and the stylesheet match their local revision 04 assets byte-for-byte. The source-deck filename discrepancy and private operator prerequisites remain documented above and in `.azure/deployment-plan.md`.

**Maintenance:** Edit `site/index.html`, `site/script.html` and `site/styles.css`, validate factual claims against the source results, and redeploy only `site/`. Public access is intentional. To restrict this site to a tenant, design and verify tenant-scoped authorization first; the built-in `authenticated` role alone does **not** limit sign-in to this tenant.
