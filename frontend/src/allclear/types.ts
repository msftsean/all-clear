// Typed contract mirroring the backend PipelineResult (app/agents/schemas.py).
// Only the fields the briefing room renders are modelled; unknown extras are tolerated.

export type Severity = "SEV1" | "SEV2" | "SEV3" | "SEV4";
export type RoutingOutcome = "OPEN_INCIDENT" | "ATTACH_TO_INCIDENT" | string;

export interface Citation {
  source_id: string;
  source_type: string;
  quote: string;
}

export interface SignalEntities {
  location?: string | null;
  system?: string | null;
  severity_indicators?: string[];
  other?: string[];
}

export interface SignalClassification {
  intent: string;
  intent_category: string;
  target_queue: string;
  confidence: number;
  entities: SignalEntities;
  requires_escalation: boolean;
  escalation_reason?: string | null;
  pii_detected: boolean;
  pii_types: string[];
  sentiment: string;
  urgency_indicators: string[];
}

export interface RoutingDecision {
  outcome: RoutingOutcome;
  target_queue: string;
  severity: Severity;
  sla_minutes: number;
  escalate: boolean;
  escalation_reason?: string | null;
  matched_incident_id?: string | null;
  dedup_similarity?: number | null;
  magnitude: number;
  routing_rules_applied: string[];
}

export interface Sitrep {
  incident_id: string;
  summary: string;
  citations: Citation[];
}

export interface IncidentAction {
  status: string;
  incident_id: string;
  queue: string;
  severity: Severity;
  knowledge_articles: unknown[];
  sitrep?: Sitrep | null;
  citations: Citation[];
  estimated_response_time: string;
  escalated: boolean;
  user_message: string;
}

export interface PipelineResult {
  session_id: string;
  channel: string;
  signal_text: string;
  classification: SignalClassification;
  routing: RoutingDecision;
  action: IncidentAction;
  processing_ms: number;
}

export interface HealthStatus {
  status: string;
  mock_mode: boolean;
  domain: string;
}

export interface ModelStatus {
  active?: string | null;
  fallback_chain?: string[];
  last_served?: string | null;
  failover_active?: boolean;
  mock_mode?: boolean;
}

export interface DemoClearBoardIncident {
  incident_id: string;
  title: string;
  location: string;
  queue: string;
  severity: Severity;
  report_count: number;
  sla_minutes: number;
  dedup_similarity: number;
  status: string;
  summary: string;
  sample_signals: string[];
}

export interface DemoClearBoard {
  mode: "blank" | "loaded";
  total_signals: number;
  incidents: DemoClearBoardIncident[];
  headline: string;
  subhead: string;
}
