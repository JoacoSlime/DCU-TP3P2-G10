<script setup>
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import Modal from '../components/Modal.vue'
import ListCard from '../components/ListCard.vue'

let map = null
const showModal = ref(true)

const puntosContaminacion = [
  { id: 1, lat: -34.7, lng: -58.2, nivel: 'alto', nombre: 'BER: BERNAL' },
  { id: 2, lat: -34.9, lng: -57.9, nivel: 'bajo', nombre: 'LP: LA PLATA' }
]

onMounted(() => {

  const logged = localStorage.getItem('logged');
  const role = localStorage.getItem('role');

  console.log("--- DEBUG DE SESIÓN ---");
  console.log("Valor de 'logged':", logged);
  console.log("Valor de 'role':", role);
  
  showModal.value = true;
  console.log("ShowModal ahora es:", showModal.value);

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

const searchQuery = ref('')
import { computed } from 'vue'

const puntosFiltrados = computed(() => {
  const query = searchQuery.value.toLowerCase();
 
  if (!query) return puntosContaminacion;
  

  return puntosContaminacion.filter(p => 
    p.nombre.toLowerCase().includes(query)
  );
})

</script>

<template>
  <div class="map-container">
    <div id="map"></div>
    
    <ListCard v-if="!showModal"
      class="floating-list"
      title="Puntos de Contaminación" 
      :items="puntosFiltrados" 
      @go-to="centrarMapa" 
    />
    <p v-if="puntosFiltrados.length === 0">No se encontraron puntos</p>
    <Modal v-if="showModal" :show="true" @close="showModal = false" />
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