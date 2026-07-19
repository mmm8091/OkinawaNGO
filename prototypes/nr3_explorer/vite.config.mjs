import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

export default defineConfig({
  publicDir: resolve(
    import.meta.dirname,
    "../../outputs/exploration_system_data_v1",
  ),
  optimizeDeps: {
    include: [
      "react",
      "react-dom/client",
      "@phosphor-icons/react",
      "d3-force",
      "d3-geo",
    ],
  },
  server: {
    host: "0.0.0.0",
    allowedHosts: ["terminal.local"],
    warmup: {
      clientFiles: ["./src/main.jsx"],
    },
  },
  plugins: [react()],
});
