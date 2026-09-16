import CollapsibleNotes from '../components/CollapsibleNotes'
import { MagnifyingGlassIcon, ShieldCheckIcon, UserGroupIcon } from '@heroicons/react/24/outline'

export default function ResponsibleAI() {
  return (
    <div role="tabpanel" id="responsible-ai-panel" aria-labelledby="responsible-ai-tab">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-3xl font-semibold tracking-tight text-dark-text mb-4">
          Responsible AI in Practice
        </h2>
        <p className="text-xl text-ink/70 mb-12">
          Concrete governance, not abstract principles
        </p>

        <div className="bg-brand/5 border border-brand/20 p-6 rounded-xl shadow-sm mb-12">
          <p className="text-xl font-medium text-dark-text">
            Responsible AI Is a Build Decision, Not a Review Step
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="card">
            <div className="flex items-center gap-3 mb-4">
              <MagnifyingGlassIcon className="w-8 h-8 text-brand" />
              <h3 className="font-semibold text-xl text-dark-text">Transparency</h3>
            </div>
            <p className="text-ink/75 mb-3">
              The workshop path exposes inspectable traces for routing and escalation decisions. Demo
              transcripts are admin-scoped and PII-redacted before display.
            </p>
            <ul className="text-sm text-ink/70 space-y-1">
              <li>• Session traces for local/mock interactions</li>
              <li>• Input modality logged (text/voice)</li>
              <li>• PII-filtered transcript display</li>
              <li>• Live mode must configure durable audit storage</li>
            </ul>
          </div>

          <div className="card">
            <div className="flex items-center gap-3 mb-4">
              <ShieldCheckIcon className="w-8 h-8 text-brand" />
              <h3 className="font-semibold text-xl text-dark-text">Safety</h3>
            </div>
            <p className="text-ink/75 mb-3">
              Bounded tools, escalation triggers, and PII filtering enforce safety at the architecture level, 
              not just policy.
            </p>
            <ul className="text-sm text-ink/70 space-y-1">
              <li>• Exactly 4 tools (no more, no less)</li>
              <li>• Automatic escalation keywords</li>
              <li>• PII redaction before logging</li>
              <li>• No raw audio storage</li>
            </ul>
          </div>

          <div className="card">
            <div className="flex items-center gap-3 mb-4">
              <UserGroupIcon className="w-8 h-8 text-brand" />
              <h3 className="font-semibold text-xl text-dark-text">Equity</h3>
            </div>
            <p className="text-ink/75 mb-3">
              Voice AND text, keyboard navigation, screen reader support. Accessibility is not optional — 
              it's architectural.
            </p>
            <ul className="text-sm text-ink/70 space-y-1">
              <li>• Voice is additive, not replacement</li>
              <li>• Keyboard-only operation</li>
              <li>• ARIA labels for screen readers</li>
              <li>• Transcripts always visible</li>
            </ul>
          </div>
        </div>

        <div className="card mb-8">
          <h3 className="font-semibold text-lg mb-4 text-dark-text">Audit Trail Visualization</h3>
          <p className="text-sm text-ink/70 mb-4">
            What a production log entry should look like. The local workshop uses in-memory mock stores;
            live mode fails closed unless durable audit storage is configured:
          </p>
          <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-xs font-mono">
{`{
  "session_id": "abc-123",
  "timestamp": "2026-03-19T14:00:00Z",
  "input_modality": "voice",
  "user_input": "[PII filtered] password reset request",
  "intent": "it_support",
  "confidence": 0.95,
  "department": "IT Support",
  "priority": "high",
  "action": "create_ticket",
  "ticket_id": "IT-2024-0847",
  "kb_articles": ["KB-1234: Password Reset Guide"],
  "pii_filtered": true,
  "tool_calls": [
    {
      "tool": "analyze_and_route_query",
      "duration_ms": 234
    },
    {
      "tool": "create_ticket",
      "duration_ms": 189
    },
    {
      "tool": "search_knowledge_base",
      "duration_ms": 145
    }
  ]
}`}
          </pre>
        </div>

        <div className="card mb-8">
          <h3 className="font-semibold text-lg mb-4 text-dark-text">Health Check Dashboard</h3>
          <p className="text-sm text-ink/70 mb-4">
            What administrators should verify before a live demo — mock mode is intentionally explicit:
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
              <div className="text-2xl mb-1">✅</div>
              <div className="text-xs font-semibold text-ink">LLM Service</div>
              <div className="text-xs text-green-600">Operational</div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
              <div className="text-2xl mb-1">✅</div>
              <div className="text-xs font-semibold text-ink">Ticketing</div>
              <div className="text-xs text-green-600">Operational</div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
              <div className="text-2xl mb-1">✅</div>
              <div className="text-xs font-semibold text-ink">Knowledge Base</div>
              <div className="text-xs text-green-600">Operational</div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
              <div className="text-2xl mb-1">✅</div>
              <div className="text-xs font-semibold text-ink">Session Store</div>
              <div className="text-xs text-green-600">Mock or Cosmos</div>
            </div>
          </div>
          <div className="mt-4 p-3 bg-brand/5 rounded border border-blue-200">
            <div className="text-sm font-semibold mb-1 text-dark-text">
              Voice Availability: <span className="text-brand">GET /api/realtime/availability</span>
            </div>
            <div className="text-xs text-ink/70">
              Returns availability only when a realtime deployment is configured; frontend hides the
              mic button in mock/offline mode.
            </div>
          </div>
        </div>

        <div className="card mb-8 border-iu-crimson/30 bg-iu-crimson/5">
          <h3 className="font-semibold text-lg mb-4 text-dark-text">Graceful Degradation Demo</h3>
          <div className="space-y-3">
            <div className="flex items-center gap-4 p-3 bg-surface-muted rounded">
              <div className="text-2xl">🎤</div>
              <div className="flex-1">
                <div className="font-medium text-sm text-ink">Voice Enabled</div>
                <div className="text-xs text-ink/70">Mic button visible, WebRTC active</div>
              </div>
              <div className="text-green-600 font-bold">ON</div>
            </div>
            <div className="text-center text-ink/40">↓ Voice service unavailable</div>
            <div className="flex items-center gap-4 p-3 bg-surface-muted rounded">
              <div className="text-2xl">💬</div>
              <div className="flex-1">
                <div className="font-medium text-sm text-ink">Voice Disabled → Text Works</div>
                <div className="text-xs text-ink/70">Mic button hidden, chat interface fully functional</div>
              </div>
              <div className="text-brand font-bold">DEGRADED</div>
            </div>
          </div>
          <p className="text-sm text-ink/80 mt-4 bg-brand/5 p-3 rounded-lg border border-border">
            <strong>Constitutional Principle VI:</strong> Accessibility is additive. When voice is OFF, 
            the mic button disappears, but text chat works perfectly. No feature loss for core functionality.
          </p>
        </div>

        <CollapsibleNotes>
          <p className="mb-3">
            <strong>University IT teams ask:</strong> "How do we know what the AI is doing?"
          </p>
          <p className="mb-3">
            The answer is <strong>architectural transparency</strong>: keep the workshop traceable, and
            require durable audit logging before a live consequential-use deployment. Routing and
            escalation records should include:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>The modality (voice or text)</li>
            <li>The session ID (for tracing conversations)</li>
            <li>PII-filtered content (no raw audio, no SSNs, no known sensitive identifiers)</li>
            <li>Tool execution time and results</li>
            <li>Department routing and priority assignment</li>
          </ul>
          <p className="mb-3">
            This is not a production attestation by itself. With durable audit storage enabled,
            administrators should be able to:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Audit scoped sessions by ID</li>
            <li>Search logs for specific tool calls or departments</li>
            <li>Track escalation patterns and response times</li>
            <li>Monitor PII filtering effectiveness</li>
            <li>Check service health in real-time</li>
          </ul>
          <p>
            This is what makes Responsible AI <strong>operational</strong>, not aspirational. It's built 
            into the architecture, logged at every step, and verified before deployment.
          </p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
