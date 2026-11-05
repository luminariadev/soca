<script setup lang="ts">
import type { TabType } from '../types';

const props = defineProps<{
  currentTab: TabType;
}>();

const emit = defineEmits<{
  (e: 'selectTab', tab: TabType): void;
}>();

const navItems: { id: TabType; label: string; icon: string }[] = [
  { id: 'beranda', label: 'Beranda', icon: 'grid_view' },
  { id: 'pindai', label: 'Pindai', icon: 'center_focus_strong' },
  { id: 'hasil', label: 'Hasil', icon: 'clinical_notes' },
  { id: 'edukasi', label: 'Edukasi', icon: 'menu_book' },
  { id: 'privasi', label: 'Privasi', icon: 'verified_user' }
];
</script>

<template>
  <!-- Floating iOS Liquid Glass Bottom Pill (Permintaan User: rounded glass/liquid ala Apple iOS) -->
  <nav class="md:hidden fixed bottom-4 left-4 right-4 max-w-md mx-auto h-16 bg-surface-container-low/75 backdrop-blur-2xl border border-white/10 rounded-full z-50 flex items-center justify-around px-2 shadow-[0_16px_40px_rgba(0,0,0,0.65)] ring-1 ring-white/15">
    <button
      v-for="item in navItems"
      :key="item.id"
      @click="emit('selectTab', item.id)"
      class="relative flex flex-col items-center justify-center flex-1 h-full py-1 rounded-full transition-all duration-200"
      :class="currentTab === item.id ? 'text-primary' : 'text-on-surface-variant hover:text-on-surface'"
    >
      <!-- Active Liquid Capsule Background -->
      <div
        v-if="currentTab === item.id"
        class="absolute inset-x-1.5 inset-y-1.5 rounded-full bg-primary-container/20 border border-primary/30 shadow-[0_0_12px_rgba(62,144,255,0.25)] -z-10"
      ></div>

      <span
        class="material-symbols-outlined text-[20px] transition-transform"
        :class="currentTab === item.id ? 'fill-1 scale-110 text-primary-fixed' : ''"
      >
        {{ item.icon }}
      </span>

      <span
        class="text-[10px] font-medium tracking-tight mt-0.5"
        :class="currentTab === item.id ? 'font-bold text-primary-fixed' : ''"
      >
        {{ item.label }}
      </span>

      <!-- Active Pulse Glow Dot -->
      <span
        v-if="currentTab === item.id"
        class="w-1 h-1 rounded-full bg-primary mt-0.5 shadow-[0_0_6px_rgba(170,199,255,1)]"
      ></span>
    </button>
  </nav>
</template>
