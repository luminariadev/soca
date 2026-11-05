<script setup lang="ts">
import SocaLogo from './SocaLogo.vue';

const props = defineProps<{
  historyCount: number;
  sidebarCollapsed: boolean;
}>();

const emit = defineEmits<{
  (e: 'toggleSidebar'): void;
  (e: 'openHistory'): void;
  (e: 'openAbout'): void;
}>();
</script>

<template>
  <header
    class="sticky top-0 z-30 h-16 w-full bg-surface-container-lowest/90 backdrop-blur-2xl border-b border-outline-variant/30 px-3 sm:px-6 flex items-center justify-between shrink-0"
  >
    <!-- Left: Desktop-Only Sidebar Toggle & Brand Title -->
    <div class="flex items-center gap-2.5 sm:gap-4 min-w-0">
      <!-- Desktop Sidebar Toggle (Hidden on mobile where bottom navbar is used) -->
      <button
        @click="emit('toggleSidebar')"
        class="hidden md:flex w-9 h-9 rounded-xl bg-surface-container hover:bg-surface-container-high text-on-surface border border-outline-variant/40 items-center justify-center transition-all hover:scale-105 active:scale-95 shadow-sm shrink-0"
        :title="sidebarCollapsed ? 'Perluas Sidebar' : 'Ciutkan Sidebar'"
      >
        <span class="material-symbols-outlined text-[20px] text-primary">
          {{ sidebarCollapsed ? 'dock_to_right' : 'dock_to_left' }}
        </span>
      </button>

      <!-- macOS window indicator dots (Hidden on mobile) -->
      <div class="hidden sm:flex items-center gap-1.5 pl-0.5">
        <span class="w-3 h-3 rounded-full bg-[#FF5F56] shadow-[inset_0_0_0_1px_rgba(0,0,0,0.15)]"></span>
        <span class="w-3 h-3 rounded-full bg-[#FFBD2E] shadow-[inset_0_0_0_1px_rgba(0,0,0,0.15)]"></span>
        <span class="w-3 h-3 rounded-full bg-[#27C93F] shadow-[inset_0_0_0_1px_rgba(0,0,0,0.15)]"></span>
      </div>

      <!-- App Title & Telemetry -->
      <div class="flex items-center gap-2.5 min-w-0">
        <div class="md:hidden shrink-0">
          <SocaLogo :size="30" />
        </div>
        <div class="flex flex-col min-w-0">
          <div class="flex items-center gap-2">
            <span class="font-extrabold text-on-surface tracking-tight text-sm sm:text-base truncate">
              SOCA <span class="text-primary font-normal text-xs sm:text-sm">• Ocularis AI</span>
            </span>
            <span class="hidden md:inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-primary-container/20 text-primary-fixed text-[11px] font-mono font-medium">
              <span class="w-1.5 h-1.5 rounded-full bg-tertiary animate-pulse"></span>
              97.99% Val Acc
            </span>
          </div>
          <span class="text-[11px] font-mono text-on-surface-variant hidden sm:inline truncate">
            Non-Retinal Anterior Eye Screening • 7 Biological Conditions
          </span>
        </div>
      </div>
    </div>

    <!-- Right: Clean Purposeful Actions (About Developer & History Sessions) -->
    <div class="flex items-center gap-2 shrink-0">
      <!-- About Developer Button (Bisa diakses di Mobile dan Desktop) -->
      <button
        @click="emit('openAbout')"
        class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-surface-container hover:bg-surface-container-high text-on-surface border border-outline-variant/40 transition-all shadow-sm active:scale-95"
        title="Tentang Pengembang (Rizkia Nuari) & Aplikasi"
      >
        <span class="material-symbols-outlined text-[18px] text-primary">help</span>
        <span class="text-xs font-semibold hidden sm:inline">Tentang</span>
      </button>

      <!-- History Counter Button -->
      <button
        @click="emit('openHistory')"
        class="relative flex items-center gap-2 px-3 py-1.5 rounded-xl bg-surface-container hover:bg-surface-container-high text-on-surface border border-outline-variant/40 transition-all shadow-sm active:scale-95"
        title="Riwayat Sesi Skrining"
      >
        <span class="material-symbols-outlined text-[18px] text-primary">history</span>
        <span class="text-xs font-semibold hidden sm:inline">Riwayat</span>
        <span
          v-if="historyCount > 0"
          class="w-5 h-5 rounded-full bg-primary-container text-on-primary-container text-[10px] font-bold flex items-center justify-center font-mono animate-bounce"
        >
          {{ historyCount }}
        </span>
      </button>
    </div>
  </header>
</template>
