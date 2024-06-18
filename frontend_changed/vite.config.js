import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  "base": "simplitrac/frontend_changed/",
  plugins: [react()],
})
