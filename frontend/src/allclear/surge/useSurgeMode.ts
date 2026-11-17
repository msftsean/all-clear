import { useEffect, useState } from "react";

export type SurgeMode = "checking" | "mock" | "live" | "error";

export function useSurgeMode(): SurgeMode {
  const [mode, setMode] = useState<SurgeMode>("checking");
  useEffect(() => {
    let active = true;
    async function check() {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_BASE_URL || ""}/api/health`,
        );
        if (!response.ok) throw new Error("Processing mode check failed.");
        const data: unknown = await response.json();
        if (
          typeof data !== "object" ||
          data === null ||
          !("mock_mode" in data) ||
          typeof data.mock_mode !== "boolean"
        ) {
          throw new Error("Processing mode response is invalid.");
        }
        if (active) setMode(data.mock_mode ? "mock" : "live");
      } catch (error) {
        if (active) {
          console.error("Could not verify Surge processing mode", error);
          setMode("error");
        }
      }
    }
    void check();
    return () => {
      active = false;
    };
  }, []);
  return mode;
}
