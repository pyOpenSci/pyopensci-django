/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './core/templates/**/*.html',
    './blog/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'pyos': {
          'deep-purple': '#33205c',
          'dark-purple': '#542668', 
          'medium-purple': '#735fab',
          'light-purple': '#e1dfed',
          'footer-gray': '#eae6ea',
          'footer-text': '#4a5568',
          'teal': '#81c0aa',
        }
      },
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
        'nunito': ['Nunito Sans', 'sans-serif'],
        'itim': ['Itim', 'cursive'],
      }
    },
  },
  plugins: [],
}