/**
 * Main chat container component.
 */

import { useRef, useEffect, useCallback } from "react";
import { MessageBubble } from "./MessageBubble";
import { ChatInput } from "./ChatInput";
import { TypingIndicator } from "./TypingIndicator";
import { VoiceMicButton } from "./VoiceMicButton";
import { VoiceStatusIndicator } from "./VoiceStatusIndicator";
import { VoiceTranscript } from "./VoiceTranscript";
import { useVoice } from "../hooks/useVoice";
import { VoiceUIState } from "../types/voice";
import type { Message } from "../types";

interface ChatContainerProps {
  messages: Message[];
  isLoading: boolean;
  sessionId: string | null;
  onSendMessage: (content: string) => Promise<void>;
}

export function ChatContainer({
  messages,
  isLoading,
  sessionId,
  onSendMessage,
}: ChatContainerProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatRegionRef = useRef<HTMLDivElement>(null);
  const chatInputRef = useRef<HTMLTextAreaElement>(null);
  const previousVoiceStateRef = useRef<VoiceUIState | null>(null);

  const {
    voiceState,
    transcript,
    pendingEscalation,
    startVoice,
    stopVoice,
    isVoiceSupported,
    available,
  } = useVoice({
    sessionId: sessionId ?? undefined,
  });

  const handleVoiceToggle = useCallback(() => {
    if (!available) {
      return;
    }

    if (voiceState === VoiceUIState.Idle || voiceState === VoiceUIState.Error) {
      startVoice();
    } else {
      stopVoice();
    }
  }, [available, voiceState, startVoice, stopVoice]);

  // Auto-scroll to bottom when new messages or transcript entries arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, transcript, isLoading]);

  // Announce new messages to screen readers
  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.role === "assistant") {
        // The aria-live region will announce this automatically
      }
    }
  }, [messages]);

  useEffect(() => {
    const previousVoiceState = previousVoiceStateRef.current;
    if (
      previousVoiceState &&
      previousVoiceState !== voiceState &&
      (voiceState === VoiceUIState.Idle || voiceState === VoiceUIState.Error)
    ) {
      chatInputRef.current?.focus();
    }
    previousVoiceStateRef.current = voiceState;
  }, [voiceState]);

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-80px)]">
      {/* Voice status banner (hidden when idle) */}
      {voiceState !== VoiceUIState.Idle && (
        <div className="flex justify-center px-4 pt-2">
          <VoiceStatusIndicator
            voiceState={voiceState}
            pendingEscalation={pendingEscalation}
          />
        </div>
      )}

      {/* Messages area */}
      <div
        ref={chatRegionRef}
        className="flex-1 overflow-y-auto px-4 py-6 space-y-4"
        role="log"
        aria-label="Chat messages"
        aria-live="polite"
        aria-atomic="false"
        aria-relevant="additions"
      >
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {/* Voice transcript appears inline after text messages */}
        <VoiceTranscript messages={transcript} />

        {isLoading && <TypingIndicator />}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-gray-200 bg-white px-4 py-4">
        <div className="flex items-end gap-2">
          <div className="flex-1">
            <ChatInput
              ref={chatInputRef}
              onSend={onSendMessage}
              disabled={isLoading}
            />
          </div>
          {isVoiceSupported && (
            <VoiceMicButton
              voiceState={voiceState}
              onToggle={handleVoiceToggle}
              disabled={isLoading}
              available={available}
            />
          )}
        </div>

        {/* Session indicator */}
        {sessionId && (
          <p className="mt-2 text-xs text-gray-400 text-center">
            Session: {sessionId.slice(0, 8)}...
          </p>
        )}
      </div>
    </div>
  );
}
