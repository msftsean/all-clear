/**
 * useStudentIdentity — provides a stable, anonymous student identity token.
 *
 * Generates a random UUID on first use and persists it to localStorage so the
 * same token is returned across browser sessions. The token is SHA-256 hashed
 * before being sent to the backend (Constitution Art. III: student IDs must be
 * hashed before storage).
 *
 * Note: this is a device-scoped anonymous identity — no login required.
 */

import { useMemo } from "react";

const STORAGE_KEY = "allclear_student_token";

function getOrCreateToken(): string {
  let token = localStorage.getItem(STORAGE_KEY);
  if (!token) {
    token = crypto.randomUUID();
    localStorage.setItem(STORAGE_KEY, token);
  }
  return token;
}

async function sha256hex(input: string): Promise<string> {
  const encoded = new TextEncoder().encode(input);
  const hashBuffer = await crypto.subtle.digest("SHA-256", encoded);
  return Array.from(new Uint8Array(hashBuffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

export function useStudentIdentity(): {
  token: string;
  getHash: () => Promise<string>;
} {
  const token = useMemo(() => getOrCreateToken(), []);
  const getHash = useMemo(() => () => sha256hex(token), [token]);
  return { token, getHash };
}
