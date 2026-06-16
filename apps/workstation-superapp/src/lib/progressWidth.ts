/**
 * Maps a 0-100 percentage to a literal Tailwind width class, snapped to the
 * nearest 5%. Used for data-driven progress bars so callers never need an
 * inline `style={{ width: ... }}` — every class below is a literal string
 * Tailwind's content scanner can discover at build time.
 */
const WIDTH_CLASSES: Record<number, string> = {
  0: 'w-[0%]', 5: 'w-[5%]', 10: 'w-[10%]', 15: 'w-[15%]', 20: 'w-[20%]',
  25: 'w-[25%]', 30: 'w-[30%]', 35: 'w-[35%]', 40: 'w-[40%]', 45: 'w-[45%]',
  50: 'w-[50%]', 55: 'w-[55%]', 60: 'w-[60%]', 65: 'w-[65%]', 70: 'w-[70%]',
  75: 'w-[75%]', 80: 'w-[80%]', 85: 'w-[85%]', 90: 'w-[90%]', 95: 'w-[95%]',
  100: 'w-[100%]',
};

export function progressWidthClass(percent: number): string {
  const clamped = Math.max(0, Math.min(100, percent));
  const snapped = Math.round(clamped / 5) * 5;
  return WIDTH_CLASSES[snapped] ?? 'w-[0%]';
}

/**
 * Maps a pixel height to the nearest literal Tailwind height class from a
 * fixed set of steps (Tailwind's own 4px-multiple spacing scale), so a
 * draggable resize handle can adjust element height without ever using an
 * inline `style={{ height }}`.
 */
const HEIGHT_STEPS: { px: number; cls: string }[] = [
  { px: 80, cls: 'h-20' }, { px: 96, cls: 'h-24' }, { px: 112, cls: 'h-28' },
  { px: 128, cls: 'h-32' }, { px: 144, cls: 'h-36' }, { px: 160, cls: 'h-40' },
  { px: 176, cls: 'h-44' }, { px: 192, cls: 'h-48' }, { px: 208, cls: 'h-52' },
  { px: 224, cls: 'h-56' }, { px: 240, cls: 'h-60' }, { px: 256, cls: 'h-64' },
  { px: 288, cls: 'h-72' }, { px: 320, cls: 'h-80' }, { px: 384, cls: 'h-96' },
];

export function heightClass(px: number): string {
  const clamped = Math.max(HEIGHT_STEPS[0].px, Math.min(HEIGHT_STEPS[HEIGHT_STEPS.length - 1].px, px));
  let nearest = HEIGHT_STEPS[0];
  let bestDiff = Infinity;
  for (const step of HEIGHT_STEPS) {
    const diff = Math.abs(step.px - clamped);
    if (diff < bestDiff) {
      bestDiff = diff;
      nearest = step;
    }
  }
  return nearest.cls;
}

export const FOOTER_MIN_HEIGHT_PX = HEIGHT_STEPS[0].px;
export const FOOTER_MAX_HEIGHT_PX = HEIGHT_STEPS[HEIGHT_STEPS.length - 1].px;

/**
 * Same snapping idea as `heightClass`, but for a draggable column *width*
 * (the far-right Workstation dock) — literal `w-N` classes only.
 */
const WIDTH_PX_STEPS: { px: number; cls: string }[] = [
  { px: 56, cls: 'w-14' }, { px: 64, cls: 'w-16' }, { px: 80, cls: 'w-20' },
  { px: 96, cls: 'w-24' }, { px: 112, cls: 'w-28' }, { px: 128, cls: 'w-32' },
  { px: 144, cls: 'w-36' }, { px: 160, cls: 'w-40' }, { px: 176, cls: 'w-44' },
  { px: 192, cls: 'w-48' }, { px: 208, cls: 'w-52' }, { px: 224, cls: 'w-56' },
  { px: 240, cls: 'w-60' }, { px: 256, cls: 'w-64' }, { px: 288, cls: 'w-72' },
  { px: 320, cls: 'w-80' }, { px: 384, cls: 'w-96' },
];

export function widthPxClass(px: number): string {
  const clamped = Math.max(WIDTH_PX_STEPS[0].px, Math.min(WIDTH_PX_STEPS[WIDTH_PX_STEPS.length - 1].px, px));
  let nearest = WIDTH_PX_STEPS[0];
  let bestDiff = Infinity;
  for (const step of WIDTH_PX_STEPS) {
    const diff = Math.abs(step.px - clamped);
    if (diff < bestDiff) {
      bestDiff = diff;
      nearest = step;
    }
  }
  return nearest.cls;
}

export const RIGHT_DOCK_COLLAPSED_PX = WIDTH_PX_STEPS[0].px; // 56
export const RIGHT_DOCK_MIN_PX = 240;
export const RIGHT_DOCK_MAX_PX = 384;

/**
 * Maps a 0-100 percentage to a literal Tailwind *height*-percent class,
 * snapped to the nearest 5% — the `h-[X%]` sibling of `progressWidthClass`.
 * Used for real-time audio-amplitude bars so they never need inline styles.
 */
const HEIGHT_PERCENT_CLASSES: Record<number, string> = {
  0: 'h-[0%]', 5: 'h-[5%]', 10: 'h-[10%]', 15: 'h-[15%]', 20: 'h-[20%]',
  25: 'h-[25%]', 30: 'h-[30%]', 35: 'h-[35%]', 40: 'h-[40%]', 45: 'h-[45%]',
  50: 'h-[50%]', 55: 'h-[55%]', 60: 'h-[60%]', 65: 'h-[65%]', 70: 'h-[70%]',
  75: 'h-[75%]', 80: 'h-[80%]', 85: 'h-[85%]', 90: 'h-[90%]', 95: 'h-[95%]',
  100: 'h-[100%]',
};

export function heightPercentClass(percent: number): string {
  const clamped = Math.max(0, Math.min(100, percent));
  const snapped = Math.round(clamped / 5) * 5;
  return HEIGHT_PERCENT_CLASSES[snapped] ?? 'h-[0%]';
}
