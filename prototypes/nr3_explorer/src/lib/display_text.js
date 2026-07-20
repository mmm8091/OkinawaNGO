// Presentation-only locale selection. The unsuffixed field is the unchanged
// source text and remains the final fallback for incomplete/older data packs.
export const localizedFieldOf = (object, field, lang = "zh") =>
  object?.[`${field}_${lang}`] || object?.[field] || "";

export const labelOf = (object, lang = "zh") =>
  localizedFieldOf(object, "display_label", lang);
