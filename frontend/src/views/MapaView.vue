<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { ref } from 'vue'
import Modal from '../components/Modal.vue'
import ListCard from '../components/ListCard.vue'

const showModal = ref(true)

// Simulación de datos (esto vendría de tu backend en Rust)
const puntosContaminacion = [
  { id: 1, lat: -34.7, lng: -58.2, nivel: 'alto', nombre: 'BER: BERNAL' },
  { id: 2, lat: -34.9, lng: -57.9, nivel: 'bajo', nombre: 'LP: LA PLATA' }
]

onMounted(() => {
  const map = L.map('map').setView([-34.7, -58.2], 10)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)

  puntosContaminacion.forEach(p => {
    // Definimos colores según nivel
    const colores = { alto: 'red', medio: 'orange', bajo: 'yellow' }
    
    // Crear marcador con color
    L.circleMarker([p.lat, p.lng], {
      color: colores[p.nivel],
      radius: 10,
      fillOpacity: 0.8
    }).addTo(map).bindPopup(p.nombre)
  })
})

const centrarMapa = (punto) => {
  // Aquí accedes al objeto Leaflet 'map' y haces el setView
  map.setView([punto.lat, punto.lng], 15)
}
</script>

<template>
  <div class="map-container">
    <div id="map"></div>
    
    <ListCard v-if="!showModal"
      class="floating-list"
      title="Puntos de Contaminación" 
      :items="puntosContaminacion" 
      @go-to="centrarMapa" 
    />
    <Modal :show="showModal" @close="showModal = false" />
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
}
</style>