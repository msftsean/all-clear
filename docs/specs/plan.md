> ARCHIVED — superseded by All Clear (incident triage). See CONTEXT.md.

# Implementation Plan: Universal Front Door Support Agent

**Branch**: `1-front-door-agent` | **Date**: 2026-01-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/docs/specs/spec.md`

## Summary

Build a three-agent system (QueryAgent, RouterAgent, ActionAgent) that provides a unified student support entry point. The system uses LLM-based intent classification to detect 30+ intent categories, routes requests to appropriate departments (IT, HR, Registrar, Financial Aid, Facilities, Student Affairs, Campus Safety), creates tickets in ServiceNow, retrieves relevant knowledge base articles, and escalates policy-related or ambiguous queries to human reviewers. Target: increase first-contact resolution from 40% to 65%.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI (backend API), Azure OpenAI SDK (LLM), React 18+ with TypeScript (frontend), Tailwind CSS (styling)
**Storage**: Azure Cosmos DB (sessions, audit logs), Azure AI Search (knowledge base)
**Testing**: pytest (backend), pytest-asyncio (async tests), Playwright (E2E), Jest/React Testing Library (frontend)
**Target Platform**: Azure Container Apps (backend), Azure Static Web Apps (frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <30 second end-to-end response time, 500 concurrent users
**Constraints**: 99.9% uptime target, 90-day session retention, FERPA compliance
**Scale/Scope**: Mid-size university (15,000-30,000 students), 500 concurrent users peak

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Implementation Approach |
|-----------|--------|------------------------|
| I. Bounded Agent Authority | ✅ PASS | Three separate agent classes with distinct interfaces; no cross-boundary methods |
| II. Human Escalation | ✅ PASS | RouterAgent implements all 6 escalation triggers; escalation is explicit routing outcome |
| III. Privacy-First | ✅ PASS | Student ID hashed via SHA-256; PII detector runs before any logging; audit logs store only intents |
| IV. Stateful Context | ✅ PASS | Cosmos DB sessions with 90-day TTL; conversation history stored per session |
| V. Test-First | ✅ PASS | Acceptance scenarios converted to pytest fixtures; boundary tests for unauthorized access |
| VI. Accessibility | ✅ PASS | WCAG AA baseline, AAA for high-contrast; keyboard navigation; ARIA labels |
| VII. Graceful Degradation | ✅ PASS | Service abstractions with fallback implementations; circuit breakers on external calls |

**Security & Compliance**:
- HTTPS required for all connections
- API credentials in Azure Key Vault (not in code/logs)
- Rate limiting via Azure API Management
- Audit logs append-only with 7-year retention

## Project Structure

### Documentation (this feature)

```text
docs/specs/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
│   └── api.yaml
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── query_agent.py      # Intent detection & entity extraction
│   │   ├── router_agent.py     # Routing decisions & escalation logic
│   │   └── action_agent.py     # Ticket creation & KB retrieval
│   ├── models/
│   │   ├── __init__.py
│   │   ├── session.py          # Session entity
│   │   ├── audit_log.py        # AuditLog entity
│   │   ├── query_result.py     # QueryResult entity
│   │   ├── routing_decision.py # RoutingDecision entity
│   │   ├── action_result.py    # ActionResult entity
│   │   └── knowledge_article.py # KnowledgeArticle entity
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py      # Azure OpenAI abstraction
│   │   ├── ticket_service.py   # ServiceNow abstraction
│   │   ├── knowledge_service.py # Azure AI Search abstraction
│   │   ├── session_service.py  # Cosmos DB session management
│   │   ├── audit_service.py    # Audit logging
│   │   └── pii_detector.py     # PII detection service
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py         # POST /api/chat
│   │   │   ├── tickets.py      # GET /api/tickets/{id}
│   │   │   └── health.py       # GET /api/health
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py         # SSO validation
│   │       └── rate_limit.py   # Rate limiting
│   └── config/
│       ├── __init__.py
│       ├── settings.py         # Environment config
│       └── prompts/
│           └── intent_classification.txt  # Few-shot prompts
├── tests/
│   ├── conftest.py
│   ├── contract/
│   │   └── test_api_contracts.py
│   ├── integration/
│   │   ├── test_chat_flow.py
│   │   ├── test_escalation.py
│   │   └── test_ticket_creation.py
│   └── unit/
│       ├── test_query_agent.py
│       ├── test_router_agent.py
│       ├── test_action_agent.py
│       └── test_pii_detector.py
├── mock_data/
│   ├── sample_tickets.json
│   ├── sample_kb_articles.json
│   └── intent_examples.json
├── pyproject.toml
├── Dockerfile
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── TicketCard.tsx
│   │   ├── KnowledgeArticleCard.tsx
│   │   ├── TypingIndicator.tsx
│   │   ├── HumanEscalationButton.tsx
│   │   └── AccessibilityToggle.tsx
│   ├── pages/
│   │   └── ChatPage.tsx
│   ├── services/
│   │   └── api.ts              # Backend API client
│   ├── hooks/
│   │   ├── useChat.ts
│   │   └── useAccessibility.ts
│   ├── styles/
│   │   ├── globals.css
│   │   └── high-contrast.css
│   ├── App.tsx
│   └── main.tsx
├── tests/
│   ├── components/
│   │   └── ChatWindow.test.tsx
│   └── e2e/
│       └── chat.spec.ts        # Playwright E2E tests
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── Dockerfile
```

**Structure Decision**: Web application pattern selected due to separate frontend (React chat UI) and backend (Python agents + API). This enables independent scaling and deployment of each tier.

## Complexity Tracking

No Constitution Check violations requiring justification. The three-agent architecture is required by the spec's bounded authority principle, not added complexity.
