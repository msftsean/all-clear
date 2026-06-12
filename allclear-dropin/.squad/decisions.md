# Decisions Log

| Date | Decision | Rationale | Owner |
|------|----------|-----------|-------|
| 2026-06-11 | Product renamed All Clear (was 47 Doors / Watchfloor candidate) | Goal-state name, cross-vertical, built-in demo ending. Code slug is `allclear` (one word) in packages/env vars; repo is `all-clear` | Sean |
| 2026-06-11 | Pin agent-framework==1.8.1 + agent-framework-openai==1.8.1; orchestrations package banned (rc) | Verified GA line via live package introspection; see specs/001-maf-rehost/plan.md Appendix A/B | Sean |
| 2026-06-11 | RouterExecutor stays deterministic, zero LLM calls | Production-proven pattern from 47 Doors; teaching point for ISV lab; enforced by test | Sean |
| 2026-06-11 | Loop Protocol adopted for all build work | Verifiers first, maker never grades own work, 3-strikes stop condition | Sean |
| 2026-06-12 | Squad recast: MCU Avengers (T'Challa lead) | New project, new universe, per casting policy | Sean |
