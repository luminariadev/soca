<script setup lang="ts">
</script>

<template>
  <div class="flex flex-col gap-8 w-full">
    <!-- Header -->
    <div class="flex flex-col gap-2">
      <div class="flex items-center gap-2 text-primary font-mono text-xs uppercase tracking-wider">
        <span class="material-symbols-outlined text-[18px]">security</span>
        <span>Etika Medis & Arsitektur Privasi</span>
      </div>
      <h1 class="text-2xl sm:text-3xl font-extrabold text-on-surface tracking-tight">
        Komitmen Privasi, Keamanan, & Batasan Klinis
      </h1>
      <p class="text-xs sm:text-sm text-on-surface-variant max-w-2xl">
        SOCA dirancang dengan filosofi privasi mutlak (*Privacy-by-Design*). Seluruh data visual mata Anda diproses di sisi klien tanpa pernah diunggah atau disimpan di server cloud publik.
      </p>
    </div>

    <!-- 3 Core Pillars -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Pillar 1 -->
      <div class="p-6 rounded-2xl bg-surface-container/70 border border-outline-variant/30 backdrop-blur-xl shadow-lg flex flex-col gap-4">
        <div class="w-12 h-12 rounded-2xl bg-tertiary/15 text-tertiary flex items-center justify-center">
          <span class="material-symbols-outlined text-[26px]">lock</span>
        </div>
        <div>
          <h3 class="font-bold text-on-surface text-base">Zero-Cloud On-Device ML</h3>
          <p class="text-xs text-on-surface-variant leading-relaxed mt-2">
            Pemrosesan citra kamera dilakukan secara lokal di memori peramban Anda. Tidak ada video atau rekaman wajah yang dikirimkan ke server eksternal mana pun.
          </p>
        </div>
      </div>

      <!-- Pillar 2 -->
      <div class="p-6 rounded-2xl bg-surface-container/70 border border-outline-variant/30 backdrop-blur-xl shadow-lg flex flex-col gap-4">
        <div class="w-12 h-12 rounded-2xl bg-primary/15 text-primary flex items-center justify-center">
          <span class="material-symbols-outlined text-[26px]">medical_services</span>
        </div>
        <div>
          <h3 class="font-bold text-on-surface text-base">Batas Kewenangan Klinis</h3>
          <p class="text-xs text-on-surface-variant leading-relaxed mt-2">
            SOCA adalah instrumen skrining awal (*first-line triage aid*), bukan instrumen diagnosis mutlak. Penegakan diagnosa definitif tetap menjadi wewenang Dokter Spesialis Mata (Sp.M).
          </p>
        </div>
      </div>

      <!-- Pillar 3 -->
      <div class="p-6 rounded-2xl bg-surface-container/70 border border-outline-variant/30 backdrop-blur-xl shadow-lg flex flex-col gap-4">
        <div class="w-12 h-12 rounded-2xl bg-secondary/15 text-secondary flex items-center justify-center">
          <span class="material-symbols-outlined text-[26px]">emergency</span>
        </div>
        <div>
          <h3 class="font-bold text-on-surface text-base">Protokol Kegawatdaruratan</h3>
          <p class="text-xs text-on-surface-variant leading-relaxed mt-2">
            Apabila Anda mengalami trauma mata mendadak, terpapar bahan kimia beracun, atau mengalami hilang penglihatan akut, segera datangi IGD Rumah Sakit Mata terdekat tanpa menunggu hasil aplikasi.
          </p>
        </div>
      </div>
    </div>

    <!-- Detailed Regulatory & Ethics Accordion Box -->
    <div class="p-6 md:p-8 rounded-2xl bg-surface-container-low/90 border border-outline-variant/30 backdrop-blur-2xl shadow-xl flex flex-col gap-6">
      <h2 class="text-lg font-bold text-on-surface">Spesifikasi Transparansi Algoritma</h2>

      <div class="flex flex-col gap-4 text-xs text-on-surface-variant leading-relaxed">
        <div class="p-4 rounded-xl bg-surface-container border border-outline-variant/20">
          <span class="font-bold text-on-surface text-sm">1. Non-Retinal / Safe Optical Acquisition</span>
          <p class="mt-1">
            Kamera yang digunakan adalah webcam standar 720p/1080p laptop atau ponsel. Sistem <strong>TIDAK menggunakan sinar laser atau radiasi fundus medis</strong>, melainkan hanya mendeteksi pantulan cahaya alami pada permukaan mata bagian luar.
          </p>
        </div>

        <div class="p-4 rounded-xl bg-surface-container border border-outline-variant/20">
          <span class="font-bold text-on-surface text-sm">2. Perlindungan Out-of-Distribution (OOD Rejection)</span>
          <p class="mt-1">
            Algoritma dilengkapi mekanisme penolakan otomatis. Apabila kamera merekam objek bukan mata, jari tangan, atau ruangan gelap, model menolak memberikan diagnosa palsu (*max confidence &lt; 45%*) dan meminta pengguna menyesuaikan posisi kamera.
          </p>
        </div>

        <div class="p-4 rounded-xl bg-surface-container border border-outline-variant/20">
          <span class="font-bold text-on-surface text-sm">3. Lisensi & Kepemilikan Riset</span>
          <p class="mt-1">
            Arsitektur antarmuka dan model kecerdasan buatan SOCA dirancang dan dikembangkan oleh <strong>Rizkia Nuari Fujiana (luminariadev)</strong> di bawah lisensi MIT untuk kepentingan riset akademis dan inovasi teknologi kesehatan mata digital.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
