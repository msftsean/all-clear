/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: 'rgb(var(--bg-rgb) / <alpha-value>)',
        fg: 'rgb(var(--fg-rgb) / <alpha-value>)',
        ink: 'rgb(var(--fg-rgb) / <alpha-value>)',
        surface: 'rgb(var(--surface-rgb) / <alpha-value>)',
        'surface-muted': 'rgb(var(--surface-elevated-rgb) / <alpha-value>)',
        border: 'rgb(var(--border-rgb) / <alpha-value>)',
        brand: 'rgb(var(--accent-rgb) / <alpha-value>)',
        accent: 'rgb(var(--danger-rgb) / <alpha-value>)',
        'dark-text': 'rgb(var(--fg-rgb) / <alpha-value>)',
        'iu-crimson': 'rgb(var(--danger-rgb) / <alpha-value>)',
        'microsoft-blue': 'rgb(var(--accent-rgb) / <alpha-value>)',
        'neutral-gray': 'rgb(var(--surface-elevated-rgb) / <alpha-value>)',
      },
      fontFamily: {
        display: ['var(--font-display)'],
        sans: ['var(--font-body)'],
      },
    },
  },
  plugins: [],
}
