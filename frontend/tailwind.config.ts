import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        surface: {
          light: '#ffffff',
          dark: '#111827',
        },
        card: {
          light: '#ffffff',
          dark: '#1f2937',
        },
      },
    },
  },
  plugins: [],
} satisfies Config
