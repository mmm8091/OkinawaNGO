import { createHash } from "node:crypto";
import {
  createReadStream,
  realpathSync,
  readFileSync,
  statSync,
} from "node:fs";
import {
  dirname,
  isAbsolute,
  relative,
  resolve,
} from "node:path";

const PUBLICATION_NAMESPACES = [
  "core/",
  "exhibits/",
  "research/",
  "views/",
];

const contentTypeFor = (path) => {
  if (path.endsWith(".geojson")) {
    return "application/geo+json; charset=utf-8";
  }
  if (path.endsWith(".json")) {
    return "application/json; charset=utf-8";
  }
  if (path.endsWith(".md")) {
    return "text/markdown; charset=utf-8";
  }
  return "application/octet-stream";
};

const normalizedBasePath = (basePath) => {
  const withLeadingSlash = `/${String(basePath || "/").replace(/^\/+/, "")}`;
  return withLeadingSlash.endsWith("/")
    ? withLeadingSlash
    : `${withLeadingSlash}/`;
};

const pathInside = (parent, child) => {
  const childRelative = relative(parent, child);
  return (
    childRelative === "" ||
    (!isAbsolute(childRelative) &&
      childRelative !== ".." &&
      !childRelative.startsWith(`..\\`) &&
      !childRelative.startsWith("../"))
  );
};

const isPublicationRequest = (path) =>
  path === "manifest.json" ||
  path === "checksums.json" ||
  PUBLICATION_NAMESPACES.some((prefix) => path.startsWith(prefix));

export function loadVerifiedPublicationChannel({
  expectedProfile,
  projectRoot,
}) {
  const channelPath = resolve(
    projectRoot,
    "outputs",
    "publication_channels_v1",
    `${expectedProfile}.json`,
  );
  const channel = JSON.parse(readFileSync(channelPath, "utf8"));
  if (
    channel.schema_version !== "publication_channel_v1" ||
    channel.channel !== expectedProfile ||
    channel.profile !== expectedProfile
  ) {
    throw new Error("Publication channel profile mismatch");
  }
  if (
    typeof channel.release_id !== "string" ||
    !/^[A-Za-z0-9._-]+$/.test(channel.release_id)
  ) {
    throw new Error("Publication channel release ID is unsafe");
  }

  const snapshotRoot = resolve(projectRoot, channel.snapshot_path);
  const expectedSnapshotRoot = resolve(
    projectRoot,
    "outputs",
    "publication_releases_v1",
    expectedProfile,
    channel.release_id,
  );
  if (snapshotRoot !== expectedSnapshotRoot) {
    throw new Error("Publication snapshot path does not match the release ID");
  }
  if (
    !pathInside(realpathSync(projectRoot), realpathSync(snapshotRoot))
  ) {
    throw new Error("Publication snapshot path escapes the project root");
  }

  const manifestPath = resolve(snapshotRoot, "manifest.json");
  if (!pathInside(snapshotRoot, manifestPath)) {
    throw new Error("Publication manifest path escapes the snapshot");
  }
  const manifestBytes = readFileSync(manifestPath);
  const manifestHash = createHash("sha256")
    .update(manifestBytes)
    .digest("hex");
  const manifest = JSON.parse(manifestBytes.toString("utf8"));
  if (manifestHash !== channel.manifest_sha256) {
    throw new Error("Publication channel manifest hash mismatch");
  }
  if (
    manifest.release_id !== channel.release_id ||
    manifest.release_profile !== expectedProfile ||
    manifest.public !== true
  ) {
    throw new Error("Publication channel release metadata mismatch");
  }
  if (
    manifest.output_hashes == null ||
    typeof manifest.output_hashes !== "object" ||
    Array.isArray(manifest.output_hashes)
  ) {
    throw new Error("Publication manifest output allowlist is missing");
  }

  return {
    allowedPaths: new Set([
      ...Object.keys(manifest.output_hashes),
      "checksums.json",
      "manifest.json",
    ]),
    channel,
    manifest,
    snapshotRoot,
  };
}

const sendJsonError = (response, statusCode, code) => {
  response.statusCode = statusCode;
  response.setHeader("Cache-Control", "no-store");
  response.setHeader("Content-Type", "application/json; charset=utf-8");
  response.end(`${JSON.stringify({ error: code })}\n`);
};

export function createPublicationDevMiddleware({
  basePath = "/",
  publication,
}) {
  const base = normalizedBasePath(basePath);
  return (request, response, next) => {
    if (request.method !== "GET" && request.method !== "HEAD") {
      next();
      return;
    }

    let pathname;
    try {
      pathname = new URL(request.url || "/", "http://localhost").pathname;
      if (base !== "/") {
        if (!pathname.startsWith(base)) {
          next();
          return;
        }
        pathname = `/${pathname.slice(base.length)}`;
      }
      pathname = decodeURIComponent(pathname).replace(/^\/+/, "");
    } catch {
      sendJsonError(response, 400, "invalid_publication_path");
      return;
    }

    if (!isPublicationRequest(pathname)) {
      next();
      return;
    }
    if (
      pathname.includes("\\") ||
      pathname.split("/").some((part) => part === "..")
    ) {
      sendJsonError(response, 403, "unsafe_publication_path");
      return;
    }

    if (!publication.allowedPaths.has(pathname)) {
      sendJsonError(response, 404, "publication_file_not_in_release");
      return;
    }

    const filePath = resolve(
      publication.snapshotRoot,
      ...pathname.split("/"),
    );
    if (!pathInside(publication.snapshotRoot, filePath)) {
      sendJsonError(response, 403, "unsafe_publication_path");
      return;
    }

    let stat;
    try {
      stat = statSync(filePath);
    } catch {
      sendJsonError(response, 404, "publication_file_missing");
      return;
    }
    if (!stat.isFile()) {
      sendJsonError(response, 404, "publication_file_missing");
      return;
    }

    response.statusCode = 200;
    response.setHeader("Cache-Control", "no-store");
    response.setHeader("Content-Length", String(stat.size));
    response.setHeader("Content-Type", contentTypeFor(pathname));
    response.setHeader(
      "X-Publication-Release",
      publication.channel.release_id,
    );
    if (request.method === "HEAD") {
      response.end();
      return;
    }
    const stream = createReadStream(filePath);
    stream.on("error", () => {
      if (!response.headersSent) {
        sendJsonError(response, 500, "publication_file_read_failed");
      } else {
        response.destroy();
      }
    });
    stream.pipe(response);
  };
}

export function createPublicationChannelChangeHandler({
  currentReleaseId,
  debounceMs = 75,
  expectedProfile,
  projectRoot,
  restart,
  warn = () => {},
}) {
  const channelPath = resolve(
    projectRoot,
    "outputs",
    "publication_channels_v1",
    `${expectedProfile}.json`,
  );
  let disposed = false;
  let restartPending = false;
  let timer = null;

  const check = async () => {
    timer = null;
    if (disposed || restartPending) return;
    let active;
    try {
      active = loadVerifiedPublicationChannel({
        expectedProfile,
        projectRoot,
      });
    } catch {
      warn("Publication channel change could not be verified; keeping current release.");
      return;
    }
    if (active.channel.release_id === currentReleaseId) return;
    restartPending = true;
    try {
      await restart();
    } finally {
      restartPending = false;
    }
  };

  return {
    channelPath,
    dispose() {
      disposed = true;
      if (timer) clearTimeout(timer);
      timer = null;
    },
    notify(changedPath) {
      if (resolve(changedPath) !== channelPath || disposed) return;
      if (timer) clearTimeout(timer);
      timer = setTimeout(check, debounceMs);
    },
  };
}

export function publicationDevPlugin({
  basePath,
  expectedProfile,
  projectRoot,
  publication,
}) {
  return {
    apply: "serve",
    configureServer(server) {
      server.middlewares.use(
        createPublicationDevMiddleware({
          basePath,
          publication,
        }),
      );
      const controller = createPublicationChannelChangeHandler({
        currentReleaseId: publication.channel.release_id,
        expectedProfile,
        projectRoot,
        restart: () => server.restart(),
        warn: (message) => server.config.logger.warn(message),
      });
      const onChannelEvent = (_event, changedPath) =>
        controller.notify(changedPath);
      server.watcher.add(dirname(controller.channelPath));
      server.watcher.on("all", onChannelEvent);
      server.httpServer?.once("close", () => {
        controller.dispose();
        server.watcher.off("all", onChannelEvent);
      });
    },
    name: "nr3-active-publication-channel",
  };
}
