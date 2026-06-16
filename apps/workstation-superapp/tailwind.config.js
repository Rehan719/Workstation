import containerQueries from '@tailwindcss/container-queries';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "../../packages/ui/src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sovereign: "#020617", // Deep Space Blue
        aura: "#64ffda",      // Neural Cyan
        highlight: "#ffd740", // Luminous Amber
        vital: "#ff5252",      // Kinetic Red
        surface: "#0f172a",
        border: "rgba(255, 255, 255, 0.1)",
      },
      fontFamily: {
        sans: ['Inter', 'SF Pro Display', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        display: ['Cal Sans', 'Inter', 'sans-serif'],
      },
      animation: {
        'ping-slow': 'ping 3s cubic-bezier(0, 0, 0.2, 1) infinite',
        'pulse-subtle': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'avatar-blink': 'avatar-blink 4.5s ease-in-out infinite',
        'avatar-breathe': 'avatar-breathe 3.2s ease-in-out infinite',
        'avatar-talk': 'avatar-talk 0.32s ease-in-out infinite',
        'avatar-look': 'avatar-look 9s ease-in-out infinite',
        'avatar-sway': 'avatar-sway 5.5s ease-in-out infinite',
        'avatar-drift': 'avatar-drift 7s ease-in-out infinite',
        'avatar-brow': 'avatar-brow 6.5s ease-in-out infinite',
        'eq-bar': 'eq-bar 0.8s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'avatar-blink': {
          '0%, 88%, 100%': { transform: 'scaleY(1)' },
          '94%': { transform: 'scaleY(0.08)' },
        },
        'avatar-breathe': {
          '0%, 100%': { transform: 'scaleY(1) translateY(0)' },
          '50%': { transform: 'scaleY(1.035) translateY(-0.5px)' },
        },
        'avatar-talk': {
          '0%, 100%': { transform: 'scaleY(0.35)' },
          '50%': { transform: 'scaleY(1)' },
        },
        'avatar-look': {
          '0%, 12%, 100%': { transform: 'translateX(0)' },
          '20%, 32%': { transform: 'translateX(1.4px)' },
          '45%, 57%': { transform: 'translateX(-1.4px)' },
          '70%, 100%': { transform: 'translateX(0)' },
        },
        'avatar-sway': {
          '0%, 100%': { transform: 'rotate(0deg)' },
          '50%': { transform: 'rotate(1.2deg)' },
        },
        'avatar-drift': {
          '0%, 100%': { transform: 'scale(1) translateY(0)', opacity: '0.25' },
          '50%': { transform: 'scale(1.08) translateY(-2px)', opacity: '0.4' },
        },
        'eq-bar': {
          '0%, 100%': { transform: 'scaleY(0.3)' },
          '50%': { transform: 'scaleY(1)' },
        },
        'avatar-brow': {
          '0%, 70%, 100%': { transform: 'translateY(0)' },
          '78%, 86%': { transform: 'translateY(-0.6px)' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'aura-glow': 'radial-gradient(circle at 50% 50%, rgba(100, 255, 218, 0.1) 0%, transparent 70%)',
      }
    },
  },
  plugins: [containerQueries],
}
