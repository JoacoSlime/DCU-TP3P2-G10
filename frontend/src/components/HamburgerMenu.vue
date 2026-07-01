<template>
  <button
    class="hamburger-button"
    :class="{ 'show-button': showButton }"
    type="button"
    aria-label="Open navigation menu"
    @click="openMenu"
  >
    <ion-icon name="menu"></ion-icon>
  </button>
  <div class="hamburger-menu-wrapper">
    <transition name="fade">
      <div v-if="isOpen" class="menu-backdrop" @click="closeMenu" />
    </transition>

    <transition name="slide-up">
      <nav v-if="isOpen" class="mobile-sheet" aria-label="Mobile navigation">
        <div class="sheet-header">
          <h2>Menú</h2>
          <button
            class="close-btn"
            type="button"
            aria-label="Close navigation menu"
            @click="closeMenu"
          >
            <ion-icon name="close"></ion-icon>
          </button>
        </div>

        <router-link to="/" class="menu-item" @click="closeMenu">Mapa</router-link>
        <router-link to="/listado-puntos" class="menu-item" @click="closeMenu">
          Listado de puntos
        </router-link>
        <router-link to="/ajustes" class="menu-item" @click="closeMenu"> Ajustes </router-link>
      </nav>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  showButton: {
    type: Boolean,
    default: true,
  },
})

const isOpen = ref(false)

const openMenu = () => {
  isOpen.value = true
}

const closeMenu = () => {
  isOpen.value = false
}
</script>

<style scoped>
ion-icon {
  flex: 1;
  font-size: 32px;
}

.hamburger-menu-wrapper {
  position: relative;
  z-index: 3000;
}

.hamburger-button {
  border: none;
  display: none;
  background: #2c3e50;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  height: 100%;
  aspect-ratio: 1 / 1;
}

/* mostrar solo en celular */
@media screen and (max-width: 930px) {
  .hamburger-button.show-button {
    display: flex;
  }
}

.hamburger-button:active {
  transform: scale(0.97);
}

.menu-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
}

.mobile-sheet {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: #ffffff;
  border-radius: 18px 18px 0 0;
  box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.2);
  padding: 14px 16px 22px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.sheet-header h2 {
  margin: 0;
  font-size: 1.05rem;
  color: #2c3e50;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 1.1rem;
  color: #2c3e50;
  cursor: pointer;
}

.menu-item {
  display: block;
  text-decoration: none;
  color: #2c3e50;
  font-weight: 600;
  padding: 12px 10px;
  border-radius: 10px;
  background: #f5f7fa;
}

.menu-item.router-link-active {
  background: #008737;
  color: #fff;
}

/* transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition:
    transform 0.25s ease,
    opacity 0.25s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
