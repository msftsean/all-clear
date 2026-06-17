/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        ink: '#1B1B1F',
        surface: '#FFFFFF',
        'surface-muted': '#F7F8FA',
        border: '#E6E8EC',
        brand: '#0F6CBD',
        accent: '#990000',

        bg: '#F7F8FA',
        fg: '#1B1B1F',
        'dark-text': '#1B1B1F',
        'iu-crimson': '#990000',
        'microsoft-blue': '#0F6CBD',
        'neutral-gray': '#F7F8FA',
      },
      fontFamily: {
        display: ['var(--font-display)'],
        sans: ['var(--font-body)'],
      },
    },
  },
  plugins: [],
}
