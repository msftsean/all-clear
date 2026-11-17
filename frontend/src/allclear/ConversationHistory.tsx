/**
 * Conversation history is disabled until the backend can verify session ownership.
 * A browser-generated hash or shared voice hash is not an authorization contract.
 */

interface ConversationHistoryProps {
  studentIdHash: string | null;
  onResume?: (sessionId: string) => void;
}

export default function ConversationHistory({
  studentIdHash,
}: ConversationHistoryProps) {
  const message = studentIdHash
    ? "Conversation history is unavailable until authenticated ownership is configured."
    : "No identity found. Submit a signal to start tracking history.";

  return <p className="text-sm text-zinc-500 p-4">{message}</p>;
}
