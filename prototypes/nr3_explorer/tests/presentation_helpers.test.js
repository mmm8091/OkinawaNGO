import assert from "node:assert/strict";
import test from "node:test";

import {
  actorClassGroup,
  actorClassMeta,
  placeDisplayRegion,
  regionMeta,
} from "../src/lib/data.js";

const presentation = {
  actor_class_to_group: { citizen_group: "civic" },
  actor_class_groups: [
    { id: "civic", color: "#123456" },
    { id: "unknown", color: "#999999" },
  ],
  regions: [{ id: "miyako", color: "#abcdef" }],
  place_display_regions: { P013: "miyako" },
  default_place_display_region: "okinawa",
};

test("actor classes and colors come from the presentation contract", () => {
  assert.equal(actorClassGroup("citizen_group", presentation), "civic");
  assert.equal(actorClassMeta("citizen_group", presentation).color, "#123456");
  assert.equal(actorClassGroup("unmapped", presentation), "unknown");
  assert.equal(actorClassMeta("unmapped", presentation).color, "#999999");
});

test("place display regions and region colors come from the presentation contract", () => {
  assert.equal(placeDisplayRegion({ id: "P013" }, presentation), "miyako");
  assert.equal(placeDisplayRegion({ id: "P999" }, presentation), "okinawa");
  assert.equal(regionMeta("miyako", presentation).color, "#abcdef");
});
