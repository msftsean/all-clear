/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Paper world (conversation column) — inverted to a dark, high-contrast shell
        paper: "#0B0700",
        paper2: "#000000",
        paperline: "#271905",
        inkwarm: "#E8DFCC",
        midwarm: "#AD9D85",
        voice: "#E8C470",
        // Night world (canvas) — inverted into a light cream command surface
        night: "#F7EDD4",
        panel: "#EFDBA5",
        nline: "#D7B262",
        nink: "#0B0700",
        ndim: "#462700",
        cta: "#29D7C6",
        ctaink: "#000000",
        // Status (both worlds)
        sev1: "#29D7C6",
        sev2: "#0F9589",
        sev3: "#B25C00",
        sev4: "#754307",
        clear: "#B63E72",
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
        // Antigravity "lift" — floating cards with inverted gold/cyan-tinted depth
        "antimetal-card":
          "0 1px 2px rgba(232,223,204,0.08), 0 10px 28px -10px rgba(232,196,112,0.36), 0 28px 56px -28px rgba(41,215,198,0.24)",
        "antimetal-soft":
          "0 1px 2px rgba(232,223,204,0.08), 0 8px 20px -12px rgba(232,196,112,0.28)",
        "antimetal-cta":
          "0 10px 26px -6px rgba(41,215,198,0.44)",
        "dark-glass":
          "0 1px 2px rgba(70,39,0,0.18), 0 18px 40px -16px rgba(70,39,0,0.30), inset 0 1px 0 rgba(255,255,255,0.42)",
      },
      backgroundImage: {
        "antimetal-hero":
          "radial-gradient(120% 140% at 86% -22%, #E8C470 0%, #EFDBA5 48%, #F7EDD4 100%)",
        grad: "linear-gradient(100deg, #E8C470 0%, #B25C00 46%, #29D7C6 100%)",
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