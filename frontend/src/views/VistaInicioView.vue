<script setup>
import { ref, onMounted } from 'vue'
import { obtenerPuntos } from '@/services/puntosService.js'

const puntos = ref([])
onMounted(async () => {
    puntos.value = await obtenerPuntos()
})
</script>
<template>
    <div>
        <h2>Mapa y puntos contaminados</h2>

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
</template>