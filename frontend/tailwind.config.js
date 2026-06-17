/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Paper world (conversation column) — bold blue/red with pastel support
        paper: "#F4F8FF",
        paper2: "#ffffff",
        paperline: "#D8E6FA",
        inkwarm: "#172033",
        midwarm: "#52627A",
        voice: "#173B8F",
        // Night world (canvas) — heroic blue with red signal accents
        night: "#08122B",
        panel: "#10245A",
        nline: "#284D9D",
        nink: "#F4F8FF",
        ndim: "#B9D8FF",
        cta: "#D62839",
        ctaink: "#ffffff",
        // Status (both worlds)
        sev1: "#D62839",
        sev2: "#F06A76",
        sev3: "#4DA3FF",
        sev4: "#8ABCF8",
        clear: "#49C18D",
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
        // Antigravity "lift" — floating cards with blue/red-tinted depth
        "antimetal-card":
          "0 1px 2px rgba(23,32,51,0.05), 0 10px 28px -10px rgba(23,59,143,0.22), 0 28px 56px -28px rgba(214,40,57,0.18)",
        "antimetal-soft":
          "0 1px 2px rgba(23,32,51,0.05), 0 8px 20px -12px rgba(23,59,143,0.18)",
        "antimetal-cta":
          "0 10px 26px -6px rgba(214,40,57,0.42)",
        "dark-glass":
          "0 1px 2px rgba(0,0,0,0.40), 0 18px 40px -16px rgba(0,0,0,0.55), inset 0 1px 0 rgba(244,248,255,0.08)",
      },
      backgroundImage: {
        "antimetal-hero":
          "radial-gradient(120% 140% at 86% -22%, #173B8F 0%, #10245A 48%, #08122B 100%)",
        grad: "linear-gradient(100deg, #173B8F 0%, #4DA3FF 46%, #D62839 100%)",
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