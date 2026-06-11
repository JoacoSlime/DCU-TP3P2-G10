<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { obtenerPuntoPorId } from '@/services/puntosService.js'
import { computed } from 'vue'
import MigasDePan from '@/components/MigasPan.vue'

const route = useRoute()
const punto = ref(null)

// Log para ver qué hay en route.params
console.log('route.params:', route.params)
console.log('route.params.id:', route.params.id)

onMounted(async () => {
    const id = route.params.id
    console.log('ID obtenido:', id)

    if (id) {
        try {
            punto.value = await obtenerPuntoPorId(id)
            console.log('Punto cargado:', punto.value)
        } catch (error) {
            console.error('Error al cargar punto:', error)
        }
    } else {
        console.error('No hay ID en la ruta')
    }
})
const migas = computed(() => [
    {
        texto: 'Inicio',
        ruta: '/'
    },
    {
        texto: 'Listado de puntos',
        ruta: '/listado-puntos'
    },
    {
        texto: punto.value?.nombre || 'Punto'
    }
])
</script>

<template>
    <div v-if="punto">
        <MigasDePan :items="migas" />
        <h2>{{ punto.nombre }}</h2>
        <p><strong>Nivel contaminación:</strong> {{ punto.contaminacion }}</p>
        <p><strong>Descripción:</strong> {{ punto.descripcion }}</p>
        <p><strong>Colaborador:</strong> {{ punto.colaborador }}</p>
        <p><strong>Fecha creación:</strong> {{ punto.fechaCreacion }}</p>
        <div>
            <router-link :to="`/punto/${punto.id}/agregar-medicion`">Agregar medición</router-link>
            |
            <router-link :to="`/punto/${punto.id}/historial`">Ver datos históricos</router-link>
        </div>
    </div>
    <div v-else>Cargando...</div>
</template>
