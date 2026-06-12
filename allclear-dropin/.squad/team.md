# Squad Team

> All Clear, cross-vertical incident triage for ISVs. Every signal, until all clear.

## Coordinator

| Name | Role | Notes |
|------|------|-------|
| Squad | Coordinator | Routes work, enforces handoffs and reviewer gates. Does not generate domain artifacts. |

## Members

| Name | Role | Charter | Status |
|------|------|---------|--------|
| T'Challa | Lead | `.squad/agents/tchalla/charter.md` | ✅ Active |
| Shuri | Backend Dev | `.squad/agents/shuri/charter.md` | ✅ Active |
| Stark | Frontend Dev | `.squad/agents/stark/charter.md` | ✅ Active |
| Rogers | Security | `.squad/agents/rogers/charter.md` | ✅ Active |
| Barton | Tester | `.squad/agents/barton/charter.md` | ✅ Active |
| FRIDAY | Session Logger | `.squad/agents/friday/charter.md` | 📋 Silent |
| Ralph | Work Monitor | (built-in) | 🔄 Monitor |

## Project Context

- **Owner:** msftsean
- **Repo:** github.com/EstablishedCorp/all-clear
- **Stack:** Python 3.11+ / FastAPI, Microsoft Agent Framework 1.8.1, TypeScript 5 / React 18 + Vite, Azure OpenAI (gpt-5.1 family), Azure AI Search, Pydantic v2, Azure Container Apps
- **Description:** Three-agent MAF pipeline (QueryAgent → RouterExecutor → ActionAgent) for surge incident triage with embedding dedup, voice via WebRTC/ACS, and the ClearBoard live view. Refactored from 47 Doors.
- **Created:** 2026-06-12
- **Ground rules:** specs/001-maf-rehost/plan.md Loop Protocol governs all build work. CONTEXT.md defines domain vocabulary. shared/constitution.md is non-negotiable.
