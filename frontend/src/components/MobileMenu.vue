<script setup>
import { inject } from 'vue'

const closeMobileMenu = inject('closeMobileMenu')
</script>

<template>
  <nav class="mobile-sheet">
    <router-link to="/" class="menu-item" @click="closeMobileMenu">Mapa</router-link>
    <router-link to="/listado-puntos" class="menu-item" @click="closeMobileMenu">
      Listado de puntos
    </router-link>
    <router-link to="/ajustes" class="menu-item" @click="closeMobileMenu"> Ajustes </router-link>
  </nav>
</template>

<style scoped>
.mobile-sheet {
  z-index: 5000;
  background: #fff;
  border-radius: 18px 18px 0 0;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: end;
  height: 100%;
  width: 100%;
  gap: 8px;
  overflow: hidden;

  transform: translateY(100%);
  animation: sheet-in 0.25s ease-out forwards;
  will-change: transform;
}

.sheet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.menu-item {
  display: block;
  padding: 12px;
  border-radius: 10px;
  text-decoration: none;
  color: #2c3e50;
  background: #f5f7fa;
  font-weight: 600;
}

.menu-item.router-link-active {
  background: #008737;
  color: #fff;
}

@keyframes sheet-in {
  from {
    transform: translateY(24px); /* small offset avoids page overflow jump */
  }
  to {
    transform: translateY(0);
  }
}
</style>
