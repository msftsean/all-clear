import { render, screen } from "@testing-library/react";
import { afterEach, vi } from "vitest";
import LiveCalls from "./LiveCalls";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("LiveCalls", () => {
  it("does not open an unauthenticated transcript stream", () => {
    const eventSource = vi.fn();
    vi.stubGlobal("EventSource", eventSource);

    render(<LiveCalls onExit={() => undefined} />);

    expect(
      screen.getByText(/unavailable until authenticated call ownership is configured/i),
    ).toBeInTheDocument();
    expect(eventSource).not.toHaveBeenCalled();
  });
});
