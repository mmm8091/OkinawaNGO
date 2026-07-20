import assert from "node:assert/strict";
import test from "node:test";

import { labelOf, localizedFieldOf } from "../src/lib/display_text.js";

test("episode display fields select the requested language", () => {
  const episode = {
    display_label: "中央原文",
    display_label_zh: "中央原文",
    display_label_ja: "日本語",
    display_label_en: "English",
    local_problem: "基础文本",
    local_problem_en: "Base text",
  };

  assert.equal(labelOf(episode, "ja"), "日本語");
  assert.equal(localizedFieldOf(episode, "local_problem", "en"), "Base text");
});

test("episode display fields safely fall back to the unchanged source text", () => {
  const episode = {
    display_label: "中央原文",
    display_label_ja: "",
    local_problem: "基础文本",
  };

  assert.equal(labelOf(episode, "ja"), "中央原文");
  assert.equal(localizedFieldOf(episode, "local_problem", "en"), "基础文本");
  assert.equal(localizedFieldOf(null, "local_problem", "en"), "");
});
