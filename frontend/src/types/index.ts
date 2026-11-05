export type TabType = 'beranda' | 'pindai' | 'hasil' | 'edukasi' | 'privasi';

export interface ClassProbability {
  name: string;
  probability: number; // 0 to 100
  icd10?: string;
}

export interface DiagnosticCondition {
  id: string;
  name: string;
  latinName: string;
  icd10: string;
  category: string;
  description: string;
  severity: 'Aman / Normal' | 'Ringan' | 'Sedang' | 'Perlu Penanganan Cepat';
  symptoms: string[];
  selfCare: {
    title: string;
    desc: string;
    icon: string;
  }[];
  restrictions: string[];
  redFlags: string[];
  imageUrl: string;
}

export interface ScanResult {
  id: string;
  timestamp: string;
  conditionName: string;
  confidence: number; // e.g. 97.99
  icd10: string;
  severity: 'Aman / Normal' | 'Ringan' | 'Sedang' | 'Perlu Penanganan Cepat';
  probabilities: ClassProbability[];
  imageSrc?: string;
  notes?: string;
}

export interface ClinicProvider {
  id: string;
  name: string;
  type: string; // e.g. "Pusat Mata Spesialis"
  region: string; // e.g. "Jawa Barat", "Bali", "Sumatera", "Jabodetabek", etc.
  coordinates: [number, number]; // [lat, lng]
  distanceKm: number;
  rating: number;
  address: string;
  schedule: string;
  doctorOnCall: string;
  phone: string;
  mapsUrl: string;
}
