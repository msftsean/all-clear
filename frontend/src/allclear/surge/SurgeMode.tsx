import type { SurgeMode } from "./useSurgeMode";

export function SurgeModeNotice({ mode }: { mode: SurgeMode }) {
  if (mode === "live") return null;
  return (
    <p
      role={mode === "error" ? "alert" : "status"}
      className="rounded-bubble border border-sev2/60 bg-panel px-3 py-2 text-sm text-nink"
    >
      {mode === "mock"
        ? "MOCK REHEARSAL - no live AI. Repeated wording demonstrates grouping; reports are temporary."
        : mode === "error"
          ? "Could not verify processing mode. Refresh before sending a report."
          : "Checking processing mode..."}
    </p>
  );
}
