import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import { EMPTY_STATE, SurgeBoardView, prettyCategory } from "./SurgeBoard";
import { resultDetail, resultHeadline } from "./SurgeReport";
import { SURGE_CARDS, findCard, reportUrl } from "./cards";
import type { SurgeState } from "./surgeApi";

vi.mock("qrcode", () => ({
  default: { toDataURL: () => Promise.resolve("data:image/png;base64,AAAA") },
}));

const LIVE: SurgeState = {
  ...EMPTY_STATE,
  open: true,
  signals: 43,
  incidents: 4,
  ratio: 10.8,
  devices: 31,
  blocked: 2,
  escalated_to_person: 1,
  tiles: [
    {
      incident_id: "AC-0001",
      severity: "SEV2",
      queue: "field-operations",
      category: "INFRASTRUCTURE_OUTAGE",
      location: "Wilson Blvd",
      escalated: false,
      room_reports: 18,
      magnitude: 18,
    },
    {
      incident_id: "AC-0002",
      severity: "SEV1",
      queue: "escalations",
      category: "PUBLIC_SAFETY",
      location: "Courthouse Plaza",
      escalated: true,
      room_reports: 9,
      magnitude: 9,
    },
  ],
};

describe("Room surge board", () => {
  it("shows counters, ratio and one tile per incident", () => {
    render(<SurgeBoardView state={LIVE} joinUrl="https://allclear.example/report" stale={false} />);
    expect(screen.getByTestId("surge-signals")).toHaveTextContent("43");
    expect(screen.getByTestId("surge-incidents")).toHaveTextContent("4");
    expect(screen.getByTestId("surge-ratio")).toHaveTextContent("10.8× collapse");
    expect(screen.getByTestId("surge-blocked")).toHaveTextContent("2");
    expect(screen.getByTestId("surge-escalated")).toHaveTextContent("1");
    expect(screen.getAllByTestId("surge-tile")).toHaveLength(2);
    expect(screen.getByText("Infrastructure Outage")).toBeInTheDocument();
    expect(screen.getByText("Escalated to a person")).toBeInTheDocument();
    expect(screen.getByTestId("surge-status")).toHaveTextContent("OPEN");
  });

  it("shows the quiet state before the surge", () => {
    render(<SurgeBoardView state={EMPTY_STATE} joinUrl="https://allclear.example/report" stale />);
    expect(screen.getByText(/The board is quiet/)).toBeInTheDocument();
    expect(screen.getByText("reconnecting…")).toBeInTheDocument();
    expect(screen.getByTestId("surge-status")).toHaveTextContent("CLOSED");
    expect(screen.queryAllByTestId("surge-tile")).toHaveLength(0);
  });
});

describe("Room surge helpers", () => {
  it("formats categories", () => {
    expect(prettyCategory("FIELD_HAZARD")).toBe("Field Hazard");
  });

  it("finds cards and builds report URLs", () => {
    expect(SURGE_CARDS.map((c) => c.id)).toEqual(["A", "B", "C", "D", "E", "R"]);
    expect(findCard("b")?.title).toBe("Signals are dark");
    expect(findCard("z")).toBeNull();
    expect(reportUrl("https://h", "A")).toBe("https://h/report?card=A");
  });

  it("phrases reporter acknowledgments", () => {
    const joined = { accepted: true, outcome: "joined" as const, incident_id: "AC-0003", room_reports: 12, message: "" };
    expect(resultHeadline(joined)).toBe("Your report joined AC-0003");
    expect(resultDetail(joined)).toMatch(/12 people in this room/);
    const blocked = { accepted: false, outcome: "blocked" as const, message: "Blocked by the safety filter." };
    expect(resultHeadline(blocked)).toBe("Blocked by the safety filter");
  });
});
