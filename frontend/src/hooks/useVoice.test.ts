/**
 * useVoice hook tests.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { act, renderHook, waitFor } from "@testing-library/react";
import { useVoice } from "./useVoice";
import { VoiceUIState } from "../types/voice";
import { createRealtimeSession } from "../api/client";

vi.mock("../api/client", () => ({
  createRealtimeSession: vi.fn().mockResolvedValue({
    sessionId: "test-session",
    token: "eph_mock_token",
    expiresAt: new Date(Date.now() + 60_000).toISOString(),
    endpoint: "http://localhost:8000/mock",
    deployment: "gpt-realtime",
  }),
}));

const mockDataChannel = {
  onmessage: null as ((ev: MessageEvent) => void) | null,
  onopen: null as ((ev: Event) => void) | null,
  send: vi.fn(),
  close: vi.fn(),
  readyState: "open" as RTCDataChannelState,
};

const mockPeerConnection = {
  createOffer: vi.fn().mockResolvedValue({ type: "offer", sdp: "mock-sdp" }),
  setLocalDescription: vi.fn().mockResolvedValue(undefined),
  setRemoteDescription: vi.fn().mockResolvedValue(undefined),
  createDataChannel: vi.fn().mockReturnValue(mockDataChannel),
  addTrack: vi.fn(),
  close: vi.fn(),
  connectionState: "new" as RTCPeerConnectionState,
  onconnectionstatechange: null as ((ev: Event) => void) | null,
  ontrack: null as ((ev: RTCTrackEvent) => void) | null,
};

vi.stubGlobal(
  "RTCPeerConnection",
  vi.fn(() => mockPeerConnection),
);
vi.stubGlobal(
  "MediaStream",
  vi.fn(() => ({ getTracks: () => [] })),
);

describe("useVoice hook", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockDataChannel.onmessage = null;
    mockDataChannel.onopen = null;
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.endsWith("/api/realtime/health")) {
          return Promise.resolve({
            ok: true,
            json: vi.fn().mockResolvedValue({
              realtime_available: true,
              mock_mode: false,
              voice_enabled: true,
            }),
          });
        }

        return Promise.resolve({
          ok: true,
          text: vi.fn().mockResolvedValue("mock-answer-sdp"),
        });
      }),
    );
    vi.stubGlobal("navigator", {
      mediaDevices: {
        getUserMedia: vi.fn().mockResolvedValue({
          getTracks: () => [{ stop: vi.fn() }],
        }),
      },
    });
  });

  it("should detect RTCPeerConnection global (WebRTC environment check)", () => {
    expect(typeof RTCPeerConnection).toBe("function");
  });

  it("should export VoiceUIState enum with expected values", () => {
    expect(VoiceUIState.Idle).toBe("idle");
    expect(VoiceUIState.Connecting).toBe("connecting");
    expect(VoiceUIState.Listening).toBe("listening");
    expect(VoiceUIState.Processing).toBe("processing");
    expect(VoiceUIState.Speaking).toBe("speaking");
    expect(VoiceUIState.Error).toBe("error");
  });

  it("does not connect when health reports unavailable", async () => {
    vi.mocked(fetch).mockImplementation((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith("/api/realtime/health")) {
        return Promise.resolve({
          ok: true,
          json: vi.fn().mockResolvedValue({
            realtime_available: false,
            mock_mode: true,
            voice_enabled: false,
          }),
        } as Response);
      }

      throw new Error(`Unexpected fetch: ${url}`);
    });

    const { result } = renderHook(() => useVoice());

    await waitFor(() => expect(result.current.available).toBe(false));

    await act(async () => {
      await result.current.startVoice();
    });

    expect(createRealtimeSession).not.toHaveBeenCalled();
    expect(RTCPeerConnection).not.toHaveBeenCalled();
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("tracks pending escalation between tool request and response events", async () => {
    const { result } = renderHook(() => useVoice());

    await waitFor(() => expect(result.current.available).toBe(true));

    await act(async () => {
      await result.current.startVoice();
    });

    act(() => {
      mockDataChannel.onopen?.(new Event("open"));
    });

    expect(result.current.voiceState).toBe(VoiceUIState.Listening);

    act(() => {
      mockDataChannel.onmessage?.({
        data: JSON.stringify({
          type: "tool_call_request",
          tool_name: "escalate_to_human",
          call_id: "call-1",
        }),
      } as MessageEvent);
    });

    await waitFor(() => expect(result.current.pendingEscalation).toBe(true));

    act(() => {
      mockDataChannel.onmessage?.({
        data: JSON.stringify({
          type: "tool_call_response",
          call_id: "call-1",
          result: "{}",
        }),
      } as MessageEvent);
    });

    await waitFor(() => expect(result.current.pendingEscalation).toBe(false));
  });

  it.todo("should initialize with Idle state");
  it.todo("should transition to Connecting on startVoice");
  it.todo("should call createRealtimeSession on start");
  it.todo("should create RTCPeerConnection with received endpoint");
  it.todo('should create data channel named "oai-events"');
  it.todo("should transition to Listening when WebRTC data channel opens");
  it.todo("should relay function_call events through data channel");
  it.todo("should return to Idle on stopVoice");
  it.todo("should set Error state when session creation fails");
  it.todo("should handle WebRTC not supported (no RTCPeerConnection global)");
  it.todo(
    "should expose voiceState, startVoice, stopVoice, transcript, isSpeaking",
  );
});
