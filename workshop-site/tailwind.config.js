/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        ink: '#172033',
        surface: '#FFFFFF',
        'surface-muted': '#F4F8FF',
        border: '#D8E6FA',
        brand: '#173B8F',
        accent: '#D62839',

        bg: '#F4F8FF',
        fg: '#172033',
        'dark-text': '#172033',
        'iu-crimson': '#D62839',
        'microsoft-blue': '#173B8F',
        'neutral-gray': '#F4F8FF',
      },
      fontFamily: {
        display: ['var(--font-display)'],
        sans: ['var(--font-body)'],
      },
    },
  },
  plugins: [],
}
