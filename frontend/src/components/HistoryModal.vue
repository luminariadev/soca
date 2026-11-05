<script setup lang="ts">
import type { ScanResult } from '../types';

const props = defineProps<{
  isOpen: boolean;
  history: ScanResult[];
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'selectResult', item: ScanResult): void;
  (e: 'clearHistory'): void;
}>();
</script>

<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-[80] bg-black/80 backdrop-blur-xl flex flex-col justify-end sm:justify-center sm:items-center p-0 sm:p-6 transition-all"
    @click.self="emit('close')"
  >
    <div class="relative w-full max-w-2xl rounded-t-[32px] sm:rounded-3xl bg-surface-container/95 border-t sm:border border-outline-variant/40 backdrop-blur-2xl shadow-[0_-16px_48px_rgba(0,0,0,0.85)] sm:shadow-[0_32px_80px_rgba(0,0,0,0.85)] p-5 sm:p-7 flex flex-col gap-4 sm:gap-5 max-h-[88vh] overflow-hidden sm:my-auto">
      <!-- Mobile Pull Bar -->
      <div class="w-12 h-1.5 rounded-full bg-white/25 mx-auto mb-1 sm:hidden shrink-0"></div>

      <!-- Top Highlight Glow -->
      <div class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>

      <!-- Modal Header -->
      <div class="flex items-center justify-between pb-3 border-b border-outline-variant/30">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">history</span>
          </div>
          <div>
            <h3 class="font-bold text-on-surface text-base sm:text-lg">Riwayat Sesi Skrining</h3>
            <p class="text-[11px] sm:text-xs text-on-surface-variant font-mono">Tersimpan lokal di perangkat ini (Local Client-Side Storage)</p>
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

      <!-- Modal Body: History List -->
      <div class="overflow-y-auto flex flex-col gap-3 pr-1 py-1">
        <div
          v-if="history.length === 0"
          class="flex flex-col items-center justify-center py-12 text-center text-on-surface-variant gap-3"
        >
          <span class="material-symbols-outlined text-[48px] text-outline opacity-60">fact_check</span>
          <p class="text-sm font-medium">Belum ada riwayat pemindaian pada sesi ini.</p>
          <p class="text-xs text-outline max-w-xs">Lakukan pemindaian melalui tab "Pemindaian AI" untuk melihat hasil di sini.</p>
        </div>

        <div
          v-for="item in history"
          :key="item.id"
          class="p-4 rounded-xl bg-surface-container-low/90 border border-outline-variant/30 hover:border-primary/50 transition-all flex items-center justify-between gap-4 cursor-pointer group"
          @click="emit('selectResult', item)"
        >
          <div class="flex items-center gap-3">
            <!-- Thumbnail preview -->
            <div class="w-14 h-14 rounded-lg bg-surface-container-highest overflow-hidden relative shrink-0 border border-outline-variant/20">
              <img
                v-if="item.imageSrc"
                :src="item.imageSrc"
                class="w-full h-full object-cover"
                alt="Eye Crop"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-primary">
                <span class="material-symbols-outlined text-[24px]">visibility</span>
              </div>
            </div>

            <!-- Details -->
            <div class="flex flex-col">
              <div class="flex items-center gap-2">
                <span class="font-semibold text-on-surface text-sm group-hover:text-primary transition-colors">
                  {{ item.conditionName }}
                </span>
                <span
                  class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold"
                  :class="[
                    item.severity === 'Aman / Normal' ? 'bg-tertiary/20 text-tertiary' :
                    item.severity === 'Ringan' ? 'bg-amber-400/20 text-amber-300' :
                    'bg-error/20 text-error'
                  ]"
                >
                  {{ item.severity }}
                </span>
              </div>
              <span class="text-[11px] font-mono text-on-surface-variant">
                {{ item.timestamp }} • Keyakinan: <strong class="text-primary">{{ item.confidence.toFixed(1) }}%</strong>
              </span>
            </div>
          </div>

          <span class="material-symbols-outlined text-outline group-hover:text-primary transition-colors">
            chevron_right
          </span>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="flex items-center justify-between pt-3 border-t border-outline-variant/30 text-xs">
        <span class="text-on-surface-variant font-mono">
          Total: {{ history.length }} Pemindaian
        </span>

        <div class="flex items-center gap-2">
          <button
            v-if="history.length > 0"
            @click="emit('clearHistory')"
            class="px-3 py-1.5 rounded-lg bg-surface-container-high hover:bg-error/20 hover:text-error text-on-surface-variant transition-colors"
          >
            Hapus Riwayat
          </button>
          <button
            @click="emit('close')"
            class="px-4 py-1.5 rounded-lg bg-primary-container text-on-primary-container font-semibold hover:brightness-110 transition-all"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
