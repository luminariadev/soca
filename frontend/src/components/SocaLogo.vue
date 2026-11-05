<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    size?: number;
  }>(),
  {
    size: 40
  }
);
</script>

<template>
  <div
    class="relative inline-flex items-center justify-center shrink-0 select-none"
    :style="{ width: `${size}px`, height: `${size}px` }"
  >
    <svg
      :width="size"
      :height="size"
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      class="w-full h-full"
    >
      <!-- Deep Obsidian Shield Container -->
      <rect width="100" height="100" rx="24" fill="#0C1322" stroke="#1E293B" stroke-width="2" />

      <!-- Surgical Blue Subtle Radial Backlight -->
      <circle cx="50" cy="50" r="34" fill="#0284C7" fill-opacity="0.12" />

      <!-- Natural Human Palpebral Contour (Continuous Surgical Arc) -->
      <path
        d="M 16 50 C 28 26, 72 26, 84 50 C 72 74, 28 74, 16 50 Z"
        fill="#080E1A"
        stroke="#38BDF8"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
      />

      <!-- Slit-Lamp Cornea Inner Horizon -->
      <path
        d="M 23 50 C 32 32, 68 32, 77 50 C 68 68, 32 68, 23 50 Z"
        fill="none"
        stroke="#1E3A8A"
        stroke-width="1.2"
        stroke-dasharray="3 3"
      />

      <!-- Iris Disc (Clinical Cobalt Stroma) -->
      <circle cx="50" cy="50" r="18" fill="#0369A1" stroke="#38BDF8" stroke-width="1.8" />
      <circle cx="50" cy="50" r="14" fill="#0284C7" stroke="#7DD3FC" stroke-width="0.75" stroke-dasharray="2 3" />

      <!-- Central Pupil Aperture (Dark Onyx) -->
      <circle cx="50" cy="50" r="8" fill="#020617" />

      <!-- Natural Corneal Light Reflex (Anterior Specular Reflection) -->
      <circle cx="46.5" cy="46.5" r="2.8" fill="#FFFFFF" />
      <circle cx="53" cy="53" r="1.3" fill="#BAE6FD" />

      <!-- Subtle Minimal Medical Crosshair Markers (Clean Surgical Axis) -->
      <line x1="50" y1="20" x2="50" y2="24" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
      <line x1="50" y1="76" x2="50" y2="80" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
      <line x1="20" y1="50" x2="24" y2="50" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
      <line x1="76" y1="50" x2="80" y2="50" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
    </svg>
  </div>
</template>
