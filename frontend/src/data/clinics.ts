import type { ClinicProvider } from '../types';

export const NATIONAL_EYE_CENTERS: ClinicProvider[] = [
  // --- JAWA BARAT (Bandung) ---
  {
    id: 'jabar-cicendo',
    name: 'RS Mata Cicendo (Pusat Mata Nasional)',
    type: 'Pusat Rujukan Nasional • RS Khusus Mata Kelas A',
    region: 'Jawa Barat',
    coordinates: [-6.9118, 107.6042],
    distanceKm: 2.8,
    rating: 4.8,
    address: 'Jl. Cicendo No. 4, Pasir Kaliki, Kec. Cicendo, Kota Bandung',
    schedule: 'IGD Trauma Mata 24 Jam • Poliklinik s/d 16.00',
    doctorOnCall: 'Tim Konsultan Kornea, Infeksi & Bedah Rekonstruksi',
    phone: '022-4231280',
    mapsUrl: 'https://maps.google.com/?q=RS+Mata+Cicendo+Bandung'
  },
  {
    id: 'jabar-bec',
    name: 'Bandung Eye Center (BEC)',
    type: 'Klinik Utama & Bedah Mata Spesialis',
    region: 'Jawa Barat',
    coordinates: [-6.9388, 107.6255],
    distanceKm: 1.4,
    rating: 4.9,
    address: 'Jl. Buah Batu No. 147, Lengkong, Kota Bandung',
    schedule: 'Buka Hari Ini s/d 20.00 WIB',
    doctorOnCall: 'dr. H. Rinaldi, Sp.M(K) • Spesialis Kornea & Sklera',
    phone: '022-7301010',
    mapsUrl: 'https://maps.google.com/?q=Bandung+Eye+Center'
  },
  {
    id: 'jabar-kmn',
    name: 'KMN EyeCare Bandung',
    type: 'Pusat Diagnostik & Bedah Katarak Modern',
    region: 'Jawa Barat',
    coordinates: [-6.9069, 107.6212],
    distanceKm: 4.2,
    rating: 4.9,
    address: 'Jl. LLRE Martadinata No. 68, Cihapit, Kota Bandung',
    schedule: 'Pukul 08.30 - 17.00 WIB',
    doctorOnCall: 'dr. Sarah N., Sp.M • Spesialis Katarak & Refraksi',
    phone: '021-7516699',
    mapsUrl: 'https://maps.google.com/?q=KMN+EyeCare+Bandung'
  },

  // --- BALI (Denpasar & Badung) ---
  {
    id: 'bali-mandara',
    name: 'RS Mata Bali Mandara',
    type: 'Pusat Rujukan Mata Bali & Nusra • RS Khusus Mata',
    region: 'Bali',
    coordinates: [-8.6539, 115.2281],
    distanceKm: 0.0,
    rating: 4.8,
    address: 'Jl. Angsoka No. 8, Dangin Puri Kangin, Denpasar Utara, Bali',
    schedule: 'IGD Mata 24 Jam • Poliklinik Eksekutif',
    doctorOnCall: 'Tim Konsultan Oftalmologi Komprehensif Bali',
    phone: '0361-243350',
    mapsUrl: 'https://maps.google.com/?q=RS+Mata+Bali+Mandara'
  },
  {
    id: 'bali-ramata',
    name: 'Ramata Eye Clinic Denpasar',
    type: 'Klinik Spesialis & Bedah Katarak Modern',
    region: 'Bali',
    coordinates: [-8.6475, 115.2033],
    distanceKm: 0.0,
    rating: 4.9,
    address: 'Jl. Gatot Subroto Barat No. 888, Denpasar, Bali',
    schedule: 'Buka Senin - Sabtu s/d 20.00 WITA',
    doctorOnCall: 'dr. I Putu Budhi, Sp.M(K) • Spesialis Retina & Anterior',
    phone: '0361-9069000',
    mapsUrl: 'https://maps.google.com/?q=Ramata+Eye+Clinic+Bali'
  },

  // --- SUMATERA (Medan, Palembang, Padang) ---
  {
    id: 'sumatera-smec-medan',
    name: 'RS Mata SMEC Medan',
    type: 'Pusat Rujukan Utama Spesialis Mata Sumatera',
    region: 'Sumatera',
    coordinates: [3.5786, 98.6601],
    distanceKm: 0.0,
    rating: 4.8,
    address: 'Jl. Iskandar Muda No. 278, Petisah Tengah, Medan, Sumut',
    schedule: 'Buka 08.00 - 21.00 WIB • Layanan Darurat',
    doctorOnCall: 'Tim Konsultan Kornea & Bedah Refraktif Medan',
    phone: '061-4512999',
    mapsUrl: 'https://maps.google.com/?q=RS+Mata+SMEC+Medan'
  },
  {
    id: 'sumatera-palembang',
    name: 'RS Khusus Mata Provinsi Sumatera Selatan',
    type: 'Rumah Sakit Khusus Mata Pemerintah Daerah',
    region: 'Sumatera',
    coordinates: [-2.9372, 104.7291],
    distanceKm: 0.0,
    rating: 4.7,
    address: 'Jl. Kol. H. Burlian KM. 6, Suka Bangun, Sukarami, Palembang',
    schedule: 'IGD Mata 24 Jam • Poliklinik Rawat Jalan',
    doctorOnCall: 'dr. Eka Novita, Sp.M • Divisi Glaukoma & Anterior',
    phone: '0711-5612838',
    mapsUrl: 'https://maps.google.com/?q=RS+Mata+Provinsi+Sumsel'
  },

  // --- DKI JAKARTA & JABODETABEK ---
  {
    id: 'jkt-jec-menteng',
    name: 'JEC Eye Hospital @ Menteng',
    type: 'Rumah Sakit Khusus Mata Berstandar Internasional',
    region: 'Jabodetabek',
    coordinates: [-6.1952, 106.8423],
    distanceKm: 0.0,
    rating: 4.9,
    address: 'Jl. Teuku Cik Ditiro No. 46, Menteng, Jakarta Pusat',
    schedule: '24 Jam Emergency Eye Care • Call Center Terpadu',
    doctorOnCall: 'Tim Konsultan Infeksi, Kornea & Bedah Katarak',
    phone: '0804-122-1000',
    mapsUrl: 'https://maps.google.com/?q=JEC+Eye+Hospital+Menteng'
  },
  {
    id: 'jkt-rs-aini',
    name: 'RS Mata AINI Prof. Dr. Isak Salim',
    type: 'Rumah Sakit Khusus Mata Rujukan Regional',
    region: 'Jabodetabek',
    coordinates: [-6.2114, 106.8305],
    distanceKm: 0.0,
    rating: 4.7,
    address: 'Jl. HR Rasuna Said Blok J No. 5, Kuningan, Jakarta Selatan',
    schedule: 'Layanan Gawat Darurat Mata 24 Jam',
    doctorOnCall: 'Tim Dokter Spesialis Mata Konsultan Strabismus & Anterior',
    phone: '021-5256228',
    mapsUrl: 'https://maps.google.com/?q=RS+Mata+AINI+Jakarta'
  },

  // --- JAWA TIMUR (Surabaya) ---
  {
    id: 'jatim-undaan',
    name: 'RS Mata Undaan Surabaya',
    type: 'Pusat Layanan Kesehatan Mata Terbesar Jawa Timur',
    region: 'Jawa Timur',
    coordinates: [-7.2562, 112.7441],
    distanceKm: 0.0,
    rating: 4.8,
    address: 'Jl. Undaan Kulon No. 19, Peneleh, Genteng, Surabaya',
    schedule: '24 Jam IGD Mata • Poliklinik Subspesialis',
    doctorOnCall: 'Tim Oftalmologi Rekonstruksi & Infeksi Eksternal',
    phone: '031-5301980',
    mapsUrl: 'https://maps.google.com/?q=RS+Mata+Undaan+Surabaya'
  },

  // --- JAWA TENGAH & DI YOGYAKARTA ---
  {
    id: 'jateng-dryap',
    name: 'RS Mata Dr. Yap Yogyakarta',
    type: 'Rumah Sakit Khusus Mata Tertua & Pusat Riset',
    region: 'Jawa Tengah & DIY',
    coordinates: [-7.7801, 110.3741],
    distanceKm: 0.0,
    rating: 4.9,
    address: 'Jl. C. Simanjuntak No. 5, Terban, Gondokusuman, Yogyakarta',
    schedule: '24 Jam Unit Gawat Darurat Mata',
    doctorOnCall: 'Tim Spesialis Mata Pediatrik, Katarak & Kornea',
    phone: '0274-562054',
    mapsUrl: 'https://maps.google.com/?q=RS+Mata+Dr+Yap+Yogyakarta'
  },

  // --- SULAWESI (Makassar) ---
  {
    id: 'sulsel-makassar',
    name: 'RS Khusus Mata Provinsi Sulawesi Selatan',
    type: 'Pusat Rujukan Mata Indonesia Timur',
    region: 'Sulawesi',
    coordinates: [-5.1328, 119.4285],
    distanceKm: 0.0,
    rating: 4.7,
    address: 'Jl. Masjid Raya No. 16, Tompo Balang, Bontoala, Makassar',
    schedule: 'IGD Mata 24 Jam • Poliklinik Spesialis',
    doctorOnCall: 'dr. Andi Muhammad, Sp.M(K) • Spesialis Kornea & Refraksi',
    phone: '0411-452140',
    mapsUrl: 'https://maps.google.com/?q=RS+Khusus+Mata+Sulawesi+Selatan'
  }
];

// Helper: Haversine distance in KM between 2 GPS coordinates
export function calculateDistanceKm(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 6371; // Earth radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return parseFloat((R * c).toFixed(1));
}

export const EMERGENCY_HOTLINE = {
  name: 'Hotline Darurat Rujukan Mata Nasional 24 Jam',
  number: '119 / 022-4231280 (Nasional)',
  desc: 'Pusat Bantuan Kegawatdaruratan Trauma & Infeksi Mata 24 Jam'
};
