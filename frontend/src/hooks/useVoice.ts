/**
 * useVoice — core hook for WebRTC-based voice interaction via Azure OpenAI Realtime API.
 *
 * Tool call flow:
 *   Azure OpenAI (DataChannel) → response.function_call_arguments.done
 *     → backend WS relay (/api/realtime/ws) → execute_tool (pipeline)
 *     → conversation.item.create (function_call_output) + response.create → Azure OpenAI
 */

import { useReducer, useCallback, useRef, useEffect, useState } from "react";
import { VoiceUIState, type VoiceMessage } from "../types/voice";
import { createRealtimeSession } from "../api/client";

/** Build a ws:// / wss:// URL for the backend tool-relay from the HTTP API base. */
function buildRelayWsUrl(sessionId: string, token: string): string {
  const apiBase = (import.meta.env.VITE_API_BASE_URL as string) || "";
  let base: string;
  if (apiBase.startsWith("http")) {
    base = apiBase.replace(/^http/, "ws");
  } else {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    base = `${protocol}//${window.location.host}${apiBase}`;
  }
  return (
    `${base}/api/realtime/ws` +
    `?session_id=${encodeURIComponent(sessionId)}` +
    `&token=${encodeURIComponent(token)}`
  );
}

interface VoiceState {
  voiceState: VoiceUIState;
  transcript: VoiceMessage[];
  pendingEscalation: boolean;
  error: string | null;
}

type VoiceAction =
  | { type: "START_CONNECTING" }
  | { type: "CONNECTED" }
  | { type: "LISTENING" }
  | { type: "PROCESSING" }
  | { type: "SPEAKING" }
  | { type: "STOP" }
  | { type: "ERROR"; error: string }
  | { type: "ESCALATION_STARTED" }
  | { type: "ESCALATION_FINISHED" }
  | { type: "ADD_TRANSCRIPT"; message: VoiceMessage };

function voiceReducer(state: VoiceState, action: VoiceAction): VoiceState {
  switch (action.type) {
    case "START_CONNECTING":
      return { ...state, voiceState: VoiceUIState.Connecting, error: null };
    case "CONNECTED":
    case "LISTENING":
      return { ...state, voiceState: VoiceUIState.Listening };
    case "PROCESSING":
      return { ...state, voiceState: VoiceUIState.Processing };
    case "SPEAKING":
      return { ...state, voiceState: VoiceUIState.Speaking };
    case "STOP":
      return {
        ...state,
        voiceState: VoiceUIState.Idle,
        pendingEscalation: false,
        error: null,
      };
    case "ERROR":
      return {
        ...state,
        voiceState: VoiceUIState.Error,
        pendingEscalation: false,
        error: action.error,
      };
    case "ESCALATION_STARTED":
      return { ...state, pendingEscalation: true };
    case "ESCALATION_FINISHED":
      return { ...state, pendingEscalation: false };
    case "ADD_TRANSCRIPT":
      return { ...state, transcript: [...state.transcript, action.message] };
    default:
      return state;
  }
}

interface UseVoiceOptions {
  sessionId?: string;
  voice?: string;
  onTranscript?: (message: VoiceMessage) => void;
}

export function useVoice(options: UseVoiceOptions = {}) {
  const [state, dispatch] = useReducer(voiceReducer, {
    voiceState: VoiceUIState.Idle,
    transcript: [],
    pendingEscalation: false,
    error: null,
  });
  const [available, setAvailable] = useState(false);

  const peerConnectionRef = useRef<RTCPeerConnection | null>(null);
  const dataChannelRef = useRef<RTCDataChannel | null>(null);
  const audioElementRef = useRef<HTMLAudioElement | null>(null);
  const pendingEscalationCallIdRef = useRef<string | null>(null);
  // WS relay to backend for tool-call execution
  const wsRelayRef = useRef<WebSocket | null>(null);
  // Pending tool calls: call_id → resolve(result)
  const pendingToolCallsRef = useRef<Map<string, (result: string) => void>>(new Map());
  // Stable ref for onTranscript callback to avoid stale closures
  const onTranscriptRef = useRef(options.onTranscript);
  useEffect(() => {
    onTranscriptRef.current = options.onTranscript;
  }, [options.onTranscript]);

  const isVoiceSupported =
    typeof window !== "undefined" && typeof RTCPeerConnection !== "undefined";

  useEffect(() => {
    let cancelled = false;

    async function checkVoiceHealth() {
      try {
        const response = await fetch("/api/realtime/health");
        if (!response.ok) {
          throw new Error("Voice health check failed");
        }

        const health = (await response.json()) as {
          realtime_available?: boolean;
        };
        if (!cancelled) {
          setAvailable(health.realtime_available === true);
        }
      } catch {
        if (!cancelled) {
          setAvailable(false);
        }
      }
    }

    void checkVoiceHealth();

    return () => {
      cancelled = true;
    };
  }, []);

  const startVoice = useCallback(async () => {
    if (!available) {
      dispatch({
        type: "ERROR",
        error: "Voice is unavailable",
      });
      return;
    }

    if (!isVoiceSupported) {
      dispatch({
        type: "ERROR",
        error: "WebRTC is not supported in this browser",
      });
      return;
    }

    dispatch({ type: "START_CONNECTING" });

    try {
      // 1. Get ephemeral token from backend
      const session = await createRealtimeSession({
        sessionId: options.sessionId,
        voice: options.voice ?? "marin",
      });

      // 2. Open backend WS relay for tool-call execution
      // Must happen before the DataChannel can receive tool calls so the relay
      // is ready by the time Azure OpenAI fires its first function_call_arguments.done.
      const relayUrl = buildRelayWsUrl(session.session_id, session.token);
      const wsRelay = new WebSocket(relayUrl);
      wsRelayRef.current = wsRelay;
      wsRelay.onmessage = (evt) => {
        try {
          const response = JSON.parse(evt.data as string) as {
            call_id: string;
            result: string;
            error?: string | null;
          };
          const { call_id, result, error } = response;
          const resolve = pendingToolCallsRef.current.get(call_id);
          if (resolve) {
            pendingToolCallsRef.current.delete(call_id);
            if (error) {
              console.error(`[Voice relay] tool ${call_id} error:`, error);
              resolve(JSON.stringify({ error }));
            } else {
              resolve(result ?? "{}");
            }
          }
        } catch (e) {
          console.error("[Voice relay] message parse error:", e);
        }
      };
      wsRelay.onerror = (e) => {
        console.error("[Voice relay] WS error:", e);
      };

      // 3. Create RTCPeerConnection
      const pc = new RTCPeerConnection();
      peerConnectionRef.current = pc;

      // 4. Set up remote audio playback
      const audioEl = document.createElement("audio");
      audioEl.autoplay = true;
      audioElementRef.current = audioEl;

      pc.ontrack = (event) => {
        audioEl.srcObject = event.streams[0];
      };

      // 5. Add local mic audio
      const micStream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      micStream.getTracks().forEach((track) => pc.addTrack(track, micStream));

      // 6. Create data channel for Realtime API events
      const dc = pc.createDataChannel("oai-events");
      dataChannelRef.current = dc;

      dc.onopen = () => {
        // Send session.update with BOTH GA nested format AND preview flat format.
        // GA nested: audio.input.transcription, audio.output.voice
        // Preview flat: output_audio_transcription (needed since GA may not support audio.output.transcription)
        // The endpoint accepts what it supports and silently ignores the rest.
        dc.send(
          JSON.stringify({
            type: "session.update",
            session: {
              output_audio_transcription: {
                model: "whisper-1",
              },
              audio: {
                input: {
                  transcription: {
                    model: "whisper-1",
                  },
                },
                output: {
                  voice: options.voice ?? "marin",
                },
              },
            },
          }),
        );
        dispatch({ type: "LISTENING" });
      };

      dc.onmessage = async (event) => {
        try {
          const data = JSON.parse(event.data as string);

          // Log all non-audio-delta events for debugging transcript issues
          if (data.type !== "response.audio.delta") {
            console.log("[DC Event]", data.type);
          }

          const toolName =
            data.tool_name ??
            data.toolName ??
            data.name ??
            data.item?.name ??
            data.function?.name;
          const callId = data.call_id ?? data.callId ?? data.item?.call_id;

          if (
            data.type === "tool_call_request" &&
            toolName === "escalate_to_human"
          ) {
            pendingEscalationCallIdRef.current = callId ?? null;
            dispatch({ type: "ESCALATION_STARTED" });
          } else if (
            data.type === "tool_call_response" &&
            (!pendingEscalationCallIdRef.current ||
              callId === pendingEscalationCallIdRef.current)
          ) {
            pendingEscalationCallIdRef.current = null;
            dispatch({ type: "ESCALATION_FINISHED" });
          }

          if (
            data.type === "response.output_audio_transcript.done" ||
            data.type === "response.audio_transcript.done"
          ) {
            const message: VoiceMessage = {
              id: crypto.randomUUID(),
              content: data.transcript || "",
              role: "assistant",
              timestamp: new Date(),
            };
            dispatch({ type: "ADD_TRANSCRIPT", message });
            onTranscriptRef.current?.(message);
          } else if (
            data.type ===
            "conversation.item.input_audio_transcription.completed"
          ) {
            const message: VoiceMessage = {
              id: crypto.randomUUID(),
              content: data.transcript || "",
              role: "user",
              timestamp: new Date(),
            };
            dispatch({ type: "ADD_TRANSCRIPT", message });
            onTranscriptRef.current?.(message);
          } else if (data.type === "response.output_item.done") {
            // Fallback: extract assistant transcript from completed output item
            // when response.audio_transcript.done is not sent
            const item = data.item;
            if (item?.type === "message" && item?.role === "assistant") {
              const audioPart = item.content?.find(
                (c: { type: string; transcript?: string }) =>
                  c.type === "audio" && c.transcript,
              );
              if (audioPart?.transcript) {
                const message: VoiceMessage = {
                  id: crypto.randomUUID(),
                  content: audioPart.transcript,
                  role: "assistant",
                  timestamp: new Date(),
                };
                dispatch({ type: "ADD_TRANSCRIPT", message });
                onTranscriptRef.current?.(message);
              }
            }
          } else if (data.type === "response.function_call_arguments.done") {
            dispatch({ type: "PROCESSING" });
            // Execute the tool through the backend relay, then return the
            // result to Azure OpenAI via the DataChannel so the model can
            // continue speaking. Without this step, the conversation stalls.
            const callId: string = data.call_id ?? "";
            const toolName: string = data.name ?? "";
            let parsedArgs: Record<string, unknown> = {};
            try {
              parsedArgs = JSON.parse(data.arguments || "{}") as Record<string, unknown>;
            } catch {
              parsedArgs = {};
            }

            const relay = wsRelayRef.current;
            const dc = dataChannelRef.current;
            if (relay && relay.readyState === WebSocket.OPEN && dc && callId && toolName) {
              // Register a callback for when the relay responds with this call_id
              pendingToolCallsRef.current.set(callId, (resultJson: string) => {
                try {
                  dc.send(
                    JSON.stringify({
                      type: "conversation.item.create",
                      item: {
                        type: "function_call_output",
                        call_id: callId,
                        output: resultJson,
                      },
                    }),
                  );
                  dc.send(JSON.stringify({ type: "response.create" }));
                } catch (e) {
                  console.error("Failed to send tool result to Azure:", e);
                }
              });
              relay.send(
                JSON.stringify({
                  call_id: callId,
                  tool_name: toolName,
                  arguments: parsedArgs,
                }),
              );
            } else {
              console.warn(
                "[Voice] Cannot execute tool: relay WS not ready",
                { relay: relay?.readyState, dc: !!dc, callId, toolName },
              );
            }
          } else if (data.type === "response.done") {
            dispatch({ type: "LISTENING" });
          } else if (data.type === "response.audio.delta") {
            dispatch({ type: "SPEAKING" });
          }
        } catch (e) {
          console.error("Data channel message error:", e);
        }
      };

      // 7. Create and set local offer
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);

      // 8. Exchange SDP with Azure OpenAI Realtime API via WebRTC
      const sdpResponse = await fetch(
        `${session.endpoint}/openai/v1/realtime/calls`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${session.token}`,
            "Content-Type": "application/sdp",
          },
          body: offer.sdp,
        },
      );

      if (!sdpResponse.ok) {
        throw new Error(`WebRTC negotiation failed: ${sdpResponse.status}`);
      }

      const answerSdp = await sdpResponse.text();
      await pc.setRemoteDescription({ type: "answer", sdp: answerSdp });

      // 9. Monitor connection state
      pc.onconnectionstatechange = () => {
        switch (pc.connectionState) {
          case "connected":
            dispatch({ type: "LISTENING" });
            break;
          case "disconnected":
          case "failed":
            dispatch({ type: "ERROR", error: "Connection lost" });
            break;
          case "closed":
            dispatch({ type: "STOP" });
            break;
        }
      };
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Failed to start voice";
      dispatch({ type: "ERROR", error: message });
      console.error("Voice start error:", error);
    }
  }, [available, isVoiceSupported, options.sessionId, options.voice]);

  const stopVoice = useCallback(() => {
    if (peerConnectionRef.current) {
      peerConnectionRef.current.close();
      peerConnectionRef.current = null;
    }
    if (dataChannelRef.current) {
      dataChannelRef.current.close();
      dataChannelRef.current = null;
    }
    if (audioElementRef.current) {
      audioElementRef.current.srcObject = null;
      audioElementRef.current = null;
    }
    if (wsRelayRef.current) {
      wsRelayRef.current.close();
      wsRelayRef.current = null;
    }
    pendingToolCallsRef.current.clear();
    pendingEscalationCallIdRef.current = null;
    dispatch({ type: "STOP" });
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopVoice();
    };
  }, [stopVoice]);

  return {
    voiceState: state.voiceState,
    transcript: state.transcript,
    pendingEscalation: state.pendingEscalation,
    error: state.error,
    startVoice,
    stopVoice,
    isVoiceSupported,
    available,
  };
}
