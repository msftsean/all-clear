# Frontend

## Voice interaction

The voice UI lives in `frontend/src/components/` and is driven by `frontend/src/hooks/useVoice.ts`.

### Components

- `VoiceMicButton` — microphone toggle button. It reflects the current `VoiceUIState`, exposes accessible labels, and supports Enter to start plus Escape to stop while active.
- `VoiceTranscript` — renders voice transcript bubbles for user and assistant messages with microphone/speaker icons.
- `VoiceStatusIndicator` — announces the active voice state in an ARIA live status pill.

### `useVoice` hook

`useVoice` creates the realtime session with `POST /api/realtime/session`, manages the browser `RTCPeerConnection`, requests microphone audio with `navigator.mediaDevices.getUserMedia`, opens the Realtime API data channel, tracks transcript messages, and exposes:

- `voiceState`
- `transcript`
- `error`
- `startVoice()`
- `stopVoice()`
- `isVoiceSupported`

### State machine

`VoiceUIState` is defined in `frontend/src/types/voice.ts` with six states:

```text
Idle -> Connecting -> Listening -> Processing -> Speaking
  ^         |             |            |             |
  |         v             v            v             v
  +---------------------- Error <--------------------+
```

- `Idle`: no active voice session.
- `Connecting`: session/token and WebRTC setup in progress.
- `Listening`: connected and ready for user speech.
- `Processing`: a tool call or response is being processed.
- `Speaking`: assistant audio is streaming.
- `Error`: voice failed or connection was lost; text chat should remain usable.

### Browser support

Voice requires native WebRTC support: Chrome 90+, Firefox 85+, Edge 90+, or Safari 15+.
