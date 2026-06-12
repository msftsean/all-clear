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
    expect(screen.getByText(/1,240 signals/i)).toBeInTheDocument();
    expect(screen.getByText(/3 incidents/i)).toBeInTheDocument();
    expect(screen.getAllByTestId("hero-incident-card")).toHaveLength(3);
    expect(screen.getByText("Downtown high-rise fire")).toBeInTheDocument();
    expect(screen.getByText("812")).toBeInTheDocument();
  });

  it("renders the explicit blank demo state", () => {
    render(<Canvas result={null} onOpenReceipt={() => undefined} demoBlank />);

    expect(screen.getByTestId("canvas-empty")).toBeInTheDocument();
    expect(screen.getByText(/clean slate before the signal surge/i)).toBeInTheDocument();
  });
});
