import { fileURLToPath, URL } from 'node:url'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { ViteWebfontDownload } from 'vite-plugin-webfont-dl'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({
      dts: './components.d.ts'
    }),
    AutoImport({
      imports: [
        // presets
        'vue',
        'vue-router',
      ],
      dirs: [
        './src/utils/**',
        './src/composables/**',
      ],
      dts: './auto-import.d.ts'
    }),
    ViteWebfontDownload([
      'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+JP:wght@100;300;400;700&display=swap',
      'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200'
    ])
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
