/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        accent: {
          DEFAULT: '#B8FF00', // neon-green
          light: '#DFFF4D',
          dark: '#A6D900',
          blue: '#0EA5E9',    // electric-blue
        },
        dark: {
          900: '#0a0a0a',     // Strict dark bg
          800: '#0D0A06',
          700: '#151008',
          600: '#1A140B',
          500: '#221A10',
          400: '#2A2015',
          300: '#3A2E1E',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        serif: ['Playfair Display', 'Georgia', 'serif'],
      },
    },
  },
  plugins: [],
}
