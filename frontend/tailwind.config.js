/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: 'var(--surface-card)',
          muted: 'var(--surface-muted)',
          elevated: 'var(--surface-elevated)',
        },
        ink: {
          DEFAULT: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted: 'var(--text-muted)',
        },
        accent: {
          blue: '#3b82f6',
          purple: '#7c3aed',
          cyan: '#06b6d4',
          electric: '#6366f1',
        },
        primary: {
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
        },
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      borderRadius: {
        premium: {
          DEFAULT: '1.25rem',
          lg: '1.5rem',
          xl: '1.75rem',
        },
      },
      boxShadow: {
        'glow-sm': 'var(--glow-sm)',
        glow: 'var(--glow-md)',
        'glow-lg': 'var(--glow-lg)',
        card: 'var(--shadow-card)',
        'card-hover': 'var(--shadow-card-hover)',
        modal: 'var(--shadow-modal)',
        sm: 'var(--shadow-sm)',
      },
      backdropBlur: {
        premium: '24px',
        'premium-lg': '32px',
      },
      transitionDuration: {
        premium: '300ms',
        'premium-fast': '200ms',
      },
      animation: {
        'fade-in': 'fadeIn 0.35s ease-out both',
        'fade-up': 'fadeUp 0.45s cubic-bezier(0.22, 1, 0.36, 1) both',
        'slide-in': 'slideIn 0.35s cubic-bezier(0.22, 1, 0.36, 1) both',
        'scale-in': 'scaleIn 0.3s cubic-bezier(0.22, 1, 0.36, 1) both',
        float: 'float 14s ease-in-out infinite',
        'float-slow': 'float 22s ease-in-out infinite',
        'pulse-soft': 'pulseSoft 4s ease-in-out infinite',
        shimmer: 'shimmer 2.2s linear infinite',
        'mesh-drift': 'meshDrift 28s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(14px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(-10px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.97)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        float: {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
          '50%': { transform: 'translate(0, -14px) scale(1.02)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '0.35' },
          '50%': { opacity: '0.65' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        meshDrift: {
          '0%, 100%': { transform: 'translate(0%, 0%) rotate(0deg)' },
          '33%': { transform: 'translate(2%, -1%) rotate(1deg)' },
          '66%': { transform: 'translate(-1%, 2%) rotate(-1deg)' },
        },
        orbMove: {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
          '33%': { transform: 'translate(24px, -20px) scale(1.03)' },
          '66%': { transform: 'translate(-16px, 16px) scale(0.98)' },
        },
      },
      transitionTimingFunction: {
        smooth: 'cubic-bezier(0.4, 0, 0.2, 1)',
        premium: 'cubic-bezier(0.22, 1, 0.36, 1)',
        spring: 'cubic-bezier(0.34, 1.2, 0.64, 1)',
      },
    },
  },
  plugins: [],
}
