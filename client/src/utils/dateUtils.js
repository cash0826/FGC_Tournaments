
// Converts input into a Date object. Accepts ISO Strings (1990-01-01T00:00:00) or Date instances
function toDate(value) {
  const d = value instanceof Date ? value : new Date(value)
  return isNaN(d.getTime()) ? null : d
}

// Returns long date (no time). Saturday, September 12, 2026
export function formatLongDate(value) {
  const date = toDate(value);
  if (!date) return "";

  return date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

// Returns long date + time
export function formatLongDateTime(value) {
  const date = toDate(value);
  if (!date) return "";

  const datePart = date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });

  const timePart = date.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
  });

  return `${datePart} at ${timePart}`
}