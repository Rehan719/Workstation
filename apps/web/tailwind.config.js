/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sovereign: "#020617",
        aura: "#38bdf8",
        highlight: "#fbbf24",
        vital: "#10b981",
      },
    },
  },
  plugins: [],
}
