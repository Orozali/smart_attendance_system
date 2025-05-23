import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: '0.0.0.0',           // force external access (required)
    port: 5174,
    strictPort: true,
    open: false,
    allowedHosts: [
      'fd9a-178-217-174-2.ngrok-free.app'
    ],
    cors: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
    }
  },  
});
