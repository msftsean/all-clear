/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'deep-space': '#08131a',
        'midnight-slate': '#0d2028',
        'interactive': '#102a31',
        'starlight': '#e8f1ed',
        'silver': '#b6cbc5',
        'mercury-blue': '#20c997',
        'lead': '#55747a',
      },
      fontFamily: {
        sans: ['Manrope', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      fontWeight: {
        display: '300',
      },
    },
  },
  plugins: [],
}
