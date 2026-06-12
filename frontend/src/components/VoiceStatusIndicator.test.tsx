import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { VoiceStatusIndicator } from "./VoiceStatusIndicator";
import { VoiceUIState } from "../types/voice";

describe("VoiceStatusIndicator", () => {
  it("shows escalation status while support-agent tool call is pending", () => {
    render(
      <VoiceStatusIndicator
        voiceState={VoiceUIState.Processing}
        pendingEscalation
      />,
    );

    expect(screen.getByRole("status")).toHaveTextContent(
      "Connecting you to a support agent…",
    );
  });
});
