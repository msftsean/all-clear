import { useEffect, useState } from "react";

export type SurgeMode = "checking" | "mock" | "live" | "live-demo" | "error";

const HEALTH_POLL_MS = 10_000;
const HEALTH_TIMEOUT_MS = 3_000;

export function useSurgeMode(): SurgeMode {
  const [mode, setMode] = useState<SurgeMode>("checking");
  useEffect(() => {
    let active = true;
    let timer: number | undefined;
    let controller: AbortController | undefined;
    async function check() {
      const requestController = new AbortController();
      controller = requestController;
      const timeout = window.setTimeout(
        () => requestController.abort(),
        HEALTH_TIMEOUT_MS,
      );
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_BASE_URL || ""}/api/health`,
          { signal: requestController.signal },
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
        let next: SurgeMode;
        if (data.mock_mode) {
          next = "mock";
        } else if (!("storage_mode" in data)) {
          next = "live";
        } else if (data.storage_mode === "memory") {
          next = "live-demo";
        } else if (data.storage_mode === "cosmos") {
          next = "live";
        } else {
          throw new Error("Processing storage mode is invalid.");
        }
        if (active) setMode(next);
      } catch (error) {
        if (active) {
          console.error("Could not verify Surge processing mode", error);
          setMode("error");
        }
      } finally {
        window.clearTimeout(timeout);
        if (controller === requestController) controller = undefined;
        if (active) {
          timer = window.setTimeout(() => void check(), HEALTH_POLL_MS);
        }
      }
    }
    void check();
    return () => {
      active = false;
      if (timer !== undefined) window.clearTimeout(timer);
      controller?.abort();
    };
  }, []);
  return mode;
}
