import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { ChatContainer } from "./ChatContainer";
import { useVoice } from "../hooks/useVoice";
import { VoiceUIState } from "../types/voice";

vi.mock("../hooks/useVoice", () => ({
  useVoice: vi.fn(),
}));

const mockUseVoice = vi.mocked(useVoice);

function setVoiceState(voiceState: VoiceUIState, available = true) {
  mockUseVoice.mockReturnValue({
    voiceState,
    transcript: [],
    pendingEscalation: false,
    error: null,
    startVoice: vi.fn(),
    stopVoice: vi.fn(),
    isVoiceSupported: true,
    available,
  });
}

describe("ChatContainer", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    Element.prototype.scrollIntoView = vi.fn();
  });

  it("returns focus to the text input when voice mode ends", () => {
    setVoiceState(VoiceUIState.Listening);
    const { rerender } = render(
      <ChatContainer
        messages={[]}
        isLoading={false}
        sessionId="session-123"
        onSendMessage={vi.fn()}
      />,
    );

    screen.getByRole("button", { name: "End voice conversation" }).focus();
    expect(
      screen.getByRole("button", { name: "End voice conversation" }),
    ).toHaveFocus();

    setVoiceState(VoiceUIState.Idle);
    rerender(
      <ChatContainer
        messages={[]}
        isLoading={false}
        sessionId="session-123"
        onSendMessage={vi.fn()}
      />,
    );

    expect(
      screen.getByRole("textbox", { name: "Message input" }),
    ).toHaveFocus();
  });

  it("keeps chat log in a polite additions live region", () => {
    setVoiceState(VoiceUIState.Idle);
    render(
      <ChatContainer
        messages={[]}
        isLoading={false}
        sessionId="session-123"
        onSendMessage={vi.fn()}
      />,
    );

    const chatLog = screen.getByRole("log", { name: "Chat messages" });
    expect(chatLog).toHaveAttribute("aria-live", "polite");
    expect(chatLog).toHaveAttribute("aria-relevant", "additions");
  });

  it("hides mic when voice unavailable", () => {
    setVoiceState(VoiceUIState.Idle, false);
    render(
      <ChatContainer
        messages={[]}
        isLoading={false}
        sessionId="session-123"
        onSendMessage={vi.fn()}
      />,
    );

    const micButton = screen.getByRole("button", { name: "Voice unavailable" });
    expect(micButton).toBeDisabled();
    expect(
      screen.queryByRole("button", { name: "Start voice conversation" }),
    ).not.toBeInTheDocument();
  });
});
