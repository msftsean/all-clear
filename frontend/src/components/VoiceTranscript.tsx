/**
 * VoiceTranscript — renders voice conversation transcript entries.
 */

import React from "react";
import { MicrophoneIcon, SpeakerWaveIcon } from "@heroicons/react/24/solid";
import type { VoiceMessage } from "../types/voice";

interface VoiceTranscriptProps {
  messages: VoiceMessage[];
}

export const VoiceTranscript: React.FC<VoiceTranscriptProps> = ({
  messages,
}) => {
  if (messages.length === 0) return null;

  return (
    <div className="space-y-2 py-2" role="log" aria-label="Voice transcript">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`
              max-w-[80%] rounded-lg px-3 py-2 text-sm
              ${
                msg.role === "user"
                  ? "bg-blue-100 text-blue-900"
                  : "bg-gray-100 text-gray-900"
              }
            `}
          >
            <div className="flex items-center gap-1.5 mb-1">
              <span
                aria-label={
                  msg.role === "user"
                    ? "User voice message badge"
                    : "Assistant voice message badge"
                }
                className={`inline-flex h-5 w-5 items-center justify-center rounded-full ${
                  msg.role === "user"
                    ? "bg-white text-blue-700"
                    : "bg-blue-100 text-blue-700"
                }`}
              >
                {msg.role === "user" ? (
                  <MicrophoneIcon className="w-3 h-3" aria-hidden="true" />
                ) : (
                  <SpeakerWaveIcon className="w-3 h-3" aria-hidden="true" />
                )}
              </span>
              <span className="text-xs opacity-60">
                {msg.role === "user" ? "You (voice)" : "Agent"}
              </span>
            </div>
            <p>{msg.content}</p>
            <time className="text-xs opacity-40 mt-1 block">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </time>
          </div>
        </div>
      ))}
    </div>
  );
};
