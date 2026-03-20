import { defineConfig } from 'vite'
import { readdirSync } from 'node:fs'
import { basename, extname } from 'node:path'

const srcDir = new URL('./src/', import.meta.url)
const input = Object.fromEntries(
  readdirSync(srcDir)
    .filter((file) => extname(file) === '.ts')
    .map((file) => [basename(file, '.ts'), new URL(file, srcDir).pathname])
)

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
  },
  build: {
    outDir: 'assets',
    emptyOutDir: false,
    rollupOptions: {
      input,
      output: {
        entryFileNames: '[name].js'
      }
    }
  }
})