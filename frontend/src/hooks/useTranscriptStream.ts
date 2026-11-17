/**
 * Live phone transcripts remain disabled until the backend can authenticate
 * call ownership. Keep the existing hook shape for consumers.
 */

import type { CallState } from "../types/demo";

const unavailableState: CallState = {
  status: "idle",
  callId: null,
  durationSeconds: null,
  events: [],
};

export function useTranscriptStream() {
  return { callState: unavailableState, reset: () => undefined };
}
