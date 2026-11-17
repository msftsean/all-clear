import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import QRCode from "qrcode";
import SurgeBoard, { EMPTY_STATE, SurgeBoardView, prettyCategory } from "./SurgeBoard";
import SurgeReport, { resultDetail, resultHeadline } from "./SurgeReport";
import SurgeCards from "./SurgeCards";
import { SURGE_CARDS, findCard, reportUrl } from "./cards";
import { submitSurgeReport } from "./surgeApi";
import type { SurgeState } from "./surgeApi";

vi.mock("qrcode", () => ({
  default: { toDataURL: vi.fn(() => Promise.resolve("data:image/png;base64,AAAA")) },
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
  it("uses a masked operator key only for control requests", async () => {
    sessionStorage.clear();
    window.history.replaceState(null, "", "/surge");
    const fetchMock = vi.fn().mockImplementation((url, init) =>
      Promise.resolve({
        ok: true,
        json: async () => url.endsWith("/health")
          ? { mock_mode: false }
          : init?.method === "POST" && JSON.parse(init.body).message
          ? { accepted: true, outcome: "opened", incident_id: "AC-1", message: "" }
          : EMPTY_STATE,
      }),
    );
    vi.stubGlobal("fetch", fetchMock);
    try {
      render(<SurgeBoard />);
      await waitFor(() => expect(fetchMock).toHaveBeenCalled());
      expect(screen.queryByRole("button", { name: "Open" })).not.toBeInTheDocument();
      fireEvent.click(screen.getByText("Operator controls"));
      const input = screen.getByLabelText("Coach key");
      expect(input).toHaveAttribute("type", "password");
      fireEvent.change(input, { target: { value: "private-key" } });
      fireEvent.click(screen.getByRole("button", { name: "Set key" }));
      expect(input).toHaveValue("");
      fireEvent.click(screen.getByRole("button", { name: "Open" }));
      await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => url.endsWith("/control"))).toBe(true));
      await submitSurgeReport("test report", "test-device", "A");
      const calls = fetchMock.mock.calls;
      const control = calls.find(([url]) => url.endsWith("/control"))!;
      expect(control[1].headers["X-Surge-Key"]).toBe("private-key");
      for (const [url, init] of calls.filter(([url]) => !url.endsWith("/control"))) {
        expect(url).not.toContain("private-key");
        expect(JSON.stringify(init ?? {})).not.toContain("private-key");
      }
      expect(screen.getByText(/\/report$/).textContent).not.toContain("private-key");
      expect(QRCode.toDataURL).toHaveBeenCalledWith(
        expect.not.stringContaining("private-key"), expect.any(Object),
      );
      expect(window.location.href).not.toContain("private-key");
    } finally {
      vi.unstubAllGlobals();
      sessionStorage.clear();
    }
  });

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

describe("Surge processing-mode disclosure", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("checks the same configured API origin used for report submission", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "https://api.example.test");
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ mock_mode: true }),
    });
    vi.stubGlobal("fetch", fetchMock);
    try {
      render(<SurgeReport />);
      expect(await screen.findByText(/MOCK REHEARSAL/)).toBeInTheDocument();
      expect(fetchMock).toHaveBeenCalledWith(
        "https://api.example.test/api/health",
        expect.objectContaining({ signal: expect.any(AbortSignal) }),
      );
    } finally {
      vi.unstubAllEnvs();
    }
  });

  it("labels mock reports and offers explicit repeated-wording input", async () => {
    window.history.replaceState(null, "", "/report?card=A");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ mock_mode: true }),
    }));
    render(<SurgeReport />);
    expect(await screen.findByText(/MOCK REHEARSAL/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Use sample report" }));
    expect(screen.getByTestId("surge-input")).toHaveValue(SURGE_CARDS[0].scene);
    expect(screen.queryByText(/processed by AI/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Don't copy the card/)).not.toBeInTheDocument();
  });

  it("preserves own-word instructions in verified live mode", async () => {
    window.history.replaceState(null, "", "/report?card=A");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ mock_mode: false }),
    }));
    render(<SurgeReport />);
    expect(await screen.findByText(/Don't copy the card/)).toBeInTheDocument();
    expect(screen.queryByText(/MOCK REHEARSAL/)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Use sample report" })).not.toBeInTheDocument();
  });

  it("discloses live AI with temporary storage and keeps live instructions", async () => {
    window.history.replaceState(null, "", "/report?card=A");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ mock_mode: false, storage_mode: "memory" }),
    }));
    render(<SurgeReport />);
    expect(await screen.findByText("LIVE AZURE AI - TEMPORARY DEMO STORAGE")).toBeInTheDocument();
    expect(screen.getByText(/Reports and audit records are held in memory and will be lost on restart/))
      .toBeInTheDocument();
    expect(screen.getByText(/Don't copy the card/)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Use sample report" })).not.toBeInTheDocument();
  });

  it("refreshes mode after the backend changes while the page stays open", async () => {
    vi.useFakeTimers();
    window.history.replaceState(null, "", "/report?card=A");
    let checks = 0;
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => {
      checks += 1;
      return Promise.resolve({
        ok: true,
        json: async () => checks === 1
          ? { mock_mode: true }
          : { mock_mode: false, storage_mode: "memory" },
      });
    }));
    try {
      render(<SurgeReport />);
      await act(async () => {
        await Promise.resolve();
        await Promise.resolve();
        await Promise.resolve();
      });
      expect(screen.getByText(/MOCK REHEARSAL/)).toBeInTheDocument();
      await act(async () => {
        await vi.advanceTimersByTimeAsync(10_000);
      });
      expect(screen.getByText("LIVE AZURE AI - TEMPORARY DEMO STORAGE")).toBeInTheDocument();
      expect(screen.getByText(/Don't copy the card/)).toBeInTheDocument();
      expect(screen.queryByText(/MOCK REHEARSAL/)).not.toBeInTheDocument();
    } finally {
      vi.useRealTimers();
    }
  });

  it("surfaces an unverified mode instead of claiming live AI", async () => {
    window.history.replaceState(null, "", "/report?card=A");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));
    const error = vi.spyOn(console, "error").mockImplementation(() => {});
    try {
      render(<SurgeReport />);
      expect(await screen.findByRole("alert")).toHaveTextContent(/Could not verify/);
      fireEvent.change(screen.getByTestId("surge-input"), { target: { value: "A report" } });
      expect(screen.getByTestId("surge-send")).toBeDisabled();
    } finally {
      error.mockRestore();
    }
  });

  it("prints mock-specific instructions on the QR cards", async () => {
    window.history.replaceState(null, "", "/surge/cards?only=ABCD");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ mock_mode: true }),
    }));
    render(<SurgeCards />);
    expect(await screen.findByText(/MOCK REHEARSAL/)).toBeInTheDocument();
    expect(screen.getAllByText(/Use sample report/)).toHaveLength(4);
    expect(screen.queryByText(/Don't copy this card/)).not.toBeInTheDocument();
  });

  it("prints the temporary-storage disclosure and own-word instructions", async () => {
    window.history.replaceState(null, "", "/surge/cards?only=A");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ mock_mode: false, storage_mode: "memory" }),
    }));
    render(<SurgeCards />);
    expect(await screen.findByText("LIVE AZURE AI - TEMPORARY DEMO STORAGE")).toBeInTheDocument();
    expect(screen.getByText(/audit records are lost on restart/)).toBeInTheDocument();
    expect(screen.getByText(/Don't copy this card/)).toBeInTheDocument();
    expect(screen.queryByText(/Use sample report/)).not.toBeInTheDocument();
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
    const late = {
      ...joined,
      room_counted: false,
      message: "Your report was recorded. The room was reset while it was processing.",
    };
    expect(resultDetail(late)).toContain("room was reset");
  });
});
