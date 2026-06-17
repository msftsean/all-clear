export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Coach prep tokens
        night: '#2B2622',
        canvas: '#FBF8F4',
        paper: '#FBF8F4',
        surface: '#ffffff',
        'surface-raised': '#FFFDF9',
        border: '#ECE6DD',
        ink: '#2B2622',
        'ink-secondary': '#6D6259',
        cofounder: '#B25B34',
        'cofounder-dark': '#8F4425',
        'cofounder-soft': '#F3E7DE',
        // Keep legacy aliases for content components while retuning the palette.
        brand: '#B25B34',
        'accent-soft': '#F3E7DE',
        sage: '#3F7E6E',
        'sage-soft': '#E3EFEA',
        amber: '#A8661B',
      },
      fontFamily: {
        serif: ['"Instrument Serif"', 'Fraunces', 'Georgia', 'serif'],
        sans: ['Figtree', '"Nunito Sans"', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'pill': '50.5px',
      },
      boxShadow: {
        'soft': '0 1px 3px rgba(43,38,34,0.06), 0 8px 20px rgba(43,38,34,0.05)',
        'medium': '0 6px 22px rgba(43,38,34,0.08), 0 1px 4px rgba(43,38,34,0.05)',
        'elevated': '0 10px 36px rgba(43,38,34,0.14), 0 2px 8px rgba(43,38,34,0.06)',
        'hero-glow': '0 0 80px rgba(178,91,52,0.24)',
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
