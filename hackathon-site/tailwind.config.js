/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        maroon: '#D62839',
        'deep-maroon': '#173B8F',
        gold: '#4DA3FF',
        'light-gold': '#B9D8FF',
        cream: '#F4F8FF',
        'deep-cream': '#F7D9DE',
        ink: '#172033',
      },
      fontFamily: {
        serif: ['Playfair Display', 'Georgia', 'serif'],
        sans: ['Source Serif 4', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
};
