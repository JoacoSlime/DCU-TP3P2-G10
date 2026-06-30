<script setup>
import { ref, onMounted } from 'vue'
import { obtenerPuntos } from '@/services/puntosService.js'
import Bienvenida from '@/components/Bienvenida.vue'

const puntos = ref([])
const hasVisited = localStorage.getItem('hasVisited')

const showModal = ref(!hasVisited)

onMounted(async () => {
  puntos.value = await obtenerPuntos()
})
</script>

<template>
  <section class="mapa">
    <div>
        <h2>Mapa y puntos contaminados</h2>
        <div style="margin-bottom: 1rem;">
            <router-link to="/agregar-punto" class="boton">
                + Agregar nuevo punto
            </router-link>
        </div>

        <div style="background:#bdc3c7; height:300px; display:flex; align-items:center; justify-content:center;">
            Mapa
        </div>

        <h3>Listado de puntos</h3>
        <ul>
            <li v-for="punto in puntos" :key="punto.id">
                <router-link :to="`/punto/${punto.id}`">{{ punto.nombre }}</router-link>
            </li>
        </ul>
    </div>

    <div
      style="
        background: #bdc3c7;
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
      "
    >
      Mapa
    </div>

    <h3>Listado de puntos</h3>
    <ul>
      <li v-for="punto in puntos" :key="punto.id">
        <router-link :to="`/punto/${punto.id}`">{{ punto.title }}</router-link>
      </li>
    </ul>
  </section>
  <Bienvenida v-if="showModal" @close="showModal = false" />
</template>
