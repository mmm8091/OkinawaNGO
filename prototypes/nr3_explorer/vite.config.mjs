import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { relative, resolve } from "node:path";

const projectRoot = resolve(import.meta.dirname, "../..");
const publicationChannel = JSON.parse(
  readFileSync(
    resolve(projectRoot, "outputs/publication_channels_v1/client_preview.json"),
    "utf8",
  ),
);
const publicationRoot = resolve(projectRoot, publicationChannel.snapshot_path);
const publicationRelative = relative(projectRoot, publicationRoot);
if (
  publicationRelative.startsWith("..") ||
  publicationChannel.profile !== "client_preview"
) {
  throw new Error("Unsafe or non-client publication channel");
}
const publicationManifestPath = resolve(publicationRoot, "manifest.json");
const publicationManifestBytes = readFileSync(publicationManifestPath);
const publicationManifest = JSON.parse(publicationManifestBytes.toString("utf8"));
const manifestHash = createHash("sha256")
  .update(publicationManifestBytes)
  .digest("hex");
if (
  publicationManifest.release_id !== publicationChannel.release_id ||
  publicationManifest.release_profile !== publicationChannel.profile ||
  publicationManifest.public !== true ||
  manifestHash !== publicationChannel.manifest_sha256
) {
  throw new Error("Publication channel failed release/profile/hash verification");
}

export default defineConfig({
  base: process.env.VITE_BASE_PATH || "/",
  publicDir: publicationRoot,
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
