/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Paper world (conversation column) — Antigravity light surface
        paper: "#f4f6fe",
        paper2: "#ffffff",
        paperline: "#e7eaf6",
        inkwarm: "#161b33",
        midwarm: "#565d7a",
        voice: "#4f6bff",
        // Night world (canvas) — Antigravity deep space
        night: "#070b1a",
        panel: "#141a3a",
        nline: "#2a335f",
        nink: "#eef1ff",
        ndim: "#9aa6d6",
        cta: "#4f6bff",
        ctaink: "#ffffff",
        // Status (both worlds)
        sev1: "#E25555",
        sev2: "#E59A3A",
        sev3: "#5B8FE8",
        sev4: "#5B8FE8",
        clear: "#37C281",
      },
      fontFamily: {
        display: ["Google Sans Flex", "Google Sans", "Segoe UI", "system-ui", "sans-serif"],
        sans: ["Google Sans Flex", "Google Sans", "Segoe UI", "system-ui", "sans-serif"],
        mono: ["Google Sans Code", "ui-monospace", "Menlo", "monospace"],
      },
      borderRadius: {
        card: "20px",
        bubble: "14px",
        chip: "9999px",
        tag: "6px",
      },
      boxShadow: {
        // Antigravity "lift" — floating cards with violet-tinted depth
        "antimetal-card":
          "0 1px 2px rgba(20,28,72,0.05), 0 10px 28px -10px rgba(48,60,150,0.20), 0 28px 56px -28px rgba(48,60,150,0.22)",
        "antimetal-soft":
          "0 1px 2px rgba(20,28,72,0.05), 0 8px 20px -12px rgba(48,60,150,0.18)",
        "antimetal-cta":
          "0 10px 26px -6px rgba(99,90,255,0.55)",
        "dark-glass":
          "0 1px 2px rgba(0,0,0,0.40), 0 18px 40px -16px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.06)",
      },
      backgroundImage: {
        "antimetal-hero":
          "radial-gradient(125% 145% at 86% -22%, #2a3470 0%, #0e1330 46%, #070b1a 100%)",
        grad: "linear-gradient(100deg, #3d7bfd 0%, #7b5cff 52%, #d957d5 100%)",
      },
      keyframes: {
        bar: {
          "0%, 100%": { transform: "scaleY(0.35)" },
          "50%": { transform: "scaleY(1)" },
        },
        blink: { "0%, 100%": { opacity: "1" }, "50%": { opacity: "0.25" } },
        rise: { "0%": { opacity: "0", transform: "translateY(8px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
      },
      animation: {
        bar: "bar 1s ease-in-out infinite",
        blink: "blink 1.4s ease-in-out infinite",
        rise: "rise 300ms ease-out both",
      },
    },
  },
  plugins: [],
};