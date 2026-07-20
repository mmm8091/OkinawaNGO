import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import { dirname, join, relative, sep } from "node:path";
import test from "node:test";

import {
  createPublicationChannelChangeHandler,
  createPublicationDevMiddleware,
  loadVerifiedPublicationChannel,
} from "../dev_publication_middleware.mjs";

const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

const writeJson = (path, value) => {
  mkdirSync(dirname(path), { recursive: true });
  const bytes = `${JSON.stringify(value, null, 2)}\n`;
  writeFileSync(path, bytes, "utf8");
  return bytes;
};

const makeRelease = (projectRoot, releaseId, marker) => {
  const snapshotRoot = join(
    projectRoot,
    "outputs",
    "publication_releases_v1",
    "client_preview",
    releaseId,
  );
  const payload = writeJson(join(snapshotRoot, "core", "value.json"), {
    release_id: releaseId,
    marker,
  });
  const manifestBytes = writeJson(join(snapshotRoot, "manifest.json"), {
    release_id: releaseId,
    release_profile: "client_preview",
    public: true,
    output_hashes: {
      "core/value.json": sha256(payload),
    },
  });
  return {
    manifestHash: sha256(manifestBytes),
    releaseId,
    snapshotRoot,
  };
};

const switchChannel = (projectRoot, release) => {
  const snapshotPath = relative(projectRoot, release.snapshotRoot)
    .split(sep)
    .join("/");
  writeJson(
    join(
      projectRoot,
      "outputs",
      "publication_channels_v1",
      "client_preview.json",
    ),
    {
      channel: "client_preview",
      manifest_sha256: release.manifestHash,
      profile: "client_preview",
      release_id: release.releaseId,
      schema_version: "publication_channel_v1",
      snapshot_path: snapshotPath,
    },
  );
};

const listen = (server) =>
  new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", () => resolve(server.address()));
  });

const close = (server) =>
  new Promise((resolve, reject) => {
    server.closeIdleConnections?.();
    server.closeAllConnections?.();
    server.close((error) => (error ? reject(error) : resolve()));
  });

test("one dev-server generation stays pinned to one publication release", async (t) => {
  const projectRoot = mkdtempSync(join(tmpdir(), "nr3-publication-dev-"));
  t.after(() => rmSync(projectRoot, { recursive: true, force: true }));
  const releaseA = makeRelease(projectRoot, "client_preview-a", "A");
  const releaseB = makeRelease(projectRoot, "client_preview-b", "B");
  switchChannel(projectRoot, releaseA);

  const publicationA = loadVerifiedPublicationChannel({
    expectedProfile: "client_preview",
    projectRoot,
  });
  const middleware = createPublicationDevMiddleware({
    basePath: "/",
    publication: publicationA,
  });
  const server = createServer((request, response) =>
    middleware(request, response, () => {
      response.statusCode = 404;
      response.end("not found");
    }),
  );
  t.after(() => close(server));
  const address = await listen(server);
  const url = `http://127.0.0.1:${address.port}/core/value.json`;

  const first = await fetch(url).then((response) => response.json());
  assert.equal(first.marker, "A");

  switchChannel(projectRoot, releaseB);
  const second = await fetch(url).then((response) => response.json());
  assert.equal(second.marker, "A");

  const missing = await fetch(
    `http://127.0.0.1:${address.port}/core/missing.json`,
  );
  assert.equal(missing.status, 404);
  assert.match(missing.headers.get("content-type"), /application\/json/);
  assert.deepEqual(await missing.json(), {
    error: "publication_file_not_in_release",
  });
});

test("a verified channel change schedules one Vite restart", async () => {
  const projectRoot = mkdtempSync(join(tmpdir(), "nr3-publication-watch-"));
  try {
    const releaseA = makeRelease(projectRoot, "client_preview-a", "A");
    const releaseB = makeRelease(projectRoot, "client_preview-b", "B");
    switchChannel(projectRoot, releaseA);
    let restarts = 0;
    let controller;
    controller = createPublicationChannelChangeHandler({
      currentReleaseId: releaseA.releaseId,
      debounceMs: 5,
      expectedProfile: "client_preview",
      projectRoot,
      restart: async () => {
        restarts += 1;
        controller.dispose();
      },
    });

    controller.notify(controller.channelPath);
    await new Promise((resolve) => setTimeout(resolve, 20));
    assert.equal(restarts, 0);

    switchChannel(projectRoot, releaseB);
    controller.notify(controller.channelPath);
    controller.notify(controller.channelPath);
    await new Promise((resolve) => setTimeout(resolve, 30));
    assert.equal(restarts, 1);

    const publicationB = loadVerifiedPublicationChannel({
      expectedProfile: "client_preview",
      projectRoot,
    });
    assert.equal(publicationB.channel.release_id, releaseB.releaseId);
  } finally {
    rmSync(projectRoot, { recursive: true, force: true });
  }
});

test("channel verification rejects a stale or tampered manifest pointer", () => {
  const projectRoot = mkdtempSync(join(tmpdir(), "nr3-publication-verify-"));
  try {
    const release = makeRelease(projectRoot, "client_preview-a", "A");
    switchChannel(projectRoot, {
      ...release,
      manifestHash: "0".repeat(64),
    });
    assert.throws(
      () =>
        loadVerifiedPublicationChannel({
          expectedProfile: "client_preview",
          projectRoot,
        }),
      /manifest hash/i,
    );
  } finally {
    rmSync(projectRoot, { recursive: true, force: true });
  }
});
