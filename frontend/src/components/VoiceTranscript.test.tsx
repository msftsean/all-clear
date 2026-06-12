import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { VoiceTranscript } from "./VoiceTranscript";
import type { VoiceMessage } from "../types/voice";

const messages: VoiceMessage[] = [
  {
    id: "user-voice",
    role: "user",
    content: "I need help registering.",
    timestamp: new Date("2026-03-13T12:00:00Z"),
  },
  {
    id: "assistant-voice",
    role: "assistant",
    content: "I can help with registration.",
    timestamp: new Date("2026-03-13T12:00:01Z"),
  },
];

describe("VoiceTranscript", () => {
  it("renders distinct microphone and speaker badges for voice bubbles", () => {
    render(<VoiceTranscript messages={messages} />);

    expect(screen.getByLabelText("User voice message badge")).toHaveClass(
      "bg-white",
    );
    expect(screen.getByLabelText("Assistant voice message badge")).toHaveClass(
      "bg-blue-100",
    );
    expect(screen.getByText("I need help registering.")).toBeInTheDocument();
    expect(
      screen.getByText("I can help with registration."),
    ).toBeInTheDocument();
  });
});
