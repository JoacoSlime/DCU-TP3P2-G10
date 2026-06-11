<script setup>
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import Modal from '../components/Modal.vue'
import ListCard from '../components/ListCard.vue'

let map = null
const showModal = ref(false)

const puntosContaminacion = [
  { id: 1, lat: -34.7, lng: -58.2, nivel: 'alto', nombre: 'BER: BERNAL' },
  { id: 2, lat: -34.9, lng: -57.9, nivel: 'bajo', nombre: 'LP: LA PLATA' }
]

onMounted(() => {

  console.log("ROLE RAW:", localStorage.getItem('role'))
  const role = (localStorage.getItem('role') || '').trim().toLowerCase()
  showModal.value = role !== 'admin'

  map = L.map('map').setView([-34.7, -58.2], 10)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)

  puntosContaminacion.forEach(p => {
    const colores = { alto: 'red', medio: 'orange', bajo: 'yellow' }

    L.circleMarker([p.lat, p.lng], {
      color: colores[p.nivel],
      radius: 10,
      fillOpacity: 0.8
    })
      .addTo(map)
      .bindPopup(p.nombre)
  })
})

const centrarMapa = (punto) => {
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
    <Modal v-if="showModal" @close="showModal = false" />
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