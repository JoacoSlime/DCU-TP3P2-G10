<script setup>
import { watch, ref, provide } from 'vue'
import { useRoute } from 'vue-router'
import HamburgerButton from '@/components/HamburgerButton.vue'
import MobileMenu from '@/components/MobileMenu.vue'

function ayuda() {
  alert('Envía un correo a administrador@admin.com')
}

const route = useRoute()
const mainScreen = ref(route.path === '/')
const mobileMenuOpen = ref(false)

watch(
  () => route.path,
  (newPath) => {
    mainScreen.value = newPath === '/'
  }
)

const openMobileMenu = () => (mobileMenuOpen.value = true)
const closeMobileMenu = () => (mobileMenuOpen.value = false)
const toggleMobileMenu = () => (mobileMenuOpen.value = !mobileMenuOpen.value)

provide('mobileMenuOpen', mobileMenuOpen)
provide('openMobileMenu', openMobileMenu)
provide('closeMobileMenu', closeMobileMenu)
provide('toggleMobileMenu', toggleMobileMenu)
provide('mainScreen', mainScreen)
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="header-menu-btn" v-if="!mainScreen">
        <HamburgerButton @click="toggleMobileMenu" />
      </div>
      <h1>Contaminación de la franja costera sur</h1>
    </header>

    <!-- Menú móvil lateral (slide-in) -->
    <MobileMenu v-if="mobileMenuOpen" @close="closeMobileMenu" />

    <div class="contenedor-principal">
      <!-- Sidebar Desktop -->
      <aside class="sidebar">
        <nav class="menu">
          <router-link to="/" class="menu-item">
            <span class="mobile-nav-icon">🗺️</span>
            <span class="mobile-nav-label">Mapa</span></router-link>
          <router-link to="/listado-puntos" class="menu-item">
            <span class="mobile-nav-icon">📋</span>
            <span class="mobile-nav-label">Listado</span>s</router-link>
          <router-link to="/ajustes" class="menu-item">
            <span class="mobile-nav-icon">⚙️</span>
            <span class="mobile-nav-label">Ajustes</span></router-link>
        </nav>
      </aside>

      <!-- Contenido principal -->
      <main class="contenido" :class="{ 'main-screen': mainScreen }">
        <router-view />
      </main>

      <!-- Botón ayuda -->
      <button class="boton-ayuda-flotante" @click="ayuda">Necesito ayuda</button>
    </div>

    <!-- ===== MENÚ INFERIOR MÓVIL ===== -->
    <nav class="mobile-bottom-nav">
      <router-link to="/" class="mobile-nav-item">
        <span class="mobile-nav-icon">🗺️</span>
        <span class="mobile-nav-label">Mapa</span>
      </router-link>
      <router-link to="/listado-puntos" class="mobile-nav-item">
        <span class="mobile-nav-icon">📋</span>
        <span class="mobile-nav-label">Listado</span>
      </router-link>
      <router-link to="/ajustes" class="mobile-nav-item">
        <span class="mobile-nav-icon">⚙️</span>
        <span class="mobile-nav-label">Ajustes</span>
      </router-link>
    </nav>
  </div>
</template>

<style>
/* Reset global */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: #ecf0f1;
  font-family: 'Segoe UI', Roboto, sans-serif;
}
</style>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #ecf0f1;
  overflow: hidden;
}

/* ===== HEADER ===== */
.header {
  background: #2c3e50;
  padding: 12px 16px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  z-index: 10;
}

.header-menu-btn {
  display: none;
  flex-shrink: 0;
}

.header h1 {
  margin: 0;
  flex: 1;
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
  text-align: center;
  letter-spacing: 0.5px;
}

/* ===== LAYOUT ===== */
.contenedor-principal {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
  min-height: 0;
}

/* ===== SIDEBAR ===== */
.sidebar {
  width: 220px;
  background: #3a4a5f;
  padding: 20px 12px;
  flex-shrink: 0;
  overflow-y: auto;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.menu-item {
  display: block;
  padding: 10px 16px;
  color: #ffffff;
  text-decoration: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  transition: background 0.2s;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.15);
}

.menu-item.router-link-active {
  background: #008737;
  color: #ffffff;
  font-weight: 600;
}

/* ===== CONTENIDO ===== */
.contenido {
  flex: 1;
  overflow-y: auto;
  background: #ecf0f1;
}

.contenido:not(.main-screen) {
  padding: 1.5rem;
}

/* ===== BOTÓN AYUDA ===== */
.boton-ayuda-flotante {
  position: absolute;
  bottom: 80px;
  right: 20px;
  background: #008737;
  color: #ffffff;
  border: none;
  padding: 10px 18px;
  border-radius: 40px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
  transition: background 0.2s;
  z-index: 100;
}

.boton-ayuda-flotante:hover {
  background: #006b2c;
}

/* ===== MENÚ INFERIOR MÓVIL ===== */
.mobile-bottom-nav {
  display: none;
  /* Oculto en desktop */
  background: #3a4a5f;
  border-top: 2px solid #2c3e50;
  padding: 6px 0 8px 0;
  flex-shrink: 0;
  justify-content: space-around;
  align-items: center;
  z-index: 5;
}

.mobile-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 4px 12px;
  color: #a0b0c0;
  text-decoration: none;
  font-size: 0.6rem;
  font-weight: 500;
  border-radius: 6px;
  transition: color 0.2s, background 0.2s;
  min-width: 50px;
}

.mobile-nav-item .mobile-nav-icon {
  font-size: 1.4rem;
}

.mobile-nav-item .mobile-nav-label {
  font-size: 0.55rem;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.mobile-nav-item:hover {
  color: #ffffff;
}

.mobile-nav-item.router-link-active {
  color: #ffffff;
  background: #008737;
  border-radius: 8px;
  padding: 4px 12px;
}

/* ============================================================ */
/* ===== RESPONSIVE: MÓVIL ===== */
/* ============================================================ */
@media screen and (max-width: 768px) {

  /* Mostrar botón hamburguesa en header */
  .header-menu-btn {
    display: block;
  }

  .header h1 {
    font-size: 1rem;
  }

  /* Ocultar sidebar desktop */
  .sidebar {
    display: none;
  }

  .contenido:not(.main-screen) {
    padding: 12px;
  }

  /* Mostrar menú inferior */
  .mobile-bottom-nav {
    display: flex;
  }

  /* Botón ayuda se mueve arriba del menú inferior */
  .boton-ayuda-flotante {
    bottom: 70px;
    right: 16px;
    padding: 8px 14px;
    font-size: 0.8rem;
  }
}

/* Móviles muy pequeños */
@media screen and (max-width: 400px) {
  .header h1 {
    font-size: 0.8rem;
  }

  .mobile-nav-item .mobile-nav-icon {
    font-size: 1.1rem;
  }

  .mobile-nav-item .mobile-nav-label {
    font-size: 0.45rem;
  }

  .mobile-nav-item {
    padding: 2px 6px;
    min-width: 40px;
  }
}
</style>