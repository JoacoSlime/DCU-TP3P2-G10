<template>
  <LayoutGeneral v-if="rutasConLayout">
    <router-view />
  </LayoutGeneral>
  <router-view v-else />
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import LayoutGeneral from '@/layouts/LayoutGeneral.vue'

const route = useRoute()

// Rutas que NO deben tener menú lateral
const rutasSinLayout = ['/elegir-usuario', '/ayuda', '/iniciar-sesion']

const rutasConLayout = computed(() => {
  return !rutasSinLayout.includes(route.path)
})

onMounted(() => {
  const scriptesm = document.createElement('script')
  scriptesm.type = 'module'
  scriptesm.src = 'https://unpkg.com/ionicons@8.0.13/dist/ionicons/ionicons.esm.js'
  document.body.appendChild(scriptesm)

  const script = document.createElement('script')
  script.setAttribute('nomodule', '')
  script.src = 'https://unpkg.com/ionicons@8.0.13/dist/ionicons/ionicons.js'
  document.body.appendChild(script)
})
</script>
