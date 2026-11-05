<script setup lang="ts">
import { ref, computed } from 'vue';
import type { ScanResult, ClinicProvider } from '../types';
import { EYE_CONDITIONS } from '../data/conditions';
import { NATIONAL_EYE_CENTERS, EMERGENCY_HOTLINE, calculateDistanceKm } from '../data/clinics';
import ClinicMap from '../components/ClinicMap.vue';

const props = defineProps<{
  result: ScanResult | null;
}>();

const emit = defineEmits<{
  (e: 'newScan'): void;
}>();

// Demo simulation state when accessed directly without prior scan
const demoResult = ref<ScanResult | null>(null);

// The active result being displayed (real scan result or demo result)
const currentDisplayResult = computed(() => props.result || demoResult.value);

// Multi-Region & GPS State
const selectedRegion = ref<string>('Semua');
const userCoords = ref<[number, number] | null>(null);
const isLocating = ref(false);
const locationStatusMessage = ref<string | null>(null);
const allClinics = ref<ClinicProvider[]>([...NATIONAL_EYE_CENTERS]);
const selectedClinicId = ref<string | null>(allClinics.value[0]?.id || null);

const regions = [
  'Semua',
  'Jawa Barat',
  'Jabodetabek',
  'Bali',
  'Sumatera',
  'Jawa Timur',
  'Jawa Tengah & DIY',
  'Sulawesi'
];

// Detect User Real GPS Location
const detectUserLocation = () => {
  if (!navigator.geolocation) {
    locationStatusMessage.value = 'Browser Anda tidak mendukung geolokasi. Silakan pilih wilayah secara manual di bawah.';
    return;
  }

  isLocating.value = true;
  locationStatusMessage.value = 'Mendeteksi posisi GPS Anda...';

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      isLocating.value = false;
      const lat = pos.coords.latitude;
      const lon = pos.coords.longitude;
      userCoords.value = [lat, lon];

      const updated = NATIONAL_EYE_CENTERS.map((c) => ({
        ...c,
        distanceKm: calculateDistanceKm(lat, lon, c.coordinates[0], c.coordinates[1])
      })).sort((a, b) => a.distanceKm - b.distanceKm);

      allClinics.value = updated;
      selectedRegion.value = 'Terdekat GPS';
      selectedClinicId.value = updated[0]?.id || null;
      locationStatusMessage.value = `📍 GPS Aktif: Menemukan ${updated.length} faskes mata diurutkan dari yang paling dekat dengan posisi Anda.`;
    },
    () => {
      isLocating.value = false;
      locationStatusMessage.value = 'Izin lokasi tidak diberikan. Menampilkan direktori nasional (pilih wilayah di bawah).';
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
  );
};

const filteredClinics = computed(() => {
  if (selectedRegion.value === 'Semua' || selectedRegion.value === 'Terdekat GPS') {
    return allClinics.value;
  }
  return allClinics.value.filter((c) => c.region.includes(selectedRegion.value));
});

const selectRegionFilter = (reg: string) => {
  selectedRegion.value = reg;
  const list = filteredClinics.value;
  if (list.length > 0) {
    selectedClinicId.value = list[0].id;
  }
};

const activeCondition = computed(() => {
  if (!currentDisplayResult.value) {
    return EYE_CONDITIONS['Konjungtivitis'];
  }
  const condKey = currentDisplayResult.value.conditionName.split(' ')[0];
  return EYE_CONDITIONS[condKey] || EYE_CONDITIONS['Konjungtivitis'];
});

const selectedClinic = computed(() => {
  return allClinics.value.find((c) => c.id === selectedClinicId.value) || allClinics.value[0];
});

// Enable demo preview mode
const loadDemoResult = () => {
  demoResult.value = {
    id: 'DEMO-OCU-8842',
    timestamp: new Date().toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' }),
    conditionName: 'Konjungtivitis (Mata Merah)',
    confidence: 98.4,
    icd10: 'H10.9',
    severity: 'Sedang',
    probabilities: [
      { name: 'Konjungtivitis Akut', probability: 98.4, icd10: 'H10.9' },
      { name: 'Blefaritis Margin Palpebra', probability: 1.1, icd10: 'H01.0' },
      { name: 'Mata Sehat Normal', probability: 0.3, icd10: 'Z01.00' },
      { name: 'Kekeruhan Lensa Katarak', probability: 0.2, icd10: 'H26.9' }
    ]
  };
};

const printReferralSlip = () => {
  window.print();
};
</script>

<template>
  <div class="w-full max-w-full">
    <!-- ========================================== -->
    <!-- 1. EMPTY STATE (Ketika Belum Ada Scan)     -->
    <!-- ========================================== -->
    <div
      v-if="!currentDisplayResult"
      class="flex flex-col items-center justify-center text-center py-16 px-4 max-w-2xl mx-auto gap-6"
    >
      <!-- Biometric Scanner Icon Frame -->
      <div class="relative w-24 h-24 rounded-3xl bg-surface-container-high border border-outline-variant/40 flex items-center justify-center shadow-2xl">
        <div class="w-16 h-16 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
          <span class="material-symbols-outlined text-[42px]">clinical_notes</span>
        </div>
        <div class="absolute -top-1.5 -right-1.5 w-4 h-4 rounded-full bg-primary animate-ping"></div>
        <div class="absolute -top-1.5 -right-1.5 w-4 h-4 rounded-full bg-primary"></div>
      </div>

      <!-- Text Proposition -->
      <div class="flex flex-col gap-2">
        <span class="text-xs font-mono font-bold uppercase tracking-wider text-primary">
          Dashboard Evaluasi Klinis Standby
        </span>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Belum Ada Hasil Pemindaian Aktif
        </h1>
        <p class="text-sm text-on-surface-variant leading-relaxed">
          Halaman ini akan menyajikan analisis komprehensif (probabilitas 7 kondisi mata luar, tingkat keparahan, saran perawatan mandiri, dan rujukan dokter mata terdekat) setelah Anda melakukan skrining pada kamera.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
        <button
          @click="emit('newScan')"
          class="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-primary-container to-secondary-container text-white font-bold text-sm shadow-[0_8px_24px_rgba(49,152,220,0.4)] hover:brightness-110 active:scale-95 transition-all"
        >
          <span class="material-symbols-outlined text-[20px]">center_focus_strong</span>
          <span>Mulai Pemindaian Sekarang</span>
        </button>

        <button
          @click="loadDemoResult"
          class="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-surface-container-high hover:bg-surface-bright text-on-surface border border-outline-variant/40 text-sm font-semibold transition-all shadow-sm"
        >
          <span class="material-symbols-outlined text-[18px] text-primary">science</span>
          <span>Lihat Contoh Hasil (Simulasi Demo)</span>
        </button>
      </div>

      <div class="pt-4 text-xs font-mono text-on-surface-variant/80 border-t border-outline-variant/20 w-full flex items-center justify-center gap-4">
        <span>🔒 100% On-Device</span>
        <span>•</span>
        <span>7 Kondisi Anterior</span>
        <span>•</span>
        <span>Format Rujukan Standar Sp.M</span>
      </div>
    </div>

    <!-- =================================================== -->
    <!-- 2. FULL CLINICAL DASHBOARD (Ketika Hasil Tersedia) -->
    <!-- =================================================== -->
    <div v-else class="flex flex-col gap-8 w-full print:hidden">
      <!-- Stepper / Status Bar -->
      <div class="w-full bg-surface-container/70 border border-outline-variant/30 backdrop-blur-2xl rounded-2xl p-4 sm:p-5 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
            <span class="material-symbols-outlined text-primary text-[22px]">verified</span>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-bold text-on-surface text-sm sm:text-base">Protokol Diagnostik Anterior Selesai</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary-container/20 text-primary uppercase font-bold">
                {{ demoResult ? 'Mode Demo' : 'Live Verified' }}
              </span>
            </div>
            <span class="text-xs font-mono text-on-surface-variant">
              Sesi #{{ currentDisplayResult.id }} • Tingkat Keyakinan {{ currentDisplayResult.confidence }}%
            </span>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button
            @click="emit('newScan')"
            class="flex items-center gap-2 px-4 py-2 rounded-xl bg-surface-container-high hover:bg-surface-bright text-xs sm:text-sm font-semibold text-on-surface transition-all"
          >
            <span class="material-symbols-outlined text-[18px]">replay</span>
            <span>Pindai Mata Baru</span>
          </button>
        </div>
      </div>

      <!-- Diagnostic Banner & Triage Level -->
      <div class="relative overflow-hidden rounded-2xl bg-surface-container-low/90 border border-outline-variant/30 backdrop-blur-2xl p-6 sm:p-8 shadow-2xl flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-5">
          <div class="w-16 h-16 rounded-2xl bg-secondary-container/40 flex items-center justify-center text-secondary shrink-0 shadow-lg">
            <span class="material-symbols-outlined text-[36px]">visibility</span>
          </div>
          <div class="flex flex-col">
            <div class="flex flex-wrap items-center gap-2 mb-1.5">
              <span class="text-[11px] font-mono uppercase px-2.5 py-0.5 rounded-full bg-error/20 text-error font-bold">
                ICD-10 {{ currentDisplayResult.icd10 }}
              </span>
              <span class="text-[11px] font-mono uppercase px-2.5 py-0.5 rounded-full bg-primary/15 text-primary font-medium">
                {{ activeCondition.category }}
              </span>
            </div>
            <h1 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-on-surface tracking-tight">
              {{ currentDisplayResult.conditionName }}
            </h1>
            <p class="text-xs sm:text-sm text-on-surface-variant mt-1.5 max-w-3xl leading-relaxed">
              {{ activeCondition.description }}
            </p>
          </div>
        </div>

        <!-- Severity Capsule -->
        <div class="flex items-center gap-3.5 px-5 py-3 rounded-2xl bg-surface-container border border-outline-variant/40 shrink-0 shadow-md">
          <span
            class="w-3 h-3 rounded-full animate-ping"
            :class="[
              currentDisplayResult.severity === 'Aman / Normal' ? 'bg-tertiary' :
              currentDisplayResult.severity === 'Ringan' ? 'bg-amber-400' :
              'bg-error'
            ]"
          ></span>
          <div class="flex flex-col">
            <span class="text-[10px] font-mono uppercase tracking-wider text-on-surface-variant font-bold">Tingkat Keparahan</span>
            <span class="text-sm font-bold text-on-surface">
              {{ currentDisplayResult.severity }}
            </span>
          </div>
        </div>
      </div>

      <!-- Multi-Class Distribution Bars & Self Care Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <div class="lg:col-span-6 flex flex-col gap-5 p-6 sm:p-7 rounded-2xl bg-surface-container/60 border border-outline-variant/30 backdrop-blur-2xl shadow-xl">
          <div class="flex items-center justify-between pb-3 border-b border-outline-variant/30">
            <div class="flex items-center gap-2.5">
              <span class="material-symbols-outlined text-primary text-[22px]">bar_chart</span>
              <h2 class="text-base sm:text-lg font-bold text-on-surface">Distribusi Probabilitas Model AI</h2>
            </div>
            <span class="text-[11px] font-mono text-tertiary font-bold">CALIBRATED</span>
          </div>

          <div class="flex flex-col gap-3.5">
            <div
              v-for="(item, idx) in currentDisplayResult.probabilities"
              :key="idx"
              class="flex flex-col gap-1.5"
            >
              <div class="flex items-center justify-between text-xs">
                <span class="font-medium text-on-surface">{{ item.name }}</span>
                <span class="font-mono font-bold text-primary">{{ item.probability }}%</span>
              </div>
              <div class="w-full bg-surface-container-highest rounded-full h-2 overflow-hidden">
                <div
                  class="h-2 rounded-full transition-all duration-700 bg-gradient-to-r"
                  :class="idx === 0 ? 'from-primary-container to-secondary-container' : 'from-slate-600 to-slate-500'"
                  :style="{ width: `${item.probability}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Guidance & Self Care -->
        <div class="lg:col-span-6 flex flex-col gap-5 p-6 sm:p-7 rounded-2xl bg-surface-container/60 border border-outline-variant/30 backdrop-blur-2xl shadow-xl">
          <div class="flex items-center gap-2.5 pb-3 border-b border-outline-variant/30">
            <span class="material-symbols-outlined text-secondary text-[22px]">health_and_safety</span>
            <h2 class="text-base sm:text-lg font-bold text-on-surface">Rekomendasi Penanganan Mandiri</h2>
          </div>

          <div class="flex flex-col gap-3">
            <div
              v-for="(care, idx) in activeCondition.selfCare"
              :key="idx"
              class="p-4 rounded-xl bg-surface-container-low border border-outline-variant/20 flex items-start gap-3.5"
            >
              <div class="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0 overflow-hidden select-none">
                <span class="material-symbols-outlined text-[18px]">{{ care.icon }}</span>
              </div>
              <div class="flex flex-col">
                <span class="font-bold text-xs sm:text-sm text-on-surface">{{ care.title }}</span>
                <span class="text-xs text-on-surface-variant leading-relaxed mt-0.5">{{ care.desc }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION: PETA REAL-TIME DOKTER MATA NASIONAL -->
      <section class="p-6 sm:p-8 rounded-2xl bg-surface-container-low/90 border border-outline-variant/40 backdrop-blur-2xl shadow-2xl flex flex-col gap-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-outline-variant/30">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-2xl bg-primary/15 text-primary flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[26px]">near_me</span>
            </div>
            <div>
              <h2 class="text-xl font-bold text-on-surface">Peta Faskes & Rujukan Spesialis Mata (Nasional)</h2>
              <p class="text-xs text-on-surface-variant font-mono">
                Peta Dinamis ESRI Dark Canvas • Mendukung Deteksi GPS Real-Time & Rujukan Lintas Provinsi
              </p>
            </div>
          </div>

          <!-- 24/7 Hotline Badge -->
          <div class="flex items-center gap-2.5 px-4 py-2 rounded-xl bg-error/15 border border-error/30 text-error shrink-0">
            <span class="material-symbols-outlined text-[22px] animate-pulse">phone_in_talk</span>
            <div class="flex flex-col text-right sm:text-left">
              <span class="text-[10px] font-mono font-bold uppercase tracking-wider">Hotline Rujukan 24 Jam</span>
              <span class="text-xs font-mono font-bold">{{ EMERGENCY_HOTLINE.number }}</span>
            </div>
          </div>
        </div>

        <!-- Live GPS & Region Controls Bar -->
        <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 p-3.5 rounded-xl bg-surface-container border border-outline-variant/30">
          <button
            @click="detectUserLocation"
            :disabled="isLocating"
            class="flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-primary-container text-white text-xs font-bold shadow-md hover:brightness-110 active:scale-95 transition-all shrink-0"
          >
            <span class="material-symbols-outlined text-[18px]" :class="isLocating ? 'animate-spin' : ''">
              {{ isLocating ? 'sync' : 'my_location' }}
            </span>
            <span>{{ isLocating ? 'Mendeteksi Posisi Anda...' : 'Deteksi Lokasi Saya (GPS)' }}</span>
          </button>

          <div class="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0 scrollbar-none">
            <button
              v-for="reg in regions"
              :key="reg"
              @click="selectRegionFilter(reg)"
              class="px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all border"
              :class="[
                selectedRegion === reg
                  ? 'bg-primary text-on-primary font-bold border-primary shadow-sm'
                  : 'bg-surface-container-high/60 hover:bg-surface-bright text-on-surface-variant border-outline-variant/30'
              ]"
            >
              {{ reg }}
            </button>
          </div>
        </div>

        <div
          v-if="locationStatusMessage"
          class="px-4 py-2 rounded-xl bg-surface-container-high border border-outline-variant/30 text-xs font-mono text-primary flex items-center gap-2"
        >
          <span class="material-symbols-outlined text-[16px] text-tertiary">info</span>
          <span>{{ locationStatusMessage }}</span>
        </div>

        <!-- Real Leaflet Map Component -->
        <ClinicMap
          :clinics="filteredClinics"
          :selectedClinicId="selectedClinicId"
          :userCoordinates="userCoords"
        />

        <!-- Clinics List Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <div
            v-for="clinic in filteredClinics"
            :key="clinic.id"
            @click="selectedClinicId = clinic.id"
            class="p-5 rounded-2xl bg-surface-container border transition-all duration-200 flex flex-col justify-between gap-4 shadow-md cursor-pointer group"
            :class="selectedClinicId === clinic.id ? 'border-primary ring-2 ring-primary/40 bg-surface-container-high' : 'border-outline-variant/30 hover:border-primary/40'"
          >
            <div class="flex flex-col gap-2">
              <div class="flex items-start justify-between gap-2">
                <span class="font-bold text-sm text-on-surface group-hover:text-primary transition-colors">
                  {{ clinic.name }}
                </span>
                <div class="flex items-center gap-1 text-xs font-mono text-tertiary shrink-0">
                  <span class="material-symbols-outlined text-[14px]">star</span>
                  <span>{{ clinic.rating }}</span>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-primary/10 text-primary">
                  {{ clinic.region }}
                </span>
                <span class="text-xs text-secondary truncate">{{ clinic.type }}</span>
              </div>

              <p class="text-[11px] text-on-surface-variant leading-relaxed">{{ clinic.address }}</p>

              <div class="p-3 rounded-xl bg-surface-container-lowest/80 text-[11px] font-mono text-on-surface-variant flex flex-col gap-1 border border-outline-variant/20">
                <span class="text-primary font-semibold">{{ clinic.schedule }}</span>
                <span class="truncate">{{ clinic.doctorOnCall }}</span>
              </div>
            </div>

            <div class="flex items-center justify-between pt-2 border-t border-outline-variant/20">
              <span class="text-xs font-mono font-bold" :class="clinic.distanceKm > 0 ? 'text-tertiary' : 'text-on-surface-variant'">
                {{ clinic.distanceKm > 0 ? `${clinic.distanceKm} km dari posisi Anda` : clinic.region }}
              </span>
              <a
                :href="clinic.mapsUrl"
                target="_blank"
                @click.stop
                class="px-3.5 py-1.5 rounded-lg bg-primary-container text-white font-semibold text-xs hover:brightness-110 transition-all flex items-center gap-1 shadow-sm"
              >
                <span>Petunjuk Rute</span>
                <span class="material-symbols-outlined text-[14px]">near_me</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom Action Dock (HANYA MUNCUL KETIKA HASIL ADA, Aman di atas Mobile Floating Bar) -->
      <div class="w-full bg-surface-container-lowest/95 border border-outline-variant/30 backdrop-blur-2xl rounded-2xl p-4 sm:p-5 shadow-2xl flex flex-wrap items-center justify-between gap-4 sticky bottom-24 md:bottom-4 z-20">
        <button
          @click="emit('newScan')"
          class="flex items-center gap-2 px-5 py-2.5 rounded-full bg-surface-container-high hover:bg-surface-bright text-xs sm:text-sm font-semibold text-on-surface transition-all"
        >
          <span class="material-symbols-outlined text-[18px]">replay</span>
          <span>Periksa Pasien Lain</span>
        </button>

        <button
          @click="printReferralSlip"
          class="flex items-center gap-2 px-6 py-2.5 rounded-full bg-primary-container text-white text-xs sm:text-sm font-bold shadow-md hover:brightness-110 transition-all"
        >
          <span class="material-symbols-outlined text-[18px]">print</span>
          <span>Cetak Lembar Rujukan Medis</span>
        </button>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- 3. PRINT-ONLY MEDICAL REFERRAL SLIP TEMPLATE (Standar Rumah Sakit) -->
    <!-- ============================================================== -->
    <div
      v-if="currentDisplayResult"
      class="hidden print:block text-slate-900 bg-white p-6 max-w-4xl mx-auto font-sans leading-normal"
    >
      <!-- Hospital Referral Header -->
      <div class="border-b-2 border-slate-900 pb-4 mb-5 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <img src="/favicon.svg" class="w-12 h-12" alt="SOCA Logo" />
          <div>
            <h1 class="text-xl font-black text-slate-900 tracking-tight">SOCA CLINICAL VISION AI</h1>
            <p class="text-xs text-slate-600 font-mono">Smart Ocular Condition Analyzer • Anterior Eye Screening</p>
          </div>
        </div>
        <div class="text-right text-xs text-slate-600 font-mono">
          <div>No. Registrasi: <strong>{{ currentDisplayResult.id }}</strong></div>
          <div>Tanggal/Waktu: {{ currentDisplayResult.timestamp }}</div>
          <div>Metode: On-Device MobileNetV3 Edge Inference</div>
        </div>
      </div>

      <!-- Title Banner -->
      <div class="text-center my-4">
        <h2 class="text-base font-extrabold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 inline-block">
          LEMBAR HASIL SKRINING AWAL & REKOMENDASI RUJUKAN OFTALMOLOGI
        </h2>
        <p class="text-[11px] text-slate-500 italic mt-1">
          Dokumen hasil analisis komputasi citra mata eksternal sebagai bahan pertimbangan rujukan medis.
        </p>
      </div>

      <!-- Section 1: Diagnostic Findings Table -->
      <table class="w-full text-xs border border-slate-300 mb-5 border-collapse">
        <tbody>
          <tr class="border-b border-slate-300 bg-slate-100">
            <td class="p-2 font-bold w-1/3">Kondisi Klinis Teridentifikasi</td>
            <td class="p-2 font-bold text-slate-900 text-sm w-2/3">
              {{ currentDisplayResult.conditionName }}
            </td>
          </tr>
          <tr class="border-b border-slate-300">
            <td class="p-2 font-bold">Kode ICD-10 & Klasifikasi</td>
            <td class="p-2 font-mono">
              ICD-10: <strong>{{ currentDisplayResult.icd10 }}</strong> • {{ activeCondition.latinName }} ({{ activeCondition.category }})
            </td>
          </tr>
          <tr class="border-b border-slate-300">
            <td class="p-2 font-bold">Tingkat Keyakinan Model (Confidence)</td>
            <td class="p-2 font-mono font-bold">{{ currentDisplayResult.confidence }}%</td>
          </tr>
          <tr class="border-b border-slate-300">
            <td class="p-2 font-bold">Derajat Triage / Urgensi Medis</td>
            <td class="p-2 font-bold" :class="currentDisplayResult.severity === 'Perlu Penanganan Cepat' ? 'text-red-700 font-black' : 'text-slate-800'">
              {{ currentDisplayResult.severity }}
            </td>
          </tr>
          <tr>
            <td class="p-2 font-bold">Patofisiologi / Deskripsi Singkat</td>
            <td class="p-2 text-slate-700 leading-relaxed">{{ activeCondition.description }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Section 2: Multi-Class Probability Comparison -->
      <div class="mb-5">
        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-900 mb-2 border-b border-slate-300 pb-1">
          Distribusi Probabilitas Diferensial Diagnosis AI:
        </h3>
        <table class="w-full text-xs border border-slate-200 border-collapse">
          <thead>
            <tr class="bg-slate-100 border-b border-slate-200">
              <th class="p-1.5 text-left font-bold">Kondisi Mata Bagian Luar</th>
              <th class="p-1.5 text-right font-bold w-24">Probabilitas</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="prob in currentDisplayResult.probabilities"
              :key="prob.name"
              class="border-b border-slate-100"
            >
              <td class="p-1.5">{{ prob.name }}</td>
              <td class="p-1.5 text-right font-mono font-medium">{{ prob.probability }}%</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Section 3: Care Guidance & Strict Restrictions -->
      <div class="grid grid-cols-2 gap-4 mb-5">
        <div class="border border-slate-300 p-3 rounded">
          <h4 class="text-xs font-bold text-slate-900 mb-1.5 uppercase">Anjuran Penanganan Awal Mandiri:</h4>
          <ul class="text-[11px] text-slate-700 list-disc list-inside space-y-1">
            <li v-for="(care, idx) in activeCondition.selfCare" :key="idx">
              <strong>{{ care.title }}:</strong> {{ care.desc }}
            </li>
          </ul>
        </div>
        <div class="border border-red-300 bg-red-50/30 p-3 rounded">
          <h4 class="text-xs font-bold text-red-900 mb-1.5 uppercase">Kontraindikasi (Larangan Keras):</h4>
          <ul class="text-[11px] text-red-800 list-disc list-inside space-y-1">
            <li v-for="(res, idx) in activeCondition.restrictions" :key="idx">
              {{ res }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Section 4: Recommended Eye Center Destination -->
      <div class="border border-slate-300 p-3 rounded mb-6">
        <h4 class="text-xs font-bold text-slate-900 mb-1 uppercase">Fasilitas Kesehatan Spesialis Mata yang Direkomendasikan:</h4>
        <div class="text-xs text-slate-800">
          <div class="font-bold text-sm">{{ selectedClinic.name }} ({{ selectedClinic.type }})</div>
          <div class="text-slate-600">{{ selectedClinic.address }}</div>
          <div class="text-slate-600 font-mono mt-0.5">
            Telepon: {{ selectedClinic.phone }} • Jadwal: {{ selectedClinic.schedule }}
            <span v-if="selectedClinic.distanceKm > 0"> • Jarak: {{ selectedClinic.distanceKm }} km</span>
          </div>
        </div>
      </div>

      <!-- Section 5: Signature & Legal Disclaimer -->
      <div class="grid grid-cols-2 gap-8 pt-4 border-t border-slate-400 text-xs text-slate-600">
        <div>
          <div class="font-bold text-slate-900 mb-1">Disclaimer Medis:</div>
          <p class="text-[10px] leading-relaxed">
            Lembar rujukan ini dihasilkan secara otomatis oleh sistem kecerdasan buatan (SOCA AI) sebagai instrumen triase awal mandiri. Dokumen ini bukan resep obat dan tidak menggantikan pemeriksaan definitif slit-lamp biomicroscopy oleh Dokter Spesialis Mata (Sp.M).
          </p>
        </div>
        <div class="flex flex-col items-center justify-end text-center">
          <div class="text-[11px] text-slate-500 mb-14">Tanda Tangan & Cap Dokter Pemeriksa Rujukan:</div>
          <div class="border-b border-slate-700 w-52 mb-1"></div>
          <div class="text-[10px] text-slate-500">( Dokter Spesialis Mata / Sp.M )</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@media print {
  body {
    background-color: #ffffff !important;
    color: #0f172a !important;
  }
}
</style>
