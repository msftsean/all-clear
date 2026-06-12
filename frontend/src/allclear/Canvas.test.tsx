import { render, screen } from "@testing-library/react";
import { Canvas } from "./Canvas";
import { HERO_DEMO_BOARD } from "./demo";

describe("Canvas demo board", () => {
  it("renders the hero deduplication ratio and incident report counts", () => {
    render(
      <Canvas
        result={null}
        onOpenReceipt={() => undefined}
        demoBoard={HERO_DEMO_BOARD}
      />,
    );

    expect(screen.getByTestId("hero-clearboard")).toBeInTheDocument();
    expect(screen.getAllByText(/1,240 SIGNALS/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/3 INCIDENTS/i).length).toBeGreaterThan(0);
    expect(screen.getAllByTestId("hero-incident-card")).toHaveLength(3);
    expect(screen.getByText("Downtown high-rise fire")).toBeInTheDocument();
    expect(screen.getAllByText(/Magnitude · Reports/i)).toHaveLength(3);
  });

  it("streams a partial surge through the same ClearBoard rendering path", () => {
    render(
      <Canvas
        result={null}
        onOpenReceipt={() => undefined}
        demoBoard={HERO_DEMO_BOARD}
        demoSignalsReceived={120}
      />,
    );

    expect(screen.getAllByText(/120 SIGNALS/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/INCIDENTS/i).length).toBeGreaterThan(0);
    expect(screen.getByTestId("hero-map-card")).toHaveTextContent(/pins merge on dedup/i);
  });

  it("renders the explicit blank demo state", () => {
    render(<Canvas result={null} onOpenReceipt={() => undefined} demoBlank />);

    expect(screen.getByTestId("canvas-empty")).toBeInTheDocument();
    expect(screen.getByText(/clean slate before the signal surge/i)).toBeInTheDocument();
  });
});
