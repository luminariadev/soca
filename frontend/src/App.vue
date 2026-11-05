<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { TabType, ScanResult } from './types';
import Header from './components/Header.vue';
import Sidebar from './components/Sidebar.vue';
import MobileNavbar from './components/MobileNavbar.vue';
import HistoryModal from './components/HistoryModal.vue';
import AboutModal from './components/AboutModal.vue';
import BerandaView from './views/BerandaView.vue';
import PemindaianView from './views/PemindaianView.vue';
import HasilView from './views/HasilView.vue';
import EnsiklopediaView from './views/EnsiklopediaView.vue';
import PrivasiView from './views/PrivasiView.vue';

const validTabs: TabType[] = ['beranda', 'pindai', 'hasil', 'edukasi', 'privasi'];

const getInitialTab = (): TabType => {
  if (typeof window !== 'undefined') {
    const hash = window.location.hash.replace('#', '') as TabType;
    if (validTabs.includes(hash)) return hash;
    const saved = localStorage.getItem('soca_active_tab') as TabType;
    if (validTabs.includes(saved)) return saved;
  }
  return 'beranda';
};

const currentTab = ref<TabType>(getInitialTab());
const sidebarCollapsed = ref(false);
const showHistoryModal = ref(false);
const showAboutModal = ref(false);
const latestResult = ref<ScanResult | null>(null);
const scanHistory = ref<ScanResult[]>([]);

const selectTab = (tab: TabType) => {
  currentTab.value = tab;
  if (typeof window !== 'undefined') {
    window.location.hash = tab;
    localStorage.setItem('soca_active_tab', tab);
  }
};

// Load history & latest result from localStorage
const loadHistory = () => {
  try {
    const raw = localStorage.getItem('soca_scan_history');
    if (raw) {
      scanHistory.value = JSON.parse(raw);
    }
  } catch (e) {
    scanHistory.value = [];
  }

  try {
    const rawLatest = localStorage.getItem('soca_latest_result');
    if (rawLatest) {
      latestResult.value = JSON.parse(rawLatest);
    }
  } catch (e) {}
};

const saveHistory = (result: ScanResult) => {
  scanHistory.value.unshift(result);
  if (scanHistory.value.length > 20) {
    scanHistory.value = scanHistory.value.slice(0, 20);
  }
  try {
    localStorage.setItem('soca_scan_history', JSON.stringify(scanHistory.value));
  } catch (e) {}
};

const clearHistory = () => {
  scanHistory.value = [];
  try {
    localStorage.removeItem('soca_scan_history');
  } catch (e) {}
};

const handleScanComplete = (result: ScanResult) => {
  latestResult.value = result;
  try {
    localStorage.setItem('soca_latest_result', JSON.stringify(result));
  } catch (e) {}
  saveHistory(result);
  selectTab('hasil');
};

const handleSelectHistoryResult = (item: ScanResult) => {
  latestResult.value = item;
  try {
    localStorage.setItem('soca_latest_result', JSON.stringify(item));
  } catch (e) {}
  showHistoryModal.value = false;
  selectTab('hasil');
};

// Check tablet & mobile screens to avoid cramped desktop view
const checkScreenSize = () => {
  if (window.innerWidth < 1180) {
    sidebarCollapsed.value = true;
  }
};

onMounted(() => {
  loadHistory();
  checkScreenSize();
  window.addEventListener('resize', checkScreenSize);
  window.addEventListener('hashchange', () => {
    const hash = window.location.hash.replace('#', '') as TabType;
    if (validTabs.includes(hash)) {
      currentTab.value = hash;
    }
  });
});
</script>

<template>
  <div class="h-screen w-screen bg-background text-on-surface flex flex-row antialiased selection:bg-primary-container selection:text-on-primary-container overflow-hidden">
    <!-- Desktop Collapsible Sidebar (h-full: Reaches the absolute bottom of the screen ALWAYS) -->
    <Sidebar
      :currentTab="currentTab"
      :isCollapsed="sidebarCollapsed"
      @selectTab="selectTab"
      @openAbout="showAboutModal = true"
    />

    <!-- Main Workspace Column (100% Contiguous with Sidebar, Zero Void) -->
    <div class="flex-1 flex flex-col min-w-0 h-full overflow-hidden">
      <!-- Header with Unified Sidebar Toggle & About Button -->
      <Header
        :historyCount="scanHistory.length"
        :sidebarCollapsed="sidebarCollapsed"
        @toggleSidebar="sidebarCollapsed = !sidebarCollapsed"
        @openHistory="showHistoryModal = true"
        @openAbout="showAboutModal = true"
      />

      <!-- Main Workspace Container (Internal Smooth Scroll, Generous Mobile Bottom Padding) -->
      <main class="flex-1 w-full overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 pb-36 md:pb-12">
        <div class="max-w-[1600px] mx-auto">
          <transition name="fade" mode="out-in">
            <component
              :is="
                currentTab === 'beranda' ? BerandaView :
                currentTab === 'pindai' ? PemindaianView :
                currentTab === 'hasil' ? HasilView :
                currentTab === 'edukasi' ? EnsiklopediaView :
                PrivasiView
              "
              :result="latestResult"
              @navigate="selectTab"
              @scanComplete="handleScanComplete"
              @newScan="selectTab('pindai')"
            />
          </transition>
        </div>
      </main>
    </div>

    <!-- Mobile Floating iOS Liquid Glass Navbar -->
    <MobileNavbar
      :currentTab="currentTab"
      @selectTab="selectTab"
    />

    <!-- History Drawer / Modal -->
    <HistoryModal
      :isOpen="showHistoryModal"
      :history="scanHistory"
      @close="showHistoryModal = false"
      @selectResult="handleSelectHistoryResult"
      @clearHistory="clearHistory"
    />

    <!-- About Creator Modal -->
    <AboutModal
      :isOpen="showAboutModal"
      @close="showAboutModal = false"
    />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
