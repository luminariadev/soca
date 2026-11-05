<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import type { ClinicProvider } from '../types';

const props = defineProps<{
  clinics: ClinicProvider[];
  selectedClinicId?: string | null;
  userCoordinates?: [number, number] | null;
}>();

const mapContainer = ref<HTMLDivElement | null>(null);
let map: L.Map | null = null;
let markersLayer: L.LayerGroup | null = null;
let userMarker: L.Marker | null = null;
const markers: Record<string, L.Marker> = {};

const createCustomPin = (clinic: ClinicProvider) => {
  const isSelected = props.selectedClinicId === clinic.id;
  const pinHtml = `
    <div class="relative flex items-center justify-center cursor-pointer group">
      <div class="w-8 h-8 rounded-full ${isSelected ? 'bg-primary ring-4 ring-primary/40' : 'bg-primary-container'} text-white flex items-center justify-center shadow-[0_0_20px_rgba(49,152,220,0.85)] border-2 border-white transition-transform group-hover:scale-125">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
        </svg>
      </div>
      <div class="absolute -bottom-1 w-2 h-2 ${isSelected ? 'bg-primary' : 'bg-primary-container'} rotate-45"></div>
      <span class="absolute -bottom-6 px-2 py-0.5 rounded-md bg-surface-container-lowest/95 backdrop-blur-md text-[10px] font-mono text-on-surface whitespace-nowrap shadow-md border border-outline-variant/30 pointer-events-none">
        ${clinic.name.split(' ')[0]} ${clinic.distanceKm > 0 ? clinic.distanceKm + 'km' : ''}
      </span>
    </div>
  `;

  return L.divIcon({
    html: pinHtml,
    className: 'custom-leaflet-marker',
    iconSize: [32, 40],
    iconAnchor: [16, 36],
    popupAnchor: [0, -36]
  });
};

const createUserPin = () => {
  const pinHtml = `
    <div class="relative flex items-center justify-center">
      <div class="w-6 h-6 rounded-full bg-emerald-400/40 animate-ping absolute"></div>
      <div class="w-5 h-5 rounded-full bg-emerald-500 border-2 border-white shadow-[0_0_16px_#10b981] flex items-center justify-center">
        <div class="w-2 h-2 rounded-full bg-white"></div>
      </div>
      <span class="absolute -bottom-6 px-2 py-0.5 rounded-md bg-emerald-950/90 text-emerald-300 font-mono text-[10px] whitespace-nowrap border border-emerald-500/40 shadow-lg pointer-events-none">
        📍 Posisi Anda
      </span>
    </div>
  `;
  return L.divIcon({
    html: pinHtml,
    className: 'custom-leaflet-marker',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  });
};

const renderMarkers = () => {
  if (!map) return;
  if (markersLayer) {
    markersLayer.clearLayers();
  } else {
    markersLayer = L.layerGroup().addTo(map);
  }

  // Clear markers map
  for (const k in markers) delete markers[k];

  // Render Clinics
  props.clinics.forEach((clinic) => {
    const coords = clinic.coordinates;
    const marker = L.marker(coords, { icon: createCustomPin(clinic) });

    const popupHtml = `
      <div style="font-family: 'Inter', sans-serif; color: #dee2ee; background: #171c24; padding: 12px; border-radius: 12px; border: 1px solid rgba(147,204,255,0.25); min-width: 230px;">
        <div style="font-weight: 700; font-size: 13px; color: #93ccff; margin-bottom: 2px;">${clinic.name}</div>
        <div style="font-size: 10px; color: #38bdf8; font-family: monospace; margin-bottom: 5px;">${clinic.region} • ${clinic.type}</div>
        <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px;">${clinic.address}</div>
        <div style="font-size: 11px; color: #47e266; font-weight: 600; margin-bottom: 6px;">⭐ ${clinic.rating} ${clinic.distanceKm > 0 ? `• ${clinic.distanceKm} km dari posisi Anda` : ''}</div>
        <div style="font-size: 11px; color: #dee2ee; margin-bottom: 8px;">📞 ${clinic.phone}</div>
        <a href="${clinic.mapsUrl}" target="_blank" style="display: block; text-align: center; background: #3198dc; color: #ffffff; text-decoration: none; padding: 6px 10px; border-radius: 8px; font-weight: 600; font-size: 11px;">
          Buka Rute Navigasi ↗
        </a>
      </div>
    `;

    marker.bindPopup(popupHtml, { className: 'soca-dark-popup' });
    markers[clinic.id] = marker;
    if (markersLayer) {
      markersLayer.addLayer(marker);
    }
  });

  // Render User Marker
  if (props.userCoordinates) {
    if (userMarker) {
      userMarker.remove();
    }
    userMarker = L.marker(props.userCoordinates, { icon: createUserPin() }).addTo(map);
  }
};

const initMap = () => {
  if (!mapContainer.value) return;

  const initialCenter: [number, number] = props.userCoordinates || 
    (props.clinics.length > 0 ? props.clinics[0].coordinates : [-6.918, 107.615]);

  map = L.map(mapContainer.value, {
    center: initialCenter,
    zoom: 12,
    zoomControl: false,
    attributionControl: false
  });

  // ESRI World Dark Gray Base
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 16,
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
  }).addTo(map);

  // ESRI World Dark Gray Reference
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 16,
  }).addTo(map);

  L.control.zoom({ position: 'bottomright' }).addTo(map);
  L.control.attribution({ position: 'bottomleft', prefix: 'Leaflet | &copy; Esri & OpenStreetMap' }).addTo(map);

  renderMarkers();
};

watch(() => props.clinics, () => {
  renderMarkers();
  if (map && props.clinics.length > 0) {
    const group = L.featureGroup(Object.values(markers));
    if (props.userCoordinates && userMarker) {
      group.addLayer(userMarker);
    }
    map.fitBounds(group.getBounds().pad(0.2), { maxZoom: 13, duration: 1.0 });
  }
}, { deep: true });

watch(() => props.userCoordinates, (newCoords) => {
  if (newCoords && map) {
    if (userMarker) userMarker.remove();
    userMarker = L.marker(newCoords, { icon: createUserPin() }).addTo(map);
    map.flyTo(newCoords, 13, { duration: 1.2 });
  }
});

watch(() => props.selectedClinicId, (newId) => {
  if (newId && map) {
    const clinic = props.clinics.find(c => c.id === newId);
    if (clinic) {
      map.flyTo(clinic.coordinates, 14, { duration: 1.2 });
      if (markers[newId]) {
        markers[newId].openPopup();
      }
    }
  }
});

onMounted(() => {
  setTimeout(() => {
    initMap();
  }, 100);
});

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});
</script>

<template>
  <div class="relative w-full h-[400px] rounded-2xl overflow-hidden border border-outline-variant/30 shadow-xl bg-surface-container-lowest">
    <div ref="mapContainer" class="w-full h-full z-0"></div>

    <!-- Status Floating Capsule -->
    <div class="absolute top-3 left-3 z-10 flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-container-lowest/90 backdrop-blur-md border border-outline-variant/40 shadow-lg text-[11px] font-mono text-on-surface">
      <span class="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
      <span>Peta Topologi Klinis: ESRI Dark Canvas + Leaflet</span>
    </div>
  </div>
</template>

<style>
.custom-leaflet-marker {
  background: transparent !important;
  border: none !important;
}
</style>
