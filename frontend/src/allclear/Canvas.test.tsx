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

  it("renders a real-session ClearBoard from submitted signal results", () => {
    render(
      <Canvas
        result={null}
        onOpenReceipt={() => undefined}
        clearBoard={{
          mode: "loaded",
          total_signals: 2,
          headline: "Live ClearBoard",
          subhead: "Live Signals are preserved as Reports.",
          incidents: [
            {
              incident_id: "AC-2001",
              title: "FIELD HAZARD · Oak St",
              location: "Oak St",
              queue: "Utilities",
              severity: "SEV2",
              report_count: 2,
              sla_minutes: 15,
              dedup_similarity: 0.94,
              status: "attached",
              summary: "Two real Signals attached to one Incident.",
              sample_signals: ["line down", "same line sparking"],
            },
          ],
        }}
      />,
    );

    expect(screen.getByText(/2 SIGNALS/i)).toBeInTheDocument();
    expect(screen.getByText(/1 INCIDENTS/i)).toBeInTheDocument();
    expect(screen.getByText(/Oak St · Magnitude 2/i)).toBeInTheDocument();
  });
});
