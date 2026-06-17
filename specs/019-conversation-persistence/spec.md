# Feature Specification: Conversation Persistence & History

**Feature Branch**: `019-conversation-persistence`  
**Created**: 2026-06-17  
**Status**: Draft  
**Input**: User description: "Add conversation persistence so students can resume conversations across sessions, view history, and retrieve past ticket IDs. Admins get a dashboard showing session metrics."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Resume a Conversation (Priority: P1)

A student starts a support conversation, closes their browser, and returns later to pick up where they left off. The system remembers what was discussed, what tickets were created, and what answers were given — no need to repeat context.

**Why this priority**: This is the core value proposition. Without persistence, every session is ephemeral. This single story makes the system feel like a real support channel rather than a one-off chatbot.

**Independent Test**: Can be fully tested by starting a conversation, closing the browser, reopening the app, and verifying the prior messages and ticket IDs are visible — delivering a complete "returning student" experience.

**Acceptance Scenarios**:

1. **Given** a student had a conversation yesterday about financial aid, **When** they open the app today, **Then** they can see a "My Conversations" list and click to reopen that conversation with all prior messages intact.
2. **Given** a ticket was created during a past conversation, **When** the student resumes that conversation, **Then** the ticket ID is visible and they can ask follow-up questions in the same thread.
3. **Given** a student has never had a conversation, **When** they open the app, **Then** they see an empty history state with a prompt to start a new conversation.

---

### User Story 2 - View Conversation History (Priority: P2)

A student can see a list of all their past support conversations, with summary information (date, topic, ticket IDs) so they can quickly find the one they need without opening each one.

**Why this priority**: History browsing reduces repeat contacts — students can self-serve by finding their own prior answers rather than re-asking.

**Independent Test**: Can be tested independently by verifying the history list page shows conversations in reverse chronological order with date, detected topic, and ticket IDs.

**Acceptance Scenarios**:

1. **Given** a student has three past conversations, **When** they view their history, **Then** they see all three listed with date, topic summary, and any ticket IDs created.
2. **Given** a student searches or filters their history, **When** they type a keyword, **Then** only conversations containing that keyword are shown.
3. **Given** a conversation had no ticket created, **When** displayed in the list, **Then** it shows "No ticket" rather than an error.

---

### User Story 3 - Admin Session Dashboard (Priority: P3)

An admin or coach can view a dashboard showing active sessions, total conversations by department, average session duration, and escalation rate — giving operational visibility into how the system is being used.

**Why this priority**: Operational insight supports continuous improvement and demonstrates accountability for the "responsible AI" narrative in the workshop runbook. Lower priority because the system functions without it.

**Independent Test**: Can be tested independently by logging in as an admin and verifying the dashboard shows accurate counts from the persistent store, without any student-facing changes needed.

**Acceptance Scenarios**:

1. **Given** 10 conversations happened today, **When** an admin views the dashboard, **Then** they see counts broken down by department (Financial Aid, Registration, Housing, IT, Policy).
2. **Given** a session had an escalation, **When** viewing the dashboard, **Then** the escalation is counted separately from resolved sessions.
3. **Given** the admin selects a date range, **When** they apply the filter, **Then** the metrics update to reflect only conversations in that range.

---

### Edge Cases

- What happens when the persistent store is unavailable? The system falls back to in-memory mode and displays a notice to the student that history may not be saved.
- What happens if a student's history grows very large (hundreds of conversations)? The list is paginated (20 per page) and oldest conversations are archived after 90 days.
- What happens when two browser tabs are open for the same session? The most recent message from either tab is preserved; no messages are lost.
- What happens if a conversation was started in mock/offline mode? Those sessions are not persisted (mock mode is development-only); a notice tells the user history is not saved in offline mode.
- What happens if a student clears their browser data? Session identity is re-established on next visit; prior conversations remain accessible via their persistent identity.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST persist every conversation message (student and agent) with a timestamp so the full transcript is retrievable after the browser session ends.
- **FR-002**: The system MUST associate each conversation with a stable student identity that persists across browser sessions on the same device/browser.
- **FR-003**: Students MUST be able to view a list of their past conversations, including date, topic summary, and any ticket IDs created during each conversation.
- **FR-004**: Students MUST be able to reopen any past conversation and continue it, with all prior messages visible in order.
- **FR-005**: The system MUST surface ticket IDs created in past conversations within the conversation thread so students can reference them.
- **FR-006**: The persistent store MUST be used when available; the system MUST fall back to in-memory operation (with a user-visible notice) if the store is unreachable.
- **FR-007**: Conversations MUST be retained for 90 days and then automatically archived or deleted per a configurable retention policy.
- **FR-008**: The system MUST NOT store raw audio; only text transcripts (including voice-to-text transcripts) are persisted.
- **FR-009**: Admins MUST be able to view a dashboard showing: total conversations, conversations by department, average session duration, and escalation count — filterable by date range.
- **FR-010**: The system MUST operate identically in mock/development mode using an in-memory store (no persistent store required for local development).

### Key Entities

- **Conversation**: A sequence of messages between a student and the AI agent, identified by a unique ID, with a start timestamp, detected topic/department, status (active/closed), and list of ticket IDs created.
- **Message**: A single turn in a conversation — author (student or agent), content (text), timestamp, and message type (text, voice transcript, system).
- **Student Identity**: A stable, anonymous identifier tied to a browser/device, used to associate conversations with a returning user without requiring login.
- **Session Metrics**: Aggregate counts and durations derived from conversations, used only for the admin dashboard — not stored per student.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A returning student can locate and reopen a past conversation in under 30 seconds without any support assistance.
- **SC-002**: 100% of messages sent during a conversation are retrievable after a browser close and reopen, with no message loss.
- **SC-003**: The conversation history list loads in under 2 seconds for a student with up to 50 past conversations.
- **SC-004**: The admin dashboard refreshes in under 3 seconds and reflects conversations from the past 90 days.
- **SC-005**: Zero conversations are lost when the persistent store experiences a temporary outage (in-memory fallback activates automatically).
- **SC-006**: The feature introduces no regression: all 313 existing backend tests continue to pass after implementation.

## Assumptions

- Student identity is anonymous (no login required). A device/browser-scoped token is sufficient for the demo/EDU context.
- The existing `session_id` UUID (already in use across text, voice, and phone) is the join key for all message types — no new session model is needed.
- Voice transcripts are already text by the time they reach the backend; persistence treats them identically to text messages.
- A 90-day retention window is appropriate for the EDU support use case.
- Admin dashboard is accessible only to authenticated admins (reuses existing Azure AD / SWA auth from the workshop site).
- Mock/offline mode (`MOCK_MODE=true`) continues to use in-memory storage only — no persistent store is initialized in mock mode.

## Dependencies

- `specs/001-maf-rehost` — the All Clear backend and `session_id` model are prerequisites (already complete).
- `specs/002-voice-interaction` — voice transcripts flow through the same session pipeline and must be persisted alongside text messages.
