<script setup lang="ts">
import type { TabType } from '../types';
import SocaLogo from './SocaLogo.vue';

const props = defineProps<{
  currentTab: TabType;
  isCollapsed: boolean;
}>();

const emit = defineEmits<{
  (e: 'selectTab', tab: TabType): void;
  (e: 'openAbout'): void;
}>();

const navItems: { id: TabType; label: string; icon: string; badge?: string }[] = [
  { id: 'beranda', label: 'Beranda', icon: 'grid_view' },
  { id: 'pindai', label: 'Pemindaian AI', icon: 'center_focus_strong', badge: 'Live' },
  { id: 'hasil', label: 'Hasil & Rekomendasi', icon: 'clinical_notes' },
  { id: 'edukasi', label: 'Ensiklopedia Edukasi', icon: 'menu_book' },
  { id: 'privasi', label: 'Privasi & Disclaimer', icon: 'verified_user' }
];
</script>

<template>
  <aside
    class="hidden md:flex shrink-0 h-full bg-surface-container-low/95 backdrop-blur-2xl z-40 flex-col justify-between py-5 px-3 border-r border-outline-variant/30 shadow-[4px_0_24px_rgba(0,0,0,0.3)] transition-all duration-300 select-none"
    :class="isCollapsed ? 'w-20' : 'w-64'"
  >
    <!-- Top Section: Brand & Navigation -->
    <div class="flex flex-col gap-6">
      <!-- App Brand (No duplicate button here) -->
      <div class="flex items-center gap-3 px-1.5 overflow-hidden">
        <SocaLogo :size="38" />
        <div v-if="!isCollapsed" class="flex flex-col whitespace-nowrap transition-opacity duration-200">
          <span class="font-bold text-on-surface text-base tracking-tight flex items-center gap-1">
            SOCA <span class="text-primary text-xs font-normal">AI</span>
          </span>
          <span class="text-[10px] font-mono uppercase tracking-wider text-primary">Smart Ocular Analyzer</span>
        </div>
      </div>

      <!-- Navigation Menu -->
      <nav class="flex flex-col gap-1.5 pt-2">
        <button
          v-for="item in navItems"
          :key="item.id"
          @click="emit('selectTab', item.id)"
          class="relative flex items-center gap-3.5 px-3 py-3 rounded-xl transition-all duration-200 group text-left"
          :class="[
            currentTab === item.id
              ? 'bg-primary-container text-on-primary-container font-semibold shadow-[0_4px_16px_rgba(62,144,255,0.3)]'
              : 'text-on-surface-variant hover:bg-surface-container-high/60 hover:text-on-surface'
          ]"
          :title="isCollapsed ? item.label : undefined"
        >
          <span
            class="material-symbols-outlined text-[22px] shrink-0 transition-transform group-hover:scale-110"
            :class="currentTab === item.id ? 'fill-1' : ''"
          >
            {{ item.icon }}
          </span>
          
          <span v-if="!isCollapsed" class="text-sm truncate">
            {{ item.label }}
          </span>

          <span
            v-if="!isCollapsed && item.badge"
            class="ml-auto px-2 py-0.5 rounded-full text-[10px] font-mono font-bold tracking-wider"
            :class="currentTab === item.id ? 'bg-white/20 text-white' : 'bg-primary/20 text-primary-fixed'"
          >
            {{ item.badge }}
          </span>

          <!-- Tooltip for collapsed mode -->
          <div
            v-if="isCollapsed"
            class="absolute left-full ml-3 px-3 py-1.5 rounded-lg bg-surface-container-highest text-on-surface text-xs whitespace-nowrap opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-50 shadow-xl border border-outline-variant/40"
          >
            {{ item.label }}
          </div>
        </button>
      </nav>
    </div>

    <!-- Bottom Section: Clean Developer Profile Card (Hapus Neural Engine hijau sesuai permintaan user) -->
    <div class="flex flex-col gap-2">
      <!-- Expanded Bottom Card: Clean Dark Developer Profile -->
      <div
        v-if="!isCollapsed"
        class="flex flex-col gap-2.5 p-3 rounded-xl bg-surface-container/60 border border-outline-variant/30 backdrop-blur-xl shadow-md"
      >
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-on-surface">Rizkia Nuari Fujiana</span>
          <button
            @click="emit('openAbout')"
            class="text-[10px] text-primary hover:underline font-mono"
            title="Buka Info Detail Aplikasi"
          >
            About
          </button>
        </div>

        <span class="text-[11px] text-on-surface-variant leading-tight">
          Software Developer • <span class="text-primary font-mono font-semibold">@luminariadev</span>
        </span>

        <!-- Links to Portfolio & GitHub -->
        <div class="flex items-center gap-2 pt-1 border-t border-outline-variant/20">
          <a
            href="https://rizkianuari.vercel.app/"
            target="_blank"
            class="flex-1 py-1 px-2 rounded-lg bg-surface-container-high hover:bg-surface-bright text-[11px] font-medium text-primary flex items-center justify-center gap-1 transition-colors"
            title="Portofolio 3D Rizkia"
          >
            <span class="material-symbols-outlined text-[13px]">language</span>
            <span>My Portofolio</span>
          </a>
          <a
            href="https://github.com/luminariadev"
            target="_blank"
            class="py-1 px-2.5 rounded-lg bg-surface-container-high hover:bg-surface-bright text-[11px] font-medium text-on-surface flex items-center justify-center gap-1 transition-colors"
            title="GitHub Profile"
          >
            <span class="material-symbols-outlined text-[13px]">code</span>
          </a>
        </div>
      </div>

      <!-- Collapsed Bottom Icon -->
      <button
        v-else
        @click="emit('openAbout')"
        class="w-12 h-12 mx-auto rounded-xl bg-surface-container hover:bg-surface-container-high text-primary flex items-center justify-center transition-colors group relative"
        title="Tentang Pengembang (Rizkia Nuari)"
      >
        <span class="material-symbols-outlined text-[20px]">person</span>
        <div
          class="absolute left-full ml-3 px-3 py-1.5 rounded-lg bg-surface-container-highest text-on-surface text-xs whitespace-nowrap opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-50 shadow-xl border border-outline-variant/40"
        >
          Rizkia Nuari Fujiana (@luminariadev)
        </div>
      </button>
    </div>
  </aside>
</template>
