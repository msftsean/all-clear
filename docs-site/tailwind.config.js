/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'deep-space': '#171721',
        'midnight-slate': '#1e1e2a',
        'interactive': '#272735',
        'starlight': '#ededf3',
        'silver': '#c3c3cc',
        'mercury-blue': '#5266eb',
        'lead': '#70707d',
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
