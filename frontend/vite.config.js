import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Proxies /webhook/* to the local n8n instance so the browser never makes a
// cross-origin request (avoids CORS entirely - same-origin as far as the
// browser is concerned, Vite forwards it server-side).
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/webhook': {
        target: 'http://localhost:5678',
        changeOrigin: true,
      },
    },
  },
})
