<template>
  <LayoutGeneral v-if="rutasConLayout">
    <router-view />
  </LayoutGeneral>
  <router-view v-else />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import LayoutGeneral from '@/layouts/LayoutGeneral.vue'

const route = useRoute()

// Rutas que NO deben tener menú lateral
const rutasSinLayout = ['/elegir-usuario', '/ayuda', '/iniciar-sesion']

const rutasConLayout = computed(() => {
  return !rutasSinLayout.includes(route.path)
})
</script>
