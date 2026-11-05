<script setup lang="ts">
import { ref } from 'vue';
import type { TabType } from '../types';
import { EYE_CONDITIONS } from '../data/conditions';

const emit = defineEmits<{
  (e: 'navigate', tab: TabType): void;
}>();

const conditionsList = Object.values(EYE_CONDITIONS);
const showSampleModal = ref(false);
const activeSample = ref(conditionsList[1]); // Default to konjungtivitis
</script>

<template>
  <div class="flex flex-col gap-8 md:gap-10 w-full max-w-full">
    <!-- Hero Showcase: Obsidian Slate Clinical Workstation -->
    <section class="relative rounded-3xl bg-surface-container/70 border border-outline-variant/30 backdrop-blur-2xl shadow-[0_20px_50px_rgba(0,0,0,0.4)] p-6 sm:p-8 lg:p-10 overflow-hidden">
      <!-- Hairline Top Highlight -->
      <div class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent"></div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 items-center">
        <!-- Left: Clinical Proposition (7 Cols) -->
        <div class="lg:col-span-7 flex flex-col gap-6">
          <!-- Medical Badge -->
          <div class="inline-flex items-center gap-2.5 self-start px-3.5 py-1.5 rounded-full bg-surface-container-high/90 border border-outline-variant/40 shadow-sm">
            <span class="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
            <span class="text-xs font-mono font-medium text-primary tracking-wide uppercase">
              SOCA AI • Clinical Ocular Telemetry
            </span>
            <span class="text-[11px] font-mono text-on-surface-variant/80 border-l border-outline-variant/40 pl-2">
              v2.4
            </span>
          </div>

          <!-- Main Headline -->
          <div class="flex flex-col gap-3">
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-white leading-[1.15]">
              Skrining Cerdas Kesehatan Mata Bagian Luar Berbasis AI
            </h1>
            <p class="text-sm sm:text-base text-on-surface-variant leading-relaxed max-w-xl">
              Deteksi dini <span class="text-white font-medium">konjungtivitis, katarak luar, blefaritis, mata juling, mata menonjol, dan kantung mata</span> secara instan dan privat via kamera browser tanpa radiasi retina.
            </p>
          </div>

          <!-- Actions -->
          <div class="flex flex-wrap items-center gap-3.5 pt-1">
            <button
              @click="emit('navigate', 'pindai')"
              class="group inline-flex items-center gap-3 px-6 py-3.5 rounded-xl bg-gradient-to-r from-[#3198dc] to-[#29a195] text-white font-bold text-sm sm:text-base shadow-[0_8px_24px_rgba(49,152,220,0.35)] hover:shadow-[0_12px_32px_rgba(49,152,220,0.55)] hover:brightness-110 active:scale-[0.98] transition-all duration-200"
            >
              <span class="material-symbols-outlined text-[20px] transition-transform group-hover:scale-110">center_focus_strong</span>
              <span>Mulai Pemindaian AI</span>
            </button>

            <button
              @click="emit('navigate', 'edukasi')"
              class="inline-flex items-center gap-2.5 px-5 py-3.5 rounded-xl bg-surface-container-high/90 hover:bg-surface-bright text-on-surface border border-outline-variant/40 font-semibold text-sm sm:text-base transition-all duration-200 shadow-sm"
            >
              <span class="material-symbols-outlined text-[20px] text-primary">menu_book</span>
              <span>Atlas 7 Kondisi Mata</span>
            </button>
          </div>

          <!-- Trust & Privacy Checklist -->
          <div class="flex flex-wrap items-center gap-4 pt-1 text-on-surface-variant text-xs font-mono">
            <span class="flex items-center gap-1.5">
              <span class="material-symbols-outlined text-[16px] text-tertiary">lock</span>
              100% On-Device (Zero Server Upload)
            </span>
            <span class="text-outline-variant">•</span>
            <span class="flex items-center gap-1.5">
              <span class="material-symbols-outlined text-[16px] text-primary">bolt</span>
              Latensi &lt; 20ms GPU
            </span>
            <span class="text-outline-variant">•</span>
            <span class="flex items-center gap-1.5">
              <span class="material-symbols-outlined text-[16px] text-secondary">verified</span>
              Akurasi 97.99% Val
            </span>
          </div>
        </div>

        <!-- Right: Authentic Clinical Viewport (5 Cols) -->
        <div class="lg:col-span-5 relative">
          <div class="relative w-full rounded-2xl bg-surface-container-lowest/90 border border-outline-variant/40 shadow-[0_16px_40px_rgba(0,0,0,0.6)] overflow-hidden group">
            <!-- Viewport Top Bar -->
            <div class="px-4 py-2.5 bg-surface-container-high/60 border-b border-outline-variant/30 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-tertiary animate-pulse"></span>
                <span class="text-[11px] font-mono font-semibold text-on-surface uppercase tracking-wider">
                  Optical Aperture Feed
                </span>
              </div>
              <span class="text-[10px] font-mono text-primary font-medium px-2 py-0.5 rounded bg-primary/10">
                224×224 ANTERIOR
              </span>
            </div>

            <!-- Authentic Slit-Lamp Eye Showcase -->
            <div class="relative aspect-[4/3] w-full overflow-hidden bg-black">
              <img
                src="/images/conditions/normal.jpg"
                alt="Clinical Ocular Scan"
                class="w-full h-full object-cover opacity-90 transition-transform duration-700 group-hover:scale-105"
              />

              <!-- Clinical Crosshairs Overlay -->
              <div class="absolute inset-0 pointer-events-none border border-primary/20 m-4 rounded-xl flex items-center justify-center">
                <!-- Center Target Reticle -->
                <div class="w-16 h-16 rounded-full border border-primary/60 flex items-center justify-center relative">
                  <div class="w-2 h-2 rounded-full bg-primary/80 animate-ping"></div>
                  <div class="absolute -top-3 text-[9px] font-mono text-primary font-bold">PUPIL 3.4mm</div>
                </div>

                <!-- Corner brackets -->
                <div class="absolute top-2 left-2 w-3 h-3 border-t-2 border-l-2 border-primary"></div>
                <div class="absolute top-2 right-2 w-3 h-3 border-t-2 border-r-2 border-primary"></div>
                <div class="absolute bottom-2 left-2 w-3 h-3 border-b-2 border-l-2 border-primary"></div>
                <div class="absolute bottom-2 right-2 w-3 h-3 border-b-2 border-r-2 border-primary"></div>
              </div>

              <!-- Live Laser Scan Sweep -->
              <div class="absolute inset-x-0 h-0.5 bg-gradient-to-r from-transparent via-[#3198dc] to-transparent shadow-[0_0_12px_#3198dc] animate-[bounce_3s_infinite] pointer-events-none"></div>

              <!-- Viewport Bottom Badge -->
              <div class="absolute bottom-3 left-3 right-3 flex items-center justify-between pointer-events-none">
                <div class="px-2.5 py-1 rounded-lg bg-surface-container-lowest/90 backdrop-blur-md border border-outline-variant/40 text-[10px] font-mono text-on-surface flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
                  <span>Kornea: Transparan (0.99)</span>
                </div>
                <div class="px-2.5 py-1 rounded-lg bg-surface-container-lowest/90 backdrop-blur-md border border-outline-variant/40 text-[10px] font-mono text-primary font-bold">
                  KONDISI SEHAT
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Key Metrics: Pristine 3-Column Architectural Grid (No Horizontal Overlap) -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-5 lg:gap-6 w-full">
      <!-- Metric 1: Clinical Accuracy -->
      <div class="p-6 rounded-2xl bg-surface-container/60 border border-outline-variant/30 backdrop-blur-xl shadow-md flex flex-col justify-between gap-4 hover:border-primary/40 hover:bg-surface-container/80 transition-all duration-300">
        <div class="flex items-center justify-between">
          <span class="text-xs font-mono font-bold text-on-surface-variant uppercase tracking-wider">Akurasi Verifikasi</span>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-tertiary/20 text-tertiary">
            INDEPENDENT TEST
          </span>
        </div>
        <div>
          <div class="text-4xl font-black text-white tracking-tight">97.99%</div>
          <p class="text-xs text-on-surface-variant mt-1">
            782 dari 798 sampel uji eksternal terklasifikasi akurat dengan 0 false negative pada katarak lanjut.
          </p>
        </div>
        <div class="w-full bg-surface-container-highest rounded-full h-1.5 overflow-hidden">
          <div class="bg-gradient-to-r from-primary-container to-tertiary h-1.5 rounded-full w-[98%]"></div>
        </div>
      </div>

      <!-- Metric 2: External Eye Scope -->
      <div class="p-6 rounded-2xl bg-surface-container/60 border border-outline-variant/30 backdrop-blur-xl shadow-md flex flex-col justify-between gap-4 hover:border-primary/40 hover:bg-surface-container/80 transition-all duration-300">
        <div class="flex items-center justify-between">
          <span class="text-xs font-mono font-bold text-on-surface-variant uppercase tracking-wider">Cakupan Klasifikasi</span>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-primary/20 text-primary">
            7 KELAS ANTERIOR
          </span>
        </div>
        <div>
          <div class="text-4xl font-black text-white tracking-tight">7 Kondisi</div>
          <p class="text-xs text-on-surface-variant mt-1">
            Konjungtivitis, Katarak luar, Blefaritis, Strabismus (juling), Proptosis, Kantung mata, & Normal.
          </p>
        </div>
        <div class="flex flex-wrap gap-1.5">
          <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-surface-container-high text-on-surface-variant">Sklera</span>
          <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-surface-container-high text-on-surface-variant">Kornea</span>
          <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-surface-container-high text-on-surface-variant">Pupil</span>
          <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-surface-container-high text-on-surface-variant">Palpebra</span>
        </div>
      </div>

      <!-- Metric 3: On-Device Latency -->
      <div class="p-6 rounded-2xl bg-surface-container/60 border border-outline-variant/30 backdrop-blur-xl shadow-md flex flex-col justify-between gap-4 hover:border-primary/40 hover:bg-surface-container/80 transition-all duration-300">
        <div class="flex items-center justify-between">
          <span class="text-xs font-mono font-bold text-on-surface-variant uppercase tracking-wider">Latensi Inferensi</span>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-secondary/20 text-secondary">
            100% CLIENT-SIDE
          </span>
        </div>
        <div>
          <div class="text-4xl font-black text-white tracking-tight">8.36 ms</div>
          <p class="text-xs text-on-surface-variant mt-1">
            Diproses langsung pada hardware lokal Anda tanpa pengiriman data citra pasien ke server pihak ketiga.
          </p>
        </div>
        <div class="flex items-center gap-2 text-[11px] font-mono text-tertiary">
          <span class="w-2 h-2 rounded-full bg-tertiary"></span>
          <span>WebAssembly + WebGL Acceleration</span>
        </div>
      </div>
    </section>

    <!-- Condition Gallery Grid (Preview Atlas dengan Real Clinical Photos) -->
    <section class="flex flex-col gap-4 w-full">
      <div class="flex items-center justify-between">
        <div class="flex flex-col">
          <h2 class="text-xl font-bold text-white tracking-tight">7 Kondisi Mata yang Dikenali SOCA AI</h2>
          <p class="text-xs text-on-surface-variant">Foto referensi klinis slit-lamp dan karakteristik diagnostik utama.</p>
        </div>
        <button
          @click="emit('navigate', 'edukasi')"
          class="text-xs font-semibold text-primary hover:underline flex items-center gap-1"
        >
          <span>Lihat Detail Panduan</span>
          <span class="material-symbols-outlined text-[16px]">arrow_forward</span>
        </button>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="cond in conditionsList"
          :key="cond.id"
          @click="activeSample = cond; showSampleModal = true"
          class="group p-3 rounded-2xl bg-surface-container/50 border border-outline-variant/30 hover:border-primary/50 hover:bg-surface-container transition-all cursor-pointer flex flex-col gap-2.5 shadow-sm"
        >
          <div class="relative aspect-video w-full rounded-xl overflow-hidden bg-black/60">
            <img
              :src="cond.imageUrl"
              :alt="cond.name"
              class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
            />
            <div class="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/80 backdrop-blur-sm text-[10px] font-mono text-white font-semibold">
              {{ cond.icd10 }}
            </div>
          </div>
          <div class="flex flex-col">
            <span class="font-bold text-xs sm:text-sm text-on-surface group-hover:text-primary transition-colors line-clamp-2 leading-snug min-h-[2.25rem]">
              {{ cond.name }}
            </span>
            <span class="text-[11px] text-on-surface-variant truncate font-mono mt-0.5">
              {{ cond.category }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Clinical Sample Modal (iOS Bottom Sheet on Mobile, Centered Dialog on Desktop) -->
    <div
      v-if="showSampleModal"
      class="fixed inset-0 z-[80] bg-black/85 backdrop-blur-xl flex flex-col justify-end sm:justify-center sm:items-center p-0 sm:p-6 transition-all"
      @click.self="showSampleModal = false"
    >
      <div class="relative w-full max-w-xl rounded-t-[32px] sm:rounded-3xl bg-surface-container-high border-t sm:border border-outline-variant/40 shadow-[0_-16px_48px_rgba(0,0,0,0.85)] sm:shadow-2xl p-5 sm:p-6 pb-10 sm:pb-6 flex flex-col gap-4 max-h-[88vh] overflow-y-auto sm:my-auto">
        <!-- Mobile Pull Bar -->
        <div class="w-12 h-1.5 rounded-full bg-white/25 mx-auto mb-1 sm:hidden shrink-0"></div>

        <div class="flex items-center justify-between pb-3 border-b border-outline-variant/30">
          <div class="flex flex-col">
            <span class="text-[10px] font-mono text-primary font-bold uppercase tracking-wider">Atlas Referensi Medis</span>
            <h3 class="font-bold text-white text-lg">{{ activeSample.name }}</h3>
          </div>
          <button
            @click="showSampleModal = false"
            class="w-8 h-8 rounded-full bg-surface-container hover:bg-surface-bright flex items-center justify-center text-on-surface-variant hover:text-white transition-colors shrink-0"
            title="Tutup Modal"
          >
            <span class="material-symbols-outlined text-[18px]">close</span>
          </button>
        </div>

        <div class="relative aspect-video w-full rounded-xl overflow-hidden bg-black border border-outline-variant/30">
          <img
            :src="activeSample.imageUrl"
            :alt="activeSample.name"
            class="w-full h-full object-cover"
          />
          <div class="absolute bottom-3 left-3 px-3 py-1 rounded-full bg-black/80 backdrop-blur-md text-xs font-mono text-primary font-bold">
            ICD-10: {{ activeSample.icd10 }} • {{ activeSample.latinName }}
          </div>
        </div>

        <div class="flex flex-col gap-2">
          <span class="text-xs font-mono font-bold text-on-surface uppercase">Deskripsi Klinis:</span>
          <p class="text-xs text-on-surface-variant leading-relaxed">
            {{ activeSample.description }}
          </p>
        </div>

        <div class="flex flex-col gap-2">
          <span class="text-xs font-mono font-bold text-on-surface uppercase">Tanda & Gejala Khas:</span>
          <ul class="flex flex-col gap-1.5">
            <li
              v-for="(sym, i) in activeSample.symptoms"
              :key="i"
              class="text-xs text-on-surface-variant flex items-start gap-2"
            >
              <span class="text-primary font-bold">•</span>
              <span>{{ sym }}</span>
            </li>
          </ul>
        </div>

        <div class="flex items-center justify-end gap-3 pt-2 border-t border-outline-variant/30">
          <button
            @click="showSampleModal = false; emit('navigate', 'edukasi')"
            class="px-4 py-2 rounded-xl bg-surface-container hover:bg-surface-bright text-xs font-semibold text-on-surface transition-colors"
          >
            Buka Panduan Lengkap
          </button>
          <button
            @click="showSampleModal = false; emit('navigate', 'pindai')"
            class="px-5 py-2 rounded-xl bg-primary-container text-white text-xs font-bold hover:brightness-110 transition-all shadow-md"
          >
            Mulai Pindai Mata Anda
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
