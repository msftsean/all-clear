import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";

const source = new URL("../docs/event-readiness/showcase-2026-11-17.html", import.meta.url);
const output = new URL("./site/", import.meta.url);
const commit = "f006be0bb1f5298b6aa1b80ffe6f77c5cabb8f18";
const html = (await readFile(source, "utf8")).replace(
  /href="\.\.\/\.\.\/([^"]+)"/g,
  (_, path) => `href="https://github.com/msftsean/all-clear/blob/${commit}/${path}"`,
);
const hashes = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(
  match => `'sha256-${createHash("sha256").update(match[1].replace(/\r\n/g, "\n")).digest("base64")}'`,
);
if (hashes.length !== 2) throw new Error("Expected exactly two inline scripts.");
if (html.includes('href="../../')) throw new Error("Unresolved repository-relative link.");
const config = {
  globalHeaders: {
    "X-Robots-Tag": "noindex, nofollow, noarchive",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
    "Content-Security-Policy": [
      "default-src 'none'",
      `script-src ${hashes.join(" ")}`,
      "style-src 'unsafe-inline'",
      "img-src 'self' data:",
      "connect-src 'none'",
      "base-uri 'none'",
      "form-action 'none'",
      "frame-ancestors 'none'",
    ].join("; "),
  },
};
await mkdir(output, { recursive: true });
await Promise.all([
  writeFile(new URL("index.html", output), html, "utf8"),
  writeFile(new URL("staticwebapp.config.json", output), JSON.stringify(config, null, 2) + "\n", "utf8"),
  writeFile(new URL("robots.txt", output), "User-agent: *\nDisallow: /\n", "utf8"),
]);
console.log("Packaged presenter HTML, hashed-script security policy, and robots.txt. No backend or secrets included.");
