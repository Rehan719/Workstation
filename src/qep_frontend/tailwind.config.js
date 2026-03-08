/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      colors: {
        primary: {
          DEFAULT: '#004d40',
          light: '#00796b',
        },
        accent: '#d4af37',
      }
    },
  },
  plugins: [],
  safelist: [
    {
      pattern: /(bg|text|border)-(emerald|blue|purple|orange|teal|amber)-(400|500|600|900)\/(5|10|20|30)/,
    },
    'bg-emerald-500/20', 'text-emerald-400', 'border-emerald-500/30',
    'bg-blue-500/20', 'text-blue-400', 'border-blue-500/30',
    'bg-purple-500/20', 'text-purple-400', 'border-purple-500/30',
    'bg-orange-500/20', 'text-orange-400', 'border-orange-500/30',
    'bg-teal-500/20', 'text-teal-400', 'border-teal-500/30',
    'bg-emerald-500/5', 'border-emerald-500/10',
    'bg-blue-500/5', 'border-blue-500/10',
    'bg-purple-500/5', 'border-purple-500/10',
    'bg-orange-500/5', 'border-orange-500/10',
    'bg-teal-500/5', 'border-teal-500/10',
    'text-emerald-400', 'text-blue-400', 'text-purple-400', 'text-orange-400', 'text-teal-400'
  ]
}
