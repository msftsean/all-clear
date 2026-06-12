/**
 * VoiceMicButton component tests.
 */
import { describe, it, expect, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { VoiceMicButton } from "./VoiceMicButton";
import { VoiceUIState } from "../types/voice";

describe("VoiceMicButton", () => {
  it("should have VoiceUIState available for prop typing", () => {
    expect(VoiceUIState.Idle).toBeDefined();
    expect(VoiceUIState.Listening).toBeDefined();
    expect(VoiceUIState.Processing).toBeDefined();
  });

  it("test_keyboard_activation toggles with Enter and Escape when active", () => {
    const onToggle = vi.fn();
    const { rerender } = render(
      <VoiceMicButton voiceState={VoiceUIState.Idle} onToggle={onToggle} />,
    );

    const idleButton = screen.getByRole("button", {
      name: "Start voice conversation",
    });
    idleButton.focus();
    fireEvent.keyDown(idleButton, { key: "Enter" });
    expect(onToggle).toHaveBeenCalledTimes(1);

    rerender(
      <VoiceMicButton
        voiceState={VoiceUIState.Listening}
        onToggle={onToggle}
      />,
    );
    const activeButton = screen.getByRole("button", {
      name: "End voice conversation",
    });
    activeButton.focus();
    fireEvent.keyDown(activeButton, { key: "Escape" });
    expect(onToggle).toHaveBeenCalledTimes(2);
  });

  it("test_aria_attributes exposes pressed state, labels, and button role", () => {
    const onToggle = vi.fn();
    const { rerender } = render(
      <VoiceMicButton voiceState={VoiceUIState.Idle} onToggle={onToggle} />,
    );

    const idleButton = screen.getByRole("button", {
      name: "Start voice conversation",
    });
    expect(idleButton).toHaveAttribute("aria-pressed", "false");

    rerender(
      <VoiceMicButton
        voiceState={VoiceUIState.Listening}
        onToggle={onToggle}
      />,
    );

    const activeButton = screen.getByRole("button", {
      name: "End voice conversation",
    });
    expect(activeButton).toHaveAttribute("aria-pressed", "true");
  });
});
