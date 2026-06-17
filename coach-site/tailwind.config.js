export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Coach prep tokens
        night: '#172033',
        canvas: '#F4F8FF',
        paper: '#F4F8FF',
        surface: '#ffffff',
        'surface-raised': '#FFFFFF',
        border: '#D8E6FA',
        ink: '#172033',
        'ink-secondary': '#52627A',
        cofounder: '#173B8F',
        'cofounder-dark': '#0E2A70',
        'cofounder-soft': '#B9D8FF',
        // Keep legacy aliases for content components while retuning the palette.
        brand: '#D62839',
        'accent-soft': '#F7D9DE',
        sage: '#176B54',
        'sage-soft': '#DDF4E8',
        amber: '#B45F06',
      },
      fontFamily: {
        serif: ['"Instrument Serif"', 'Fraunces', 'Georgia', 'serif'],
        sans: ['Figtree', '"Nunito Sans"', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'pill': '50.5px',
      },
      boxShadow: {
        'soft': '0 1px 3px rgba(23,32,51,0.06), 0 8px 20px rgba(23,32,51,0.05)',
        'medium': '0 6px 22px rgba(23,32,51,0.08), 0 1px 4px rgba(23,32,51,0.05)',
        'elevated': '0 10px 36px rgba(23,32,51,0.14), 0 2px 8px rgba(23,32,51,0.06)',
        'hero-glow': '0 0 80px rgba(77,163,255,0.28)',
      },
      keyframes: {
        'fade-slide-up': {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'twinkle': {
          '0%, 100%': { opacity: '0.3' },
          '50%': { opacity: '1' },
        },
        'reveal': {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'glow-pulse': {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '0.8' },
        },
      },
      animation: {
        'fade-slide-up': 'fade-slide-up 0.8s ease-out forwards',
        'fade-slide-up-delay': 'fade-slide-up 0.8s 0.2s ease-out forwards',
        'fade-slide-up-delay2': 'fade-slide-up 0.8s 0.4s ease-out forwards',
        'twinkle': 'twinkle 3s ease-in-out infinite',
        'glow-pulse': 'glow-pulse 4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
