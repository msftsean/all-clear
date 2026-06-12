/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Paper world (conversation column)
        paper: "#f8f9fc",
        paper2: "#ffffff",
        paperline: "#dfe3ea",
        inkwarm: "#1b2540",
        midwarm: "#6b7184",
        voice: "#0050f8",
        // Night world (canvas)
        night: "#001033",
        panel: "#14213f",
        nline: "#26345c",
        nink: "#e0f6ff",
        ndim: "#9fb6d8",
        cta: "#d0f100",
        ctaink: "#1b2540",
        // Status (both worlds)
        sev1: "#E25555",
        sev2: "#E59A3A",
        sev3: "#5B8FE8",
        sev4: "#5B8FE8",
        clear: "#37C281",
      },
      fontFamily: {
        display: ["Fraunces", "Georgia", "serif"],
        sans: ["DM Sans", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Menlo", "monospace"],
      },
      borderRadius: {
        card: "20px",
        bubble: "14px",
        chip: "9999px",
        tag: "6px",
      },
      boxShadow: {
        "antimetal-card":
          "rgba(0,39,80,0.03) 0px 56px 72px -16px, rgba(0,39,80,0.03) 0px 32px 32px -16px, rgba(0,39,80,0.04) 0px 6px 12px -3px, rgba(0,39,80,0.04) 0px 0px 0px 1px",
        "antimetal-soft":
          "rgba(255,255,255,0.72) 0px 1px 1px 0px inset, rgba(4,33,80,0.02) 0px 8px 16px 0px, rgba(4,33,80,0.03) 0px 4px 12px 0px, rgba(4,33,80,0.06) 0px 1px 2px 0px, rgba(4,33,80,0.04) 0px 0px 0px 1px",
        "antimetal-cta":
          "rgba(24,37,66,0.32) 0px 1px 3px 0px, rgba(24,37,66,0.12) 0px 0.5px 0.5px 0px, rgba(24,37,66,0.44) 0px 12px 24px -12px, rgba(219,247,255,0.06) 0px 8px 16px 0px inset, rgba(219,247,255,0.48) 0px 0.5px 0.5px 0px inset",
        "dark-glass":
          "rgba(24,37,66,0.32) 0px 1px 3px 0px, rgba(24,37,66,0.44) 0px 12px 24px -12px, rgba(219,247,255,0.48) 0px 0.5px 0.5px 0px inset, rgba(219,247,255,0.04) 0px -4px 8px 0px inset",
      },
      backgroundImage: {
        "antimetal-hero": "linear-gradient(180deg,#001033 0%,#0050f8 55%,#5fbdf7 100%)",
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