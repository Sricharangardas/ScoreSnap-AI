/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable class-based dark mode toggling
  theme: {
    extend: {
      colors: {
        apple: {
          bg: {
            light: '#F5F5F7',
            dark: '#000000',
          },
          card: {
            light: 'rgba(255, 255, 255, 0.7)',
            dark: 'rgba(28, 28, 30, 0.7)',
          },
          text: {
            light: '#1D1D1F',
            dark: '#FFFFFF',
            subLight: '#6E6E73',
            subDark: '#AEAEB2',
          },
          blue: {
            light: '#007AFF',
            dark: '#0A84FF',
          },
          green: {
            light: '#34C759',
            dark: '#30D158',
          },
          red: {
            light: '#FF3B30',
            dark: '#FF453A',
          },
          orange: {
            light: '#FF9500',
            dark: '#FF9F0A',
          }
        }
      },
      fontFamily: {
        sans: ['SF Pro Display', 'SF Pro Text', 'Inter', 'sans-serif'],
      },
      backdropBlur: {
        xs: '2px',
        md: '12px',
        lg: '24px',
        xl: '40px',
      },
      boxShadow: {
        appleLight: '0 4px 30px rgba(0, 0, 0, 0.03)',
        appleDark: '0 4px 30px rgba(0, 0, 0, 0.2)',
        appleFloat: '0 20px 50px rgba(0, 0, 0, 0.1)',
        appleBlue: '0 4px 20px rgba(0, 122, 255, 0.25)',
      },
      borderRadius: {
        'apple-lg': '24px',
        'apple-md': '18px',
        'apple-sm': '12px',
      }
    },
  },
  plugins: [],
}
