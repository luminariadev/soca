<script setup lang="ts">
const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();
</script>

<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-[80] bg-black/80 backdrop-blur-xl flex flex-col justify-end sm:justify-center sm:items-center p-0 sm:p-6 transition-all"
    @click.self="emit('close')"
  >
    <!-- Responsive Sheet / Dialog: Mobile Bottom Sheet (iOS Style) & Desktop Centered Card -->
    <div
      class="relative w-full max-w-xl rounded-t-[32px] sm:rounded-3xl bg-surface-container/95 border-t sm:border border-outline-variant/40 backdrop-blur-2xl shadow-[0_-16px_48px_rgba(0,0,0,0.85)] sm:shadow-[0_32px_80px_rgba(0,0,0,0.85)] p-5 sm:p-8 flex flex-col gap-4 sm:gap-5 max-h-[88vh] overflow-y-auto sm:my-auto"
    >
      <!-- Mobile Pull / Drag Indicator Bar (iOS Bottom Sheet Style) -->
      <div class="w-12 h-1.5 rounded-full bg-white/25 mx-auto mb-1 sm:hidden shrink-0"></div>

      <!-- Ambient glow effect -->
      <div class="absolute -top-12 -left-12 w-48 h-48 bg-primary/20 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Header with Avatar & Close -->
      <div class="flex items-start justify-between">
        <div class="flex items-center gap-3.5">
          <div class="w-13 h-13 sm:w-14 sm:h-14 rounded-2xl bg-gradient-to-tr from-primary-container to-secondary-container flex items-center justify-center text-white text-2xl font-bold shadow-lg ring-2 ring-primary/30 shrink-0">
            R
          </div>
          <div class="flex flex-col">
            <h3 class="font-bold text-on-surface text-lg sm:text-xl">Rizkia Nuari Fujiana</h3>
            <p class="text-primary font-mono text-xs">@luminariadev • Fullstack & AI Engineer</p>
          </div>
        </div>

        <button
          @click="emit('close')"
          class="w-8 h-8 rounded-full bg-surface-container-high hover:bg-surface-bright flex items-center justify-center text-on-surface-variant hover:text-on-surface transition-colors shrink-0"
          title="Tutup Modal"
        >
          <span class="material-symbols-outlined text-[18px]">close</span>
        </button>
      </div>

      <!-- About Description -->
      <div class="flex flex-col gap-2.5 text-xs sm:text-sm text-on-surface-variant leading-relaxed">
        <p>
          <strong class="text-on-surface">SOCA (Smart Ocular Condition Analyzer)</strong> adalah platform skrining klinis cerdas berbasis visi komputer non-invasif yang dikembangkan untuk mendeteksi kondisi dan anomali pada <strong class="text-primary">mata bagian luar</strong> secara *real-time* via kamera standar laptop dan ponsel pintar.
        </p>
        <p>
          Sistem ini melatih arsitektur <strong class="text-on-surface">MobileNetV2 terkalibrasi</strong> pada <strong class="text-tertiary">3.988 citra mata nyata</strong> dan mencapai benchmark akurasi validasi <strong class="text-tertiary">97.99%</strong> dengan F1-Score 0.98 di seluruh 7 kondisi biologis.
        </p>
      </div>

      <!-- Tech Stack Badges -->
      <div class="flex flex-col gap-2">
        <span class="text-[11px] font-mono uppercase tracking-wider text-on-surface font-semibold">Spesifikasi Arsitektur Sistem:</span>
        <div class="flex flex-wrap gap-1.5 sm:gap-2">
          <span class="px-2.5 py-1 rounded-lg bg-surface-container-high text-xs font-mono text-primary border border-outline-variant/30">
            Vue 3 + Vite
          </span>
          <span class="px-2.5 py-1 rounded-lg bg-surface-container-high text-xs font-mono text-primary border border-outline-variant/30">
            TypeScript
          </span>
          <span class="px-2.5 py-1 rounded-lg bg-surface-container-high text-xs font-mono text-primary border border-outline-variant/30">
            Tailwind CSS
          </span>
          <span class="px-2.5 py-1 rounded-lg bg-surface-container-high text-xs font-mono text-tertiary border border-outline-variant/30">
            PyTorch 2.5 (CUDA 12.1)
          </span>
          <span class="px-2.5 py-1 rounded-lg bg-surface-container-high text-xs font-mono text-secondary border border-outline-variant/30">
            MediaPipe Face Mesh
          </span>
          <span class="px-2.5 py-1 rounded-lg bg-surface-container-high text-xs font-mono text-on-surface border border-outline-variant/30">
            Vercel Ready
          </span>
        </div>
      </div>

      <!-- Creator Links & Portfolio -->
      <div class="p-3.5 sm:p-4 rounded-2xl bg-surface-container-low border border-outline-variant/30 flex flex-col gap-2.5">
        <span class="text-xs font-semibold text-on-surface">Tautan Resmi Pengembang:</span>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <a
            href="https://rizkianuari.vercel.app/"
            target="_blank"
            class="flex items-center gap-2 p-2.5 rounded-xl bg-surface-container-high hover:bg-surface-bright text-xs font-medium text-primary transition-all border border-primary/20 active:scale-95"
          >
            <span class="material-symbols-outlined text-[16px]">language</span>
            <span>My Portofolio</span>
          </a>
          <a
            href="https://github.com/luminariadev"
            target="_blank"
            class="flex items-center gap-2 p-2.5 rounded-xl bg-surface-container-high hover:bg-surface-bright text-xs font-medium text-on-surface transition-all border border-outline-variant/30 active:scale-95"
          >
            <span class="material-symbols-outlined text-[16px]">code</span>
            <span>GitHub Profile</span>
          </a>
        </div>
      </div>

      <!-- Footer Button -->
      <div class="flex justify-end pt-1 pb-4 sm:pb-0">
        <button
          @click="emit('close')"
          class="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-primary-container text-white font-semibold text-xs sm:text-sm hover:brightness-110 active:scale-95 transition-all shadow-md"
        >
          Tutup
        </button>
      </div>
    </div>
  </div>
</template>
