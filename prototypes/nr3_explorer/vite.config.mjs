import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

import {
  loadVerifiedPublicationChannel,
  publicationDevPlugin,
} from "./dev_publication_middleware.mjs";

const projectRoot = resolve(import.meta.dirname, "../..");
const profile = "client_preview";
const basePath = process.env.VITE_BASE_PATH || "/";

export default defineConfig(() => {
  const publication = loadVerifiedPublicationChannel({
    expectedProfile: profile,
    projectRoot,
  });
  return {
    base: basePath,
    // Every server/build generation is pinned to one verified immutable
    // release. In development, a channel change restarts Vite and creates a
    // new generation rather than mixing rows from two releases.
    publicDir: publication.snapshotRoot,
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
    plugins: [
      publicationDevPlugin({
        basePath,
        expectedProfile: profile,
        projectRoot,
        publication,
      }),
      react(),
    ],
  };
});
