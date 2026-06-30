<script setup>
import { ref, onMounted, computed } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import Modal from '../components/Modal.vue'
import ListCard from '../components/ListCard.vue'
import { obtenerPuntos } from '@/services/puntosService.js'
import IniciarSesionModal from '../components/IniciarSesionModal.vue'

let map = null
const showModal = ref(true)
const puntos = ref([])
const searchQuery = ref('')
const mostrarLogin = ref(false)

// Puntos filtrados por búsqueda
const puntosFiltrados = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  if (!query) return puntos.value
  return puntos.value.filter(p =>
    p.nombre?.toLowerCase().includes(query) ||
    p.title?.toLowerCase().includes(query)
  )
})

const getColor = (nivel) => {
  const colores = {
    alto: '#e53e3e',
    media: '#dd6b20',
    baja: '#d69e2e'
  }
  return colores[nivel?.toLowerCase()] || '#a0aec0'
}

onMounted(async () => {
  //Cargar puntos desde la API
  puntos.value = await obtenerPuntos()
  console.log('Puntos cargados:', puntos.value)

  //Verificar sesión para el modal
  const logged = localStorage.getItem('logged')
  const token = localStorage.getItem('auth_token')
  const role = localStorage.getItem('role')
  const yaVioModal = localStorage.getItem('yaVioModal')

  console.log("--- DEBUG DE SESIÓN ---")
  console.log("Valor de 'logged':", logged)
  console.log("Valor de 'role':", role)

  // SI ESTÁ LOGUEADO → NO MOSTRAR MODAL (prioridad máxima)
  if (logged === 'true' || token) {
    showModal.value = false
  }
  // SI NO ESTÁ LOGUEADO PERO YA VIO EL MODAL → NO MOSTRAR
  else if (yaVioModal === 'true') {
    showModal.value = false
  }
  // SI NO ESTÁ LOGUEADO Y NO VIO EL MODAL → MOSTRAR
  else {
    showModal.value = true
  }
  console.log("ShowModal ahora es:", showModal.value)

  //Inicializar el mapa
  map = L.map('map').setView([-34.7, -58.2], 10)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map)

  //Agregar marcadores al mapa
  puntos.value.forEach(p => {
    const lat = p.lat || p.latitude
    const lng = p.lng || p.longitude

    if (lat && lng) {
      L.circleMarker([parseFloat(lat), parseFloat(lng)], {
        color: getColor(p.contaminacion),
        radius: 10,
        fillOpacity: 0.8,
        weight: 2
      })
        .addTo(map)
        .bindPopup(`<b>${p.nombre || p.title}</b><br>Contaminación: ${p.contaminacion || 'Media'}`)
    }
  })
})

const centrarMapa = (punto) => {
  if (map) {
    const lat = punto.lat || punto.latitude
    const lng = punto.lng || punto.longitude
    map.setView([parseFloat(lat), parseFloat(lng)], 15)
  }
}

const cerrarModal = () => {
  showModal.value = false
  localStorage.setItem('yaVioModal', 'true')
}

const manejarLoginExitoso = () => {
  mostrarLogin.value = false
  showModal.value = false
  localStorage.setItem('yaVioModal', 'true')
}
</script>

<template>
  <div class="map-container">
    <div id="map"></div>

    <ListCard v-if="!showModal" class="floating-list" title="Puntos de Contaminación" :items="puntosFiltrados"
      @go-to="centrarMapa" />

    <Modal v-if="showModal" :show="true" @close="cerrarModal" />
    <IniciarSesionModal v-if="mostrarLogin" @close="mostrarLogin = false" @login-success="manejarLoginExitoso" />
  </div>
</template>

<style scoped>
.map-container {
  position: relative;
  height: 100vh;
  width: 100%;
}

#map {
  height: 100%;
  width: 100%;
  z-index: 1;
}

.floating-list {
  position: absolute;
  top: 70px;
  right: 20px;
  z-index: 1000;
  width: 300px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
}
</style>