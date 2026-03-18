import { defineConfig } from 'vite'

export default defineConfig({
  root: 'html', // critical: serve generated HTML
  resolve: {
    alias: {
      '/src': new URL('./src', import.meta.url).pathname
    }
  },
  server: {
    port: 5173,
    strictPort: true,
    fs: {
      allow: ['..'] // allow access to src outside html/
    }
  },
  build: {
    outDir: 'html/assets',
    emptyOutDir: false,
    rollupOptions: {
      input: {
        main: new URL('./src/main.ts', import.meta.url).pathname
      },
      output: {
        entryFileNames: 'bundle.js'
      }
    }
  }
})