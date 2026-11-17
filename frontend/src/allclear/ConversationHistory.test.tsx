import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import ConversationHistory from "./ConversationHistory";

describe("ConversationHistory", () => {
  it("does not offer caller-hash-based history before ownership auth exists", () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    render(<ConversationHistory studentIdHash={"a".repeat(64)} />);

    expect(
      screen.getByText(/unavailable until authenticated ownership is configured/i),
    ).toBeInTheDocument();
    expect(fetchSpy).not.toHaveBeenCalled();
    fetchSpy.mockRestore();
  });
});
