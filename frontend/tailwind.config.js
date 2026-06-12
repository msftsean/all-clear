/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Paper world (conversation column)
        paper: "#F2EDE3",
        paper2: "#FFFDF7",
        paperline: "#E0D8C8",
        inkwarm: "#2E2A22",
        midwarm: "#6E6657",
        voice: "#B0541F",
        // Night world (canvas)
        night: "#10161F",
        panel: "#161E2A",
        nline: "#27324A",
        nink: "#C6D2E4",
        ndim: "#7C8CA6",
        // Status (both worlds)
        sev1: "#E25555",
        sev2: "#E59A3A",
        sev3: "#5B8FE8",
        sev4: "#5B8FE8",
        clear: "#37C281",
      },
      fontFamily: {
        display: ["Archivo", "system-ui", "sans-serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Menlo", "monospace"],
      },
      borderRadius: {
        card: "10px",
        bubble: "12px",
        chip: "5px",
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