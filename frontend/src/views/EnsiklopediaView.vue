<script setup lang="ts">
import { ref } from 'vue';
import { EYE_CONDITIONS } from '../data/conditions';

const selectedConditionId = ref('konjungtivitis');
const conditionsList = Object.values(EYE_CONDITIONS);
const currentCondition = ref(conditionsList.find(c => c.id === selectedConditionId.value) || conditionsList[1]);

const selectCondition = (id: string) => {
  selectedConditionId.value = id;
  const found = conditionsList.find(c => c.id === id);
  if (found) currentCondition.value = found;
};
</script>

<template>
  <div class="flex flex-col gap-8 w-full">
    <!-- Header -->
    <div class="flex flex-col gap-2">
      <div class="flex items-center gap-2 text-primary font-mono text-xs uppercase tracking-wider">
        <span class="material-symbols-outlined text-[18px]">menu_book</span>
        <span>Ensiklopedia Klinis Mata Luar</span>
      </div>
      <h1 class="text-2xl sm:text-3xl font-extrabold text-on-surface tracking-tight">
        Panduan & Atlas 7 Kondisi Mata Eksternal
      </h1>
      <p class="text-xs sm:text-sm text-on-surface-variant max-w-2xl">
        Pelajari karakteristik visual, patofisiologi singkat, gejala klinis, dan langkah pencegahan untuk 7 kondisi mata yang dipantau oleh SOCA AI.
      </p>
    </div>

    <!-- Condition Selector Pill Strip -->
    <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
      <button
        v-for="cond in conditionsList"
        :key="cond.id"
        @click="selectCondition(cond.id)"
        class="px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all border"
        :class="[
          selectedConditionId === cond.id
            ? 'bg-primary-container text-on-primary-container border-primary shadow-md'
            : 'bg-surface-container hover:bg-surface-container-high text-on-surface-variant border-outline-variant/30'
        ]"
      >
        {{ cond.name }}
      </button>
    </div>

    <!-- Active Condition Detail Showcase Card -->
    <div class="p-6 md:p-8 rounded-2xl bg-surface-container/70 border border-outline-variant/30 backdrop-blur-2xl shadow-xl grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      <!-- Image & Meta (5 Cols) -->
      <div class="lg:col-span-5 flex flex-col gap-4">
        <div class="relative w-full aspect-video sm:aspect-square rounded-2xl overflow-hidden bg-black/60 border border-outline-variant/30 shadow-lg">
          <img
            :src="currentCondition.imageUrl"
            class="w-full h-full object-cover"
            :alt="currentCondition.name"
          />
          <div class="absolute bottom-3 left-3 px-3 py-1 rounded-full bg-black/75 backdrop-blur-md text-[11px] font-mono text-primary font-semibold">
            ICD-10: {{ currentCondition.icd10 }}
          </div>
        </div>

        <div class="p-4 rounded-xl bg-surface-container-low border border-outline-variant/20 flex flex-col gap-1.5">
          <span class="text-[11px] font-mono text-on-surface-variant uppercase">Nama Latin Medis:</span>
          <span class="font-bold text-sm text-primary italic">{{ currentCondition.latinName }}</span>
          <span class="text-xs text-on-surface-variant mt-1">{{ currentCondition.category }}</span>
        </div>
      </div>

      <!-- Description, Symptoms & Care (7 Cols) -->
      <div class="lg:col-span-7 flex flex-col gap-6">
        <div>
          <h2 class="text-xl sm:text-2xl font-bold text-on-surface">{{ currentCondition.name }}</h2>
          <p class="text-xs sm:text-sm text-on-surface-variant leading-relaxed mt-2">
            {{ currentCondition.description }}
          </p>
        </div>

        <!-- Symptoms List -->
        <div class="flex flex-col gap-2">
          <span class="text-xs font-mono uppercase tracking-wider text-on-surface font-semibold">Tanda & Gejala Klinis:</span>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div
              v-for="(sym, idx) in currentCondition.symptoms"
              :key="idx"
              class="flex items-start gap-2 p-3 rounded-xl bg-surface-container-low border border-outline-variant/20 text-xs text-on-surface"
            >
              <span class="material-symbols-outlined text-primary text-[16px] shrink-0 mt-0.5">check</span>
              <span>{{ sym }}</span>
            </div>
          </div>
        </div>

        <!-- Self Care Directives -->
        <div class="flex flex-col gap-2">
          <span class="text-xs font-mono uppercase tracking-wider text-on-surface font-semibold">Saran Perawatan & Edukasi:</span>
          <div class="flex flex-col gap-2.5">
            <div
              v-for="(care, idx) in currentCondition.selfCare"
              :key="idx"
              class="flex items-start gap-3 p-3.5 rounded-xl bg-surface-container-low border border-outline-variant/20"
            >
              <div class="w-7 h-7 rounded-full bg-primary/10 text-primary flex items-center justify-center shrink-0 mt-0.5 overflow-hidden select-none">
                <span class="material-symbols-outlined text-[16px] leading-none">{{ care.icon }}</span>
              </div>
              <div>
                <span class="font-semibold text-xs text-on-surface">{{ care.title }}</span>
                <p class="text-[11px] text-on-surface-variant mt-0.5">{{ care.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
