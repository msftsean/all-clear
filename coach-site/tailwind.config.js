export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // GI Company tokens
        night: '#1f1f29',
        canvas: '#ffffff',
        paper: '#f2f5f9',
        surface: '#ffffff',
        'surface-raised': '#f8fafc',
        border: '#dde3ea',
        ink: '#111827',
        'ink-secondary': '#4b5563',
        cofounder: '#0081c0',
        'cofounder-dark': '#005f8f',
        'cofounder-soft': '#ddf0fa',
        // Keep legacy aliases for content components
        brand: '#0081c0',
        'accent-soft': '#ddf0fa',
        sage: '#059669',
        'sage-soft': '#d1fae5',
        amber: '#d97706',
      },
      fontFamily: {
        serif: ['"Instrument Serif"', 'Fraunces', 'Georgia', 'serif'],
        sans: ['"Inter Tight"', 'Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'pill': '50.5px',
      },
      boxShadow: {
        'soft': '0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04)',
        'medium': '0 4px 16px rgba(0,0,0,0.08), 0 1px 4px rgba(0,0,0,0.04)',
        'elevated': '0 8px 32px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06)',
        'hero-glow': '0 0 80px rgba(0,129,192,0.25)',
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
