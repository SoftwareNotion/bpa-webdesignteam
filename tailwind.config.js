/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './website/templates/*.html',
  ],
  theme: {
    extend: {
      screens: {
        'smh': {'raw': '(min-height: 600px)'}, 
        'mdh': {'raw': '(min-height: 800px)'},
      }
    },
  },
  plugins: [],
}

