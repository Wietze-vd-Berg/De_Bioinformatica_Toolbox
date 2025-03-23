import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    // eventueel andere plugins hier
  ],
  css: {
    postcss: {
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
      ]
    }
  }
})














