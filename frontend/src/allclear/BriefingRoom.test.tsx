import { act, fireEvent, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import BriefingRoom from "./BriefingRoom";
import { submitSignal } from "./api";
import type { PipelineResult } from "./types";

vi.mock("./api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("./api")>()),
  getHealth: vi.fn().mockResolvedValue({ status: "healthy", mock_mode: false, domain: "allclear" }),
  getModelStatus: vi.fn().mockResolvedValue({ active: "gpt-5.1", mock_mode: false }),
  getAzureFootprint: vi.fn().mockResolvedValue(null),
  submitSignal: vi.fn(),
}));

vi.mock("./useStudentIdentity", () => {
  const getHash = vi.fn().mockResolvedValue("test-student");
  return { useStudentIdentity: () => ({ getHash }) };
});

const attached: PipelineResult = {
  session_id: "test-session",
  channel: "chat",
  signal_text: "A sparking power line on Oak Street.",
  classification: {
    intent: "Report an electrical hazard",
    intent_category: "FIELD_HAZARD",
    target_queue: "field-operations",
    confidence: 0.99,
    entities: { location: "Oak Street", severity_indicators: ["sparking"] },
    requires_escalation: true,
    pii_detected: false,
    pii_types: [],
    sentiment: "concerned",
    urgency_indicators: [],
  },
  routing: {
    outcome: "ATTACH_TO_INCIDENT",
    target_queue: "field-operations",
    severity: "SEV1",
    sla_minutes: 15,
    escalate: true,
    escalation_reason: "sev1_incident",
    matched_incident_id: "AC-2001",
    dedup_similarity: 1,
    magnitude: 3,
    routing_rules_applied: ["dedup_match", "sev1_incident"],
  },
  action: {
    status: "attached",
    incident_id: "AC-2001",
    queue: "field-operations",
    severity: "SEV1",
    knowledge_articles: [],
    sitrep: null,
    citations: [{ source_id: "AC-2001", source_type: "incident", quote: "Electrical hazard" }],
    estimated_response_time: "15 minutes",
    escalated: true,
    user_message: "Your report was attached to the existing incident.",
  },
  processing_ms: 2000,
};

describe("BriefingRoom live decisions", () => {
  beforeEach(() => {
    window.history.replaceState({}, "", "/");
    HTMLElement.prototype.scrollTo = vi.fn();
    vi.mocked(submitSignal).mockReset();
    vi.mocked(submitSignal).mockResolvedValue(attached);
  });

  it("counts a first-session attachment, exposes its desktop receipt, and resets session counts", async () => {
    const user = userEvent.setup();
    await act(async () => {
      render(<BriefingRoom />);
    });

    async function click(testId: string) {
      await act(async () => {
        await user.click(screen.getByTestId(testId));
      });
    }

    async function send() {
      fireEvent.change(screen.getByTestId("signal-input"), {
        target: { value: attached.signal_text },
      });
      await click("send-signal");
      await screen.findByTestId("hero-clearboard");
    }

    await send();
    expect(screen.getByLabelText("1 Signals to 1 Incidents")).toBeInTheDocument();
    expect(within(screen.getByTestId("attached-signals")).getByText("1")).toBeInTheDocument();
    expect(screen.queryByText("Sitrep ready")).not.toBeInTheDocument();
    expect(screen.getByText("No sitrep returned")).toBeInTheDocument();

    await click("open-receipt");
    expect(screen.getByTestId("decision-receipt")).toHaveTextContent("ATTACH_TO_INCIDENT");
    expect(screen.getByTestId("decision-receipt")).toHaveTextContent("deterministic · no LLM");
    expect(screen.queryByTestId("approval-gate")).not.toBeInTheDocument();
    await click("receipt-close");

    await send();
    expect(within(screen.getByTestId("attached-signals")).getByText("2")).toBeInTheDocument();
    await click("clear-board");
    expect(screen.getByTestId("canvas-empty")).toBeInTheDocument();
    await send();
    expect(within(screen.getByTestId("attached-signals")).getByText("1")).toBeInTheDocument();
    expect(submitSignal).toHaveBeenCalledTimes(3);
  });
});
